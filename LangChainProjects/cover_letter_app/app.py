# app.py

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API Key not found. Please set it in your .env file as OPENAI_API_KEY.")
    st.stop()
# Initialize LLM with API Key
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0.7)
    

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["resume", "company", "role"],
    template="""
        You are a professional career consultant. 
        Based on the following resume and job details, write a tailored cover letter.

        Resume:
        {resume}

        Job Role: {role}
        Company: {company}

        Cover Letter:
        """
    )
# Create Chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# --- Function to extract text from PDF ---
def extract_text_from_pdf(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    else:
        st.error("Unsupported file type.")
        return ""

# --- Streamlit UI ---
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📄")

st.title("📄 AI Cover Letter Generator")
st.write("Upload your resume and enter job details to generate a personalized cover letter.")

# Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# Company and Role Inputs
company_name = st.text_input("Company Name")
job_role = st.text_input("Job Role")

# Generate Button
if st.button("Generate Cover Letter"):
    if uploaded_file and company_name and job_role:
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if resume_text:
            # Generate Output
            with st.spinner("Generating your cover letter..."):
                cover_letter = chain.run({
                    "resume": resume_text,
                    "company": company_name,
                    "role": job_role
                })

            st.subheader("✉️ Generated Cover Letter")
            st.write(cover_letter)

            # Option to Download
            st.download_button(
                label="📥 Download Cover Letter",
                data=cover_letter,
                file_name="cover_letter.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please upload a resume and fill all fields.")
