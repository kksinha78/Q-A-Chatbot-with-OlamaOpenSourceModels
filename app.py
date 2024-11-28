import streamlit as st
from langchain_community import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q & A Chatbot with Ollama"

## Define Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant.Pleasde responce to the user queries"),
        ("user","Question:{question}")
    ]
)
def generate_response(question,engine,temperature,max_tokens):
    
    engine=Ollama(model = engine) # Ollama is a platform, which facilates to use open sourse modelsOpen sourse model(eg- Gemma2,Llama3 etc..) must be installed in system before it is callled
    output_parser = StrOutputParser()
    chain = prompt | engine | output_parser
    answer = chain.invoke({'question':question})
    return answer

#Title of the app
st.title("Q&A Chatbot with OpenAI")

st.sidebar.title("Settings")

## Dropdown to select various Open AI models
engine = st.sidebar.selectbox("Select an Open AI Model",["mistral"])

#Adjust reposonse parameter

temperature = st.sidebar.slider("Temperature",min_value = 0.0,max_value = 1.0,value = 0.7)
max_tokens = st.sidebar.slider("Max Tokens",min_value = 50,max_value = 300,value = 150) # default = 150

## Define Main interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")


