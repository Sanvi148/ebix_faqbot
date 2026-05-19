
from retrieval.retrieve import retrieve_chunks
from retrieval.qa_chain import generate_answer
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
            #retrieve rellevant chunks
            retrieved_chunks=retrieve_chunks(query)
            #convert chunks to context and generate answer
            context="\n".join(retrieved_chunks)
            answer=generate_answer(query, context)
            print(f"\nAnswer:\n{answer}\n")
            print("\n" + "-" * 60 + "\n")
        except Exception as e:
            print(f"Error: {e}")
if __name__ == "__main__":
    chatbot()
