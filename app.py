
from retrieval.retrieve import retrieve_chunks
from retrieval.qa_chain import generate_answer
from retrieval.cache import (
    get_cached_answer,
    store_answer
)
def chatbot():
    """
    Runs FAQ chatbot loop.
    """

    print("\n FAQ Bot Ready!")
    print("Type 'exit' to stop.\n")
    while True:
        query=input("Ask Question:")
        if query.lower()=="exit":
            print("Goodbye!")
            break
        
        try:
            cached_answer = get_cached_answer(query)

            if cached_answer:

                print("\n Cached Answer:\n")
                print(cached_answer)

                print("\n" + "-" * 60 + "\n")

                continue
            #retrieve rellevant chunks
            retrieved_chunks=retrieve_chunks(query)
            context="\n\n".join(retrieved_chunks)
            answer=generate_answer(query, context)
            store_answer(query, answer)
            print("RETREIVED CHUNKS:      " ,retrieved_chunks) 
            
            print(f"\nAnswer:\n{answer}\n")
            print("\n" + "-" * 60 + "\n")
        except Exception as e:
            print(f"Error: {e}")
if __name__ == "__main__":
    chatbot()
