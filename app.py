import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from functools import wraps
import time

# Decorator for measuring execution time
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"\nFunction {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper

# Function to get text from PDF documents
@timeit
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
@timeit
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector store
@timeit
def get_vectorstore(text_chunks):
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large:latest"
    )
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create a conversation chain
@timeit
def get_conversation_chain(vectorstore):
    llm = ChatOllama(
        model="llama3:latest",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain

# Function to handle user input and generate responses
@timeit
def handle_userinput(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )

# Simple Student Assistance Chatbot Function
def assist_student(query):
    responses = {
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! How can I help you?",
        "greetings": "Greetings! What can I do for you?",
        "help": "Sure, I'm here to help! What do you need assistance with?",
        "course": "I can help you with course recommendations or any queries about your studies. What do you need?",
    }
    default_response = "I'm here to assist you with any questions you have. How can I help?"
    for keyword, response in responses.items():
        if keyword in query.lower():
            return response
    return default_response

# Function to generate course recommendations with images
def generate_recommendations(profile):
    courses = [
        {"name": "Introduction to Machine Learning", "image": "https://via.placeholder.com/150/FF6347/FFFFFF?text=Machine+Learning"},
        {"name": "Data Science Fundamentals", "image": "https://via.placeholder.com/150/4682B4/FFFFFF?text=Data+Science"},
        {"name": "Web Development Bootcamp", "image": "https://via.placeholder.com/150/32CD32/FFFFFF?text=Web+Development"},
        {"name": "Advanced Python Programming", "image": "https://via.placeholder.com/150/FFD700/FFFFFF?text=Python+Programming"},
        {"name": "Digital Marketing Essentials", "image": "https://via.placeholder.com/150/FF4500/FFFFFF?text=Marketing+Essentials"}
    ]
    return courses

# Main function
def main():
    load_dotenv()
    st.set_page_config(page_title="Multi-functional App", page_icon=":books:", layout="wide")
    st.write(css, unsafe_allow_html=True)

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose the mode", ["Home", "PDF Chat", "Student Assistance", "Course Recommendations"])

    if app_mode == "Home":
        st.header("Home Page")
        st.write("Welcome to the multi-functional application. Use the navigation on the left to switch between modes.")

    elif app_mode == "PDF Chat":
        st.header("Chat with multiple PDFs :books:")
        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            handle_userinput(user_question)

        st.sidebar.subheader("Your documents")
        pdf_docs = st.sidebar.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.sidebar.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)

    elif app_mode == "Student Assistance":
        st.header("Student Assistance")
        assist_query = st.text_area("Ask for assistance regarding your studies, college plans, etc.")
        if st.button("Submit Assistance Query"):
            with st.spinner("Generating response..."):
                assist_response = assist_student(assist_query)
                st.write(assist_response)

    elif app_mode == "Course Recommendations":
        st.header("Course Recommendations")
        profile_input = st.text_input("Enter your profile details")
        if st.button("Submit Profile for Recommendations"):
            with st.spinner("Generating recommendations..."):
                recommendations = generate_recommendations(profile_input)
                st.write("Here are some course recommendations based on your profile:")
                for course in recommendations:
                    st.image(course['image'], width=150)
                    st.write(f"**{course['name']}**")

if __name__ == "__main__":
    main()
