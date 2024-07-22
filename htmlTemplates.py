css = """
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex; 
    align-items: center;
}
.chat-message.user {
    background-color: #2b313e;
    color: #fff;
}
.chat-message.bot {
    background-color: #475063;
    color: #fff;
}
.chat-message .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 1rem;
}
.chat-message .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.chat-message .message {
    width: calc(100% - 70px); /* Adjusting width to fit the layout */
}
.stButton>button {
    background-color: #4CAF50; 
    color: white; 
    padding: 12px 24px; 
    border: none; 
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}
.stButton>button:hover {
    background-color: #45a049;
}
.stTextInput>div>div input {
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}
.stTextArea>div>textarea {
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}
.stHeader {
    color: #4CAF50;
    font-family: 'Arial Black', sans-serif;
    text-transform: uppercase;
}
.stSubheader {
    color: #45a049;
    font-family: 'Arial Black', sans-serif;
    text-transform: uppercase;
}
</style>
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png" alt="User Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""
