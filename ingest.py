from scraper.crawl_urls import get_all_urls
from scraper.extract_content import extract_main_content
from scraper.clean_text import clean_text

from processing.chunking import chunk_text
from processing.embeddings import generate_embeddings
from processing.duplicate import remove_duplicates
from processing.store_vector_db import store_chunks

BASE_URL = "https://ebixcash.com/"

def ingestion_pipeline():
    """"Runs complete website ingestion pipeline"""

    print("\n Starting Website Crawling...\n")
    urls=get_all_urls(BASE_URL)
    print(f" Total URLs Found: {len(urls)}\n")
    all_chunks=[]
    for url in urls:
        try:
            print(f" Processing: {url}")
            text=extract_main_content(url)
            if not text:
                continue
            # Clean text
            cleaned_text=clean_text(text)
            # Chunking
            chunks=chunk_text(cleaned_text)
            #add all chunks
            all_chunks.extend(chunks)
        except Exception as e:
            print(f" Error processing {url}: {e}")
    print(f"\n Total Chunks Created: {len(all_chunks)}\n")

    #generate embeddings
    print("\nGenerating Embeddings...\n")
    embeddings = generate_embeddings(all_chunks)
    #remove duplicates
    print("\nRemoving redundant chunks...\n")
    unique_chunks, unique_embeddings = remove_duplicates(all_chunks, embeddings)
    print(f"\n Unique Chunks after deduplication: {len(unique_chunks)}\n")
    #store in vector db
    print("\nStoring chunks in vector database...\n")
    store_chunks(unique_chunks, unique_embeddings)
    print("\n Ingestion Pipeline Completed Successfully!\n")
if __name__ == "__main__":
    ingestion_pipeline()    