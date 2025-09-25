import os
import json
from pathlib import Path
from typing import List
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # or paste directly
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")

client = OpenAI(api_key=OPENAI_API_KEY)

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
    #print("resp==>",resp)
    return [d.embedding for d in resp.data]

# ---- Pinecone setup ----
pc = Pinecone(api_key=PINECONE_API_KEY)
info = pc.describe_index(INDEX_NAME)
print("Index dimension:", info)
if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(INDEX_NAME)
print("index===>",index)
# ---- Indexing ----
doc_path = Path("./docs/api_docs_demo.json")
chunks = load_json_docs(doc_path)
embeddings = embed_texts(chunks)
index.upsert(vectors=[(str(i), embeddings[i], {"text": chunks[i]}) for i in range(len(chunks))])

print(f"Upserted {len(chunks)} chunks into Pinecone.")

# ---- Query ----
def rag_query(question: str, top_k: int = 4) -> str:
    q_emb = embed_texts([question])[0]
    res = index.query(vector=q_emb, top_k=top_k, include_metadata=True)
    contexts = [m["metadata"]["text"] for m in res["matches"]]
    print("contexts===>",contexts)
    return chat_with_context(contexts, question)

def chat_with_context(contexts: list[str], question: str) -> str:
    prompt = f"""Use the following API documentation context to answer:

CONTEXT:
{chr(10).join(contexts)}

QUESTION:
{question}

Answer in a clear, human-readable way, showing API URL, method, query params and example if available.
"""
    print("prompt===>",prompt)
    ans = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return ans.choices[0].message.content

if __name__ == "__main__":
    query = "How to call get ticket API?"
    print("Q:", query)
    print("A:", rag_query(query))
