import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llms = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o", temperature=0.5)

promptTemplate = PromptTemplate(
    input_variables = ["bullet_points"],
    template = """
    You are a expert email writer. Using the following bullet points, draft a professional, friendly email:{bullet_points}

    Make sure the email has a greeting, clean structure, and a closing.
    """
)

chain = LLMChain(llm=llms, prompt=promptTemplate)

st.title("Smart Email Writer")

st.write("Enter key bullet points for your email below:")

bullet_points = st.text_area("Bullet Points", height=200)

if st.button("Generate Email"):
    if bullet_points.strip() == "":
        st.warning("Please enter some bullet points")
    else:
        email = chain.run({"bullet_points": bullet_points})
        st.subheader("Drafted Email")
        st.write(email)