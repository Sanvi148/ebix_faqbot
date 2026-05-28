from sklearn.metrics.pairwise import cosine_similarity
THRESHOLD=0.90
def remove_duplicates(chunks,embeddings,metadatas):
    unique_chunks=[]
    unique_embeddings=[]
    unique_metadatas = []
    for i,emb in enumerate(embeddings):
        duplicate=False
        for existing_emb in unique_embeddings:
            similarity=cosine_similarity([emb],[existing_emb])[0][0]
            if similarity>THRESHOLD:
                duplicate=True
                break
        if not duplicate:
            unique_chunks.append(chunks[i])
            unique_embeddings.append(emb)
            unique_metadatas.append(metadatas[i])
    return unique_chunks, unique_embeddings, unique_metadatas