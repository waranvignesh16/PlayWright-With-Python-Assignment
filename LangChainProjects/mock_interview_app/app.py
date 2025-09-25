import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API Key not found. Please set it in your .env file as OPENAI_API_KEY.")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(page_title="AI Mock Interview Generator", page_icon="🎤")

st.title("🎤 AI Mock Interview Generator")
st.write("Provide a Job Role and Job Description to generate realistic Mock Interview Q&A.")

# Inputs
job_role = st.text_input("Job Role (e.g., Frontend Developer)")
job_description = st.text_area("Job Description (Paste the JD here)")

# Button
if st.button("Generate Mock Interview"):
    if job_role and job_description:

        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=OPENAI_API_KEY)

        # Prompt Template
        prompt_template = PromptTemplate(
            input_variables=["role", "jd"],
            template="""
                You are an expert technical interviewer.  
                Generate a set of **mock interview Q&A** for the given role and job description.  
                Include:
                    - At least 8 technical and behavioral questions.  
                    - Provide concise and professional sample answers.  

                Job Role: {role}  
                Job Description: {jd}  

                Mock Interview (Q&A format):
                """
        )

        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Generate
        with st.spinner("Generating Mock Interview..."):
            mock_interview = chain.run({"role": job_role, "jd": job_description})

        # Output
        st.subheader("📝 Mock Interview Q&A")
        st.write(mock_interview)

        # Download
        st.download_button(
            label="📥 Download Mock Interview",
            data=mock_interview,
            file_name="mock_interview.txt",
            mime="text/plain"
        )

    else:
        st.warning("⚠️ Please enter both Job Role and Job Description.")
