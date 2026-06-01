import chromadb

client = chromadb.PersistentClient(path="./vectordb")

collection = client.get_collection("faq_bot")

data = collection.get(include=["metadatas"])

count = 0

for meta in data["metadatas"]:

    source = meta.get("source", "")

    if "ebixcash-consumer" in source:

        count += 1
        print(source)

print("\nTOTAL CONSUMER CHUNKS:", count)