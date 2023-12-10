from fastapi import FastAPI, Request, status, Response
from pathlib import Path

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import streamlit as st
from langchain.chat_models import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()

# Add prompt injection detection

from rebuff import Rebuff

rebuff_api_key = os.environ["REBUFF_API_KEY"]

rb = Rebuff(api_token=rebuff_api_key, api_url="https://www.rebuff.ai")


@st.cache_resource
def load_conv_model():
    hf = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
    return hf


app = FastAPI(title="Conversational Form")

template = """The following is a friendly conversation between a human and an AI. The AI is helpful and provides lots of specific details from its context. While helping the human, the AI side by side ask the human, his/her details like name, email, city of residence, phone number and age. The AI will ask one personal detail at a time. If the human hesitates to share information, the AI will not force the user to share their details, and will complete the help to them, and also assure the human of their concerns. If the AI does not know the answer to a question, it truthfully says it does not know. 

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
llm = load_conv_model()
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)


@app.get("/")
def read_root(request: Request):
    return {"message": "Welcome to Formless AI!"}


@app.post("/chat")
def conversational_form(text_input: str, response: Response):
    is_injection = rb.detect_injection(text_input)
    assistant_response = conversation.run(input=text_input)
    response.status_code = status.HTTP_200_OK

    if is_injection.injectionDetected:
        print("is_injection: " + str(is_injection))
        print(
            "is_injection.vectorScore.get: "
            + str(is_injection.vectorScore.get("topScore"))
        )
        if is_injection.vectorScore.get("topScore") > 0.8:
            response.status_code = status.HTTP_412_PRECONDITION_FAILED
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
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
