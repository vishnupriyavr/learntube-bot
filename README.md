# learntube-bot

Advanced conversational chatbot for data gathering and deployment

# Implementations:

- Constructed an AI flow that asks for the personal details of the user like name, email, city of residence, phone number and age, using LangChain.
- Handled the scenario of the chatbot taking a proactive approach, initiating interactions and adeptly transitioning into small talk or different topics when users hesitate to share details.
- Created a backend for the same to be used as a service with REST APIs for the bot flow, using FastAPI
- Created a frontend for the same to be used as a chat app, for seamless conversation between user and assistant, using Streamlit.
- [UPDATE] Created a function to combat prompt injection.

# Frameworks used:

- Langchain
- FastAPI
- Streamlit

# Run UI and API for the bot

FastAPI based REST endpoint:

```
python langchain_api.py
```

Streamlit based Chat UI:

```
streamlit run langchain_streamlit.py
```

# WIP:

- Sentiment Analysis / Multi-lingual support

# Demo

https://github.com/vishnupriyavr/learntube-bot/assets/55908719/e5294a02-1f87-459a-aae6-a02279792c2f

# [UPDATE] Prompt Injection Demo


https://github.com/vishnupriyavr/learntube-bot/assets/55908719/176cd7fd-d9bf-4f64-a822-858cf41935e3


