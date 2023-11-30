import requests

import streamlit as st


st.set_page_config(page_title="Conversational Form", page_icon="📖")
st.title("📖 Conversational Form")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    # Add user message to chat history
    st.chat_message("human").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = requests.post(
        "http://localhost:8000/chat", params={"text_input": prompt}
    ).json()
    st.chat_message("ai").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
