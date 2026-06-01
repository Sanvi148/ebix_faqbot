import chromadb

URL_TO_DELETE = "https://ebixcash.com/ebixcash-consumer/bus/"

client = chromadb.PersistentClient(path="./vectordb")

collection = client.get_collection("faq_bot")

data = collection.get(include=["metadatas"])

ids_to_delete = []

for id_, meta in zip(data["ids"], data["metadatas"]):

    if meta.get("source") == URL_TO_DELETE:

        ids_to_delete.append(id_)

print(f"Found {len(ids_to_delete)} chunks")

if ids_to_delete:

    collection.delete(ids=ids_to_delete)

    print("Chunks deleted successfully.")

else:

    print("No chunks found for this URL.")