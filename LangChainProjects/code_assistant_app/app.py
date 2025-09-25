import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llms = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o", temperature=0.5)

promptTemplate = PromptTemplate(
    input_variables = ["code_task"],
    template = """
    You are a professional coding assistant. Help the user with the following task : {code_task}
    Provide clean, well-commented code and explanations if needed.
    """
)

chain = LLMChain(llm=llms, prompt=promptTemplate)

st.title("Code Assistant")

code_task = st.text_area("Describe your coding task:")

if st.button("Generate Code"):
    if code_task.strip() == "":
        st.warning("Please enter a task description.")
    else:
        response = chain.run({"code_task": code_task})
        st.subheader("Assistant Response")
        st.code(response, language="python")