import ollama

def generate_answer(query, context):

    prompt = f"""
    Answer ONLY from the context below.

    If answer is not present,
    say:
    "I could not find this information."

    Context:
    {context}

    Question:
    {query}
    """

    response = ollama.chat(
        model='phi3',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']