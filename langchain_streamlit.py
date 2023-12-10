import requests
import random

import streamlit as st


st.set_page_config(page_title="Conversational Form", page_icon="📖")
st.title("📖 Conversational Form")

assistant_greeting = [
    "Hello! How can I assist you today?",
    "Hi! Is there anything I can help you with?",
    "It is a great day today, how may I help you?",
]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.chat_message("ai").write(random.choice(assistant_greeting))

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    assistant_data = ""
    # Add user message to chat history
    st.chat_message("human").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Loading.."):
        response = requests.post(
            "http://localhost:8000/chat", params={"text_input": prompt}
        )
        assistant_status = response.status_code

        if assistant_status == 412:
            warning_content = "Injection detected!"
            st.chat_message("ai", avatar="🚨").warning(warning_content)
            st.session_state.messages.append(
                {"role": "assistant", "content": warning_content}
            )

        else:
            assistant_data = response.json()
            st.chat_message("ai").write(assistant_data)

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_data}
            )
