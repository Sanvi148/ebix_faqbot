import chromadb
client=chromadb.PersistentClient(path="./vectordb")
collection=client.get_or_create_collection(
    name="faq_bot"
)
def store_chunks(chunks,embeddings):
    ids=[str(i) for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )
    