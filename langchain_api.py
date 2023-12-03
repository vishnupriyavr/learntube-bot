from fastapi import FastAPI, Request, status, Response
from pathlib import Path

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
)
import streamlit as st
from langchain.chat_models import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()

# Add prompt injection detection

from rebuff_test import Rebuff

rebuff_api_key = os.environ["REBUFF_API_KEY"]

rb = Rebuff(api_token=rebuff_api_key, api_url="https://www.rebuff.ai")


@st.cache_resource
def load_conv_model():
    hf = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
    return hf


app = FastAPI(title="Conversational Form")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a data gathering assistant.Your task is to collect all the user details of name, email, city of residence, phone number and age. Ask one personal detail at a time. If the user hesitates to share information, divert to small talk or different topics, assure them of their concerns. With each user input, find out the sentiment of the user input, and reply adapting to the mood of the user. If all the personal details are answered then thank them and ask how you can help them.",
        ),
        ("human", "{question}"),
    ]
)
memory = ConversationBufferMemory()
# view_messages = st.expander("View the message contents in session state")

llm = load_conv_model()
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)


@app.get("/")
def read_root(request: Request):
    return {"message": "Welcome to Formless AI!"}


@app.post("/chat")
def conversational_form(text_input: str, response: Response):
    is_injection = rb.detect_injection(text_input)
    response.status_code = status.HTTP_200_OK
    assistant_response = llm_chain.run(question=text_input)

    if is_injection.injectionDetected:
        response.status_code = status.HTTP_412_PRECONDITION_FAILED
        return response
    else:
        return assistant_response


if __name__ == "__main__":
    import uvicorn  # pylint: disable=import-outside-toplevel

    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        use_colors=True,
        reload=True,
    )
