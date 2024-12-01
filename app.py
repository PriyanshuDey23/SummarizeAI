from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *
from utils import *

# Load environment variables
load_dotenv()

# Access API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Summarization chain function
def generate_summary(input_text, tone, word_count):

    # Initialize the LLM model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-8b", temperature=1, api_key=GOOGLE_API_KEY
    )

    # Set up the prompt template
    prompt = PromptTemplate(
        input_variables=["text", "tone", "word_count"],
        template=PROMPT,  # Imported from prompt.py
    )

    # Create the LLM chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate and return the response
    return llm_chain.run({"text": input_text, "tone": tone, "word_count": word_count})

# Consolidated input handling function
def get_input_data():

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    url = st.text_input("Enter a URL")
    text = st.text_area("Enter your text", height=200)

    # Handle PDF input
    if uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
        input_type = "PDF"
    # Handle URL input
    elif url:
        extracted_text = extract_text_from_url(url)
        input_type = "URL"
    # Handle direct text input
    elif text:
        extracted_text = text
        input_type = "Text"
    else:
        extracted_text = None
        input_type = None

    return extracted_text, input_type

# Streamlit App UI
st.set_page_config(page_title="Text Summarizer")
st.header("Text Summarizer")

# Get user input (file, URL, or direct text)
user_input, input_type = get_input_data()

# Display extracted or entered text
if user_input:
    st.text_area(f"Extracted Text from {input_type}", user_input, height=200)

# Parameters for summarization (tone and word count)
column_1, column_2 = st.columns([5, 5])

with column_1:
    tone = st.selectbox("Select the tone", ["Formal", "Informal", "Friendly", "Professional"])

with column_2:
    word_count = st.text_input("Number of Words")

# Summarize button action
if st.button("Summarize"):
    response = generate_summary(input_text=user_input, tone=tone, word_count=word_count)
    st.subheader("The Summary is:")
    st.write(response)

    # Download options
    st.download_button(
            label="Download as TXT",
            data=convert_to_txt(response),
            file_name="summarized_text.txt",
            mime="text/plain",
        )
    st.download_button(
            label="Download as DOCX",
            data=convert_to_docx(response),
            file_name="summarized_text.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        

