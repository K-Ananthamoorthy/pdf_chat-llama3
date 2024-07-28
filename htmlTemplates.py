# htmlTemplates.py

css = """
<style>
body {
    font-family: 'Arial', sans-serif;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border-radius: 12px;
}
.stButton>button:hover {
    background-color: white;
    color: black;
    border: 2px solid #4CAF50;
}
.chat-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 70vh;
    overflow-y: auto;
    padding: 10px;
    border-radius: 10px;
    background-color: #f0f2f6;
}
.chat-message {
    display: flex;
    align-items: flex-start;
    margin: 10px 0;
}
.chat-message.user {
    justify-content: flex-end;
}
.chat-message.bot {
    justify-content: flex-start;
}
.chat-bubble {
    max-width: 60%;
    padding: 10px;
    border-radius: 10px;
    font-size: 14px;
}
.chat-bubble.user {
    background-color: #dcf8c6;
    color: #333;
}
.chat-bubble.bot {
    background-color: #ececec;
    color: #333;
}
</style>
"""

bot_template = """
<div class="chat-message bot">
    <div class="chat-bubble bot">
        {{MSG}}
    </div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="chat-bubble user">
        {{MSG}}
    </div>
</div>
"""
