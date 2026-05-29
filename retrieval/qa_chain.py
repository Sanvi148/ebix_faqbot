import ollama

def generate_answer(query, context):

    prompt = f"""
    You are a helpful assistant.

    Answer ONLY from the provided context.

    If the answer exists in context, provide it directly.

    Do NOT refuse.
    Do NOT say you lack information.
    Do NOT mention policies.

    Context:
    {context}

    Question:
    {query}

    Answer:
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