# streamlit_app.py
import os
import json
from pathlib import Path
from typing import List
import streamlit as st
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()  # Loads environment variables from .env

# ---- Config ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---- Helper Functions ----
def load_json_docs(path: Path) -> List[str]:
    data = json.loads(path.read_text(encoding="utf-8"))

    def flatten(obj, parent=""):
        texts = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                texts.extend(flatten(v, f"{parent}.{k}" if parent else k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                texts.extend(flatten(v, f"{parent}[{i}]"))
        else:
            texts.append(f"{parent}: {obj}")
        return texts

    return flatten(data)

def embed_texts(texts: List[str]) -> List[List[float]]:
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in resp.data]

# ---- Pinecone setup ----
pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(INDEX_NAME)

# ---- Load and index documents ----
doc_path = Path("./docs/api_docs_demo.json")
chunks = load_json_docs(doc_path)

# Only upsert if index is empty
existing_vectors = index.describe_index_stats()["total_vector_count"]
if existing_vectors == 0:
    embeddings = embed_texts(chunks)
    index.upsert(vectors=[(str(i), embeddings[i], {"text": chunks[i]}) for i in range(len(chunks))])
    st.write(f"Upserted {len(chunks)} chunks into Pinecone.")

# ---- RAG Query Functions ----
def rag_query(question: str, top_k: int = 4) -> str:
    q_emb = embed_texts([question])[0]
    res = index.query(vector=q_emb, top_k=top_k, include_metadata=True)
    contexts = [m["metadata"]["text"] for m in res["matches"]]
    return chat_with_context(contexts, question)

def chat_with_context(contexts: list[str], question: str) -> str:
    # Detect if it's API-related question
    if "api" not in question.lower():
        return "I don't know other than API related questions."

    prompt = f"""You are an expert API assistant. 
Your job is to answer in **English** with a small human-readable explanation first, 
then show full technical details in the given format. 
Hide the word "Zoho" from the output (replace with ***).

Answer in this **exact format**:

Answer: <small human readable explanation in English about what this API does.>
API Name: <API Name>
API URL: <Full endpoint URL>
Method: <GET/POST/PUT/DELETE>
Query Params: <comma separated query params or N/A>
Headers:
<Header-Name>: <Header-Value or N/A>
Example Request: <curl example or N/A>
Example Response: <response example or N/A>

CONTEXT:
{chr(10).join(contexts)}

QUESTION:
{question}
"""

    ans = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    # Post-process to hide "Zoho"
    output = ans.choices[0].message.content
    output = output.replace("Zoho", "***")
    return output



# ---- Streamlit App ----
st.title("API Docs Q&A Chatbot")
st.write("Ask questions about your API documentation and get answers.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_question = st.text_input("Enter your question:")

if st.button("Get Answer") and user_question:
    with st.spinner("Generating answer..."):
        answer = rag_query(user_question)
        # Save Q&A in session state
        st.session_state.chat_history.append((user_question, answer))

# ---- Display Chat History ----
for q, a in reversed(st.session_state.chat_history):  # latest on top
    st.markdown(f"**You:** {q}")
    st.markdown("**Answer:**")
    st.markdown(f"```\n{a}\n```")
    st.write("---")
