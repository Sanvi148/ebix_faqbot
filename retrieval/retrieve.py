from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

client = chromadb.PersistentClient(
    path="./vectordb"
)

collection = client.get_collection("faq_bot")
def retrieve_chunks(query):
    query_embedding = model.encode([query])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2
    )
    return results["documents"][0]