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
    print("\n========== USER QUERY ==========\n")
    print(query)
    query_embedding = model.encode([query])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=20
    )
    all_chunks = results["documents"][0]
    distances = results["distances"][0]
    print("\n========== ALL MATCHED CHUNKS ==========\n")

    for i, (chunk, distance) in enumerate(zip(all_chunks, distances)):

        print(f"\n----- Matched Chunk {i+1} -----\n")
        print("Similarity Distance:", distance)
        print("\nChunk Text:\n")
        print(chunk)
        print("\n" + "=" * 70)
    top_2_chunks = all_chunks[:2]

    print("\n========== TOP 2 CHUNKS SELECTED ==========\n")

    for i, chunk in enumerate(top_2_chunks):
        print(f"\n---- Top Chunk {i+1} -----\n")
        print(chunk)
        print("\n" + "=" * 70)

    return top_2_chunks