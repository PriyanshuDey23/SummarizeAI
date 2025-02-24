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
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Function to generate summary
def generate_summary(input_text, tone, word_count):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-8b", temperature=1, api_key=GOOGLE_API_KEY
    )

    prompt = PromptTemplate(
        input_variables=["text", "tone", "word_count"],
        template=PROMPT,
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    return llm_chain.run({"text": input_text, "tone": tone, "word_count": word_count})

# Streamlit Page Config
st.set_page_config(page_title="Text Summarizer", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
        .stTextArea textarea { font-size: 14px !important; }
        .stDownloadButton button { width: 100%; }
        .css-18e3th9 { padding-top: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("📖 AI-Powered Text Summarizer")

# Tabs for Input Options
tab1, tab2, tab3 = st.tabs(["✍️ Text Input", "🔗 URL Input", "📄 PDF Upload"])

# Variables for input text
user_input = None
input_type = None

# Text Input Tab
with tab1:
    text = st.text_area("Enter your text", height=200)
    if text:
        user_input = text
        input_type = "Text"

# URL Input Tab
with tab2:
    url = st.text_input("Enter a URL")
    if url:
        user_input = extract_text_from_url(url)
        input_type = "URL"

# PDF Upload Tab
with tab3:
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        user_input = extract_text_from_pdf(uploaded_file)
        input_type = "PDF"

# Display Extracted Text if Available
if user_input:
    st.markdown(f"### Extracted Text from **{input_type}**")
    st.text_area("Preview", user_input, height=200)

# Parameter Selection
st.subheader("⚙️ Summarization Settings")
col1, col2 = st.columns([1, 1])

with col1:
    tone = st.selectbox("Select Tone", ["Formal", "Informal", "Friendly", "Professional"])

with col2:
    word_count = st.text_input("Word Count", placeholder="Enter a number")

# Summarization Button
if st.button("⚡ Generate Summary"):
    if not user_input:
        st.warning("❌ Please provide input (Text, URL, or PDF).")
    elif not word_count.isdigit():
        st.warning("❌ Please enter a valid word count.")
    else:
        with st.spinner("Generating summary... ⏳"):
            response = generate_summary(input_text=user_input, tone=tone, word_count=word_count)

        st.success("✅ Summary generated successfully!")
        st.subheader("📝 Summary:")
        st.write(response)

        # Download Buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📄 Download as TXT",
                data=convert_to_txt(response),
                file_name="summarized_text.txt",
                mime="text/plain",
            )
        with col2:
            st.download_button(
                label="📂 Download as DOCX",
                data=convert_to_docx(response),
                file_name="summarized_text.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
