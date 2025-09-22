# Install dependencies first (if not installed)
# pip install chromadb langchain-community langchain-huggingface
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ---------- Step 1: Define your text data ----------
texts = [
    "Python is a best language for AI",
    "This Course is for full beginners",
    "This will teach you all about the GenAI"
]

# ---------- Step 2: Create embeddings ----------
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ---------- Step 3: Create and store in Chroma ----------
vectorstore = Chroma.from_texts(
    texts, 
    embedding_model, 
    persist_directory="chroma_db"  # saves locally
)

print("✅ Texts stored as vectors in Chroma!")

# Save to local disk
vectorstore.persist()

# ---------- Step 4: Test a similarity search ----------
query = "Which language is good for AI?"
results = vectorstore.similarity_search(query, k=1)

print("\n🔎 Query Result:")
for res in results:
    print(f"- {res.page_content}")