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
import difflib

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

# Improved Student Assistance Chatbot Function with Memory
def assist_student(query, memory):
    responses = {
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! How can I help you?",
        "greetings": "Greetings! What can I do for you?",
        "help": "Sure, I'm here to help! What do you need assistance with?",
        "course": "I can help you with course recommendations or any queries about your studies. What do you need?",
        "fees": "For fee details, please visit the college website or contact the admissions office.",
        "schedule": "The class schedules are available on the student portal. You can also check with your department office.",
        "admission": "For admission inquiries, please visit our admissions page or contact the admissions office directly.",
        "exam": "Exam schedules and details can be found on the exam portal. Make sure to check it regularly.",
    }
    default_response = "I'm here to assist you with any questions you have. How can I help?"
    for keyword, response in responses.items():
        if difflib.SequenceMatcher(None, keyword, query.lower()).ratio() > 0.6:
            memory.save_context({"user": query}, {"assistant": response})
            return response
    memory.save_context({"user": query}, {"assistant": default_response})
    return default_response

def generate_recommendations(profile):
    courses = [
        {
            "name": "Introduction to Machine Learning",
            "image": "https://plus.unsplash.com/premium_photo-1682124651258-410b25fa9dc0?q=80&w=1921&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "description": "Learn the basics of machine learning with hands-on projects and real-world applications. Understand supervised and unsupervised learning techniques.",
            "rating": 4.7,
            "duration": "6 weeks",
            "instructor": "Andrew Ng",
            "link": "https://www.coursera.org/learn/machine-learning"
        },
        {
            "name": "Data Science Fundamentals",
            "image": "https://images.unsplash.com/photo-1599658880436-c61792e70672?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "description": "Explore the core concepts of data science, including data manipulation, analysis, and visualization using Python and R.",
            "rating": 4.5,
            "duration": "8 weeks",
            "instructor": "Emily Fox",
            "link": "https://www.coursera.org/specializations/data-science"
        },
        {
            "name": "Full Stack Web Development Bootcamp",
            "image": "https://images.unsplash.com/photo-1629904853893-c2c8981a1dc5?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "description": "Become a full-stack web developer with this comprehensive bootcamp covering HTML, CSS, JavaScript, Node.js, and more.",
            "rating": 4.8,
            "duration": "12 weeks",
            "instructor": "Colt Steele",
            "link": "https://www.udemy.com/course/the-web-developer-bootcamp/"
        },
        {
            "name": "Advanced Python Programming",
            "image": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "description": "Deepen your understanding of Python with advanced topics such as decorators, generators, and context managers. Solve real-world coding challenges.",
            "rating": 4.6,
            "duration": "10 weeks",
            "instructor": "Jose Portilla",
            "link": "https://www.udemy.com/course/advanced-python/"
        },
        {
            "name": "Digital Marketing Essentials",
            "image": "https://plus.unsplash.com/premium_photo-1683872921964-25348002a392?q=80&w=1935&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "description": "Master the fundamentals of digital marketing, including SEO, content marketing, social media marketing, and email marketing.",
            "rating": 4.4,
            "duration": "4 weeks",
            "instructor": "Neil Patel",
            "link": "https://www.udemy.com/course/digital-marketing-masterclass/"
        }
    ]
    return courses

#main-function
def main():
    load_dotenv()
    st.set_page_config(page_title="Multi-functional App", page_icon=":books:", layout="wide")
    st.write(css, unsafe_allow_html=True)

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "assist_memory" not in st.session_state:
        st.session_state.assist_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    if "profile" not in st.session_state:
        st.session_state.profile = None

    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose the mode", ["Home", "Chat with multiple PDFs", "Student Assistance", "Course Recommendations"])

    if app_mode == "Home":
        st.header("Home Page :house:")
        st.markdown("""
        <div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px;">
            <h2 style="color:#333;">Welcome to the Multi-functional Application</h2>
            <p style="color:#555;">Use the navigation on the left to switch between modes.</p>
            <p style="color:#555;">This app provides the following features:</p>
            <ul style="color:#555;">
                <li>Chat with multiple PDFs</li>
                <li>Student Assistance Chatbot</li>
                <li>Course Recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.profile is None:
            with st.form("profile_form"):
                st.subheader("Fill in your details")
                name = st.text_input("Name")
                branch = st.text_input("Branch")
                usn = st.text_input("USN")
                programming_languages = st.text_input("Known Programming Languages")
                interests = st.text_input("Interests")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email")
                submitted = st.form_submit_button("Submit")

                if submitted:
                    st.session_state.profile = {
                        "Name": name,
                        "Branch": branch,
                        "USN": usn,
                        "Programming Languages": programming_languages,
                        "Interests": interests,
                        "Phone Number": phone,
                        "Email": email
                    }
                    st.success("Profile saved successfully!")

        if st.session_state.profile is not None:
            st.subheader("Your Profile")
            st.write(f"**Name:** {st.session_state.profile['Name']}")
            st.write(f"**Branch:** {st.session_state.profile['Branch']}")
            st.write(f"**USN:** {st.session_state.profile['USN']}")
            st.write(f"**Programming Languages:** {st.session_state.profile['Programming Languages']}")
            st.write(f"**Interests:** {st.session_state.profile['Interests']}")
            st.write(f"**Phone Number:** {st.session_state.profile['Phone Number']}")
            st.write(f"**Email:** {st.session_state.profile['Email']}")

    elif app_mode == "Chat with multiple PDFs":
        st.header("Chat with multiple PDFs :books:")
        pdf_docs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
        if pdf_docs is not None and len(pdf_docs) > 0:
            if st.button("Process"):
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success("Processing completed successfully!")

        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            handle_userinput(user_question)

    elif app_mode == "Student Assistance":
        st.header("Student Assistance Chatbot :robot_face:")
        user_query = st.text_input("Ask your query:")

        if user_query:
            response = assist_student(user_query, st.session_state.assist_memory)
            st.write(user_template.replace("{{MSG}}", user_query), unsafe_allow_html=True)
            st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)

    elif app_mode == "Course Recommendations":
        st.header("Course Recommendations :mortar_board:")
        if st.session_state.profile is None:
            st.warning("Please fill in your profile details on the Home page first.")
        else:
            courses = generate_recommendations(st.session_state.profile)
            for course in courses:
                st.image(course["image"], width=150)
                st.write(f"### {course['name']}")
                st.write(f"**Description:** {course['description']}")
                st.write(f"**Rating:** {course['rating']} :star:")
                st.write(f"**Duration:** {course['duration']}")
                st.write(f"**Instructor:** {course['instructor']}")
                st.markdown(f"[Enroll Now]({course['link']})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
