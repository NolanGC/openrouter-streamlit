import openai
import streamlit as st
from streamlit_chat import message
from components.Sidebar import sidebar

api_key = sidebar()

st.title("💬 Streamlit GPT")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to say?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=i)

if user_input and not api_key:
    st.info("Please add your OpenAI API key to continue.")

if user_input and api_key:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    openai.api_base = "https://openrouter.ai/api/v1"
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="openai/gpt-3.5-turbo",
        messages=st.session_state.messages,
        headers={"HTTP-Referer": "https://yourdomain.streamlit.io"},
    )
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    message(msg.content)
