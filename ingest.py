from scraper.crawl_urls import get_all_urls
from scraper.extract_content import extract_content
from scraper.clean_text import clean_text
import os
from processing.chunking import chunk_text
from processing.embeddings import generate_embeddings
from processing.deduplicate import remove_duplicates
from processing.store_vector_db import store_chunks
from processing.store_vector_db import collection

BASE_URL = "https://ebixcash.com/"
def ingestion_pipeline():
    """Runs complete website ingestion pipeline"""
    os.makedirs("data", exist_ok=True)

    raw_file = open("data/raw_chunks.txt", "a", encoding="utf-8")
    clean_file = open("data/cleaned_chunks.txt", "a", encoding="utf-8")
    print("\n Starting Website Crawling...\n")
    urls = ["https://ebixcash.com/ebixcash-business/agent-assisted-model/"]
    print(f" Total URLs Found: {len(urls)}\n")
    all_chunks=[]
    all_metadata = []
    for url in urls:
        try:
            print(f"Deleting old chunks for: {url}")

            collection.delete(
                where={"source": url}
            )
            print(f" Processing: {url}")
            chunks=extract_content(url)
            if not chunks:
                print("No chunks extracted!")
                continue
            print("\nTOTAL RAW CHUNKS:", len(chunks))

            for chunk in chunks:
                if "Offer Title" in chunk:
                    print("\n===== OFFER CHUNK FOUND =====")
                    print(chunk)
            if not chunks:
                continue
            for chunk in chunks:
                raw_file.write(f"\n\n{'='*80}\n")
                raw_file.write(f"URL: {url}\n\n")
                raw_file.write(chunk)
                # Clean text
                cleaned_chunk=clean_text(chunk)
                clean_file.write(f"\n\n{'='*80}\n")
                clean_file.write(f"URL: {url}\n\n")
                clean_file.write(cleaned_chunk)
                # Chunking
                if len(cleaned_chunk) > 1000:
                    final_chunks = chunk_text(cleaned_chunk)
                else:
                    final_chunks = [cleaned_chunk]
                #add all chunks
                all_chunks.extend(final_chunks)
                for _ in final_chunks:

                    all_metadata.append({
                        "source": url
                    })
        except Exception as e:
            print(f" Error processing {url}: {e}")
    print(f"\n Total Chunks Created: {len(all_chunks)}\n")
    if not all_chunks:
        print("No chunks generated. Exiting.")
        return
    #generate embeddings
    print("\nGenerating Embeddings...\n")
    embeddings = generate_embeddings(all_chunks)
    #remove duplicates
    print("\nRemoving redundant chunks...\n")
    unique_chunks, unique_embeddings, unique_metadatas = remove_duplicates(all_chunks, embeddings, all_metadata)
    print(f"\n Unique Chunks after deduplication: {len(unique_chunks)}\n")
    #store in vector db
    print("\nStoring chunks in vector database...\n")
    print(
    "Collection count BEFORE storing:",
    collection.count()
)
    store_chunks(unique_chunks, unique_embeddings ,unique_metadatas)
    print(
    "Collection count AFTER storing:",
    collection.count()
)
    print("\n Ingestion Pipeline Completed Successfully!\n")    
    raw_file.close()
    clean_file.close()
if __name__ == "__main__":
    ingestion_pipeline()    

    