import chromadb
client=chromadb.PersistentClient(path="./vectordb")
import uuid
# try:
#     client.delete_collection("faq_bot")
# except:
#     pass

collection = client.get_or_create_collection(
    name="faq_bot"
)


def store_chunks(chunks, embeddings,metadatas):

    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]

    collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
)

    print("\nChunks stored successfully.")
    