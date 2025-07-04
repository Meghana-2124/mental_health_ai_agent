# mental_health_agent.py

import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from textblob import TextBlob  # For optional sentiment analysis

# Load AI model (Mistral via Ollama)
llm = OllamaLLM(model="gemma:2b")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# Define mental wellness prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""
You are a compassionate AI mental wellness assistant named MindEase. Your job is to support users emotionally, help them manage stress, and suggest calming activities.

Respond with empathy, kindness, and calm language.

Previous conversation:
{chat_history}
User: {question}
MindEase:
"""
)

# Function to run AI response with memory
def run_chain(question):
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages]
    )
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

    # Store interaction in memory
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)

    return response

# Streamlit UI
st.set_page_config(page_title="Mental Health Check-In", page_icon="🧠")
st.title("🧠 MindEase: Mental Health Check-In Assistant")
st.write("💬 I'm here to support you. Let's talk. You can type how you're feeling or choose a prompt below.")

# Suggestion buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🌥️ I'm feeling anxious"):
        user_input = "I'm feeling anxious today. Can you help?"
    elif st.button("📖 I need motivation"):
        user_input = "Can you give me a motivational quote?"

with col2:
    if st.button("💤 Trouble sleeping"):
        user_input = "I'm having trouble sleeping. Any advice?"
    elif st.button("🧘 Suggest a calming exercise"):
        user_input = "Suggest a calming breathing or grounding exercise."

# Custom text input
user_text = st.text_input("✍️ Or share how you're feeling:")
if user_text:
    user_input = user_text

# Process user input
if "user_input" in locals():
    # Optional Sentiment Analysis
    sentiment = TextBlob(user_input).sentiment.polarity
    if sentiment < -0.2:
        st.info("🧘 It sounds like you're feeling a bit low. I'm here to help!")

    response = run_chain(user_input)
    st.write(f"🙋 **You:** {user_input}")
    st.write(f"🤖 **MindEase:** {response}")

# Chat History
st.subheader("📝 Chat History")
for msg in st.session_state.chat_history.messages:
    emoji = "🙋" if msg.type == "human" else "🤖"
    st.write(f"{emoji} **{msg.type.capitalize()}:** {msg.content}")

# Optional download button for wellness log
if st.button("📥 Download Wellness Log"):
    with open("wellness_log.txt", "w") as f:
        for msg in st.session_state.chat_history.messages:
            f.write(f"{msg.type.capitalize()}: {msg.content}\n")
    st.success("🗒️ Wellness log saved to 'wellness_log.txt'.")
