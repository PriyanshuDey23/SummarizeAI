from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *


# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Response Format For my LLM Model
def Summarization_chain(input_text, tone, word_count):
    # Define the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002", temperature=1, api_key=GOOGLE_API_KEY)  
    
    # Define the prompt
    PROMPT_TEMPLATE = PROMPT  # Imported
    prompt = PromptTemplate(
            input_variables=["text", "tone", "word_count"], # input in prompt
            template=PROMPT_TEMPLATE,
        )
      
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate response
    response = llm_chain.run({"text": input_text, "tone": tone, "word_count": word_count})
    return response


# Streamlit app
st.set_page_config(page_title="Text Summarizer")
st.header("Text Summarizer")

# Input text
text = st.text_area("Enter your text", height=200)

# Parameters
column_1, column_2 = st.columns([5, 5])

# Tone selection
with column_1:
    tone = st.selectbox("Select the tone", ["Formal", "Informal", "Friendly", "Professional"])

# Word count selection
with column_2:
    word_count = st.text_input("Number Of Words")

# Summarize button
if st.button("Summarize"):
    if text and word_count.isdigit():
        response = Summarization_chain(input_text=text, tone=tone, word_count=word_count)
        st.write("The Summary is: \n \n ", response)
    else:
        st.warning("Please enter text and a valid number of words.")
