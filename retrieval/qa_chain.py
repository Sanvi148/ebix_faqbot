import ollama

def generate_answer(query, context):

    prompt = f"""
    You are an FAQ assistant.

    Use ONLY the information present in the provided context.

    Rules:
    1. Answer directly from the context.
    2. Do not make up information.
    3. Do not add assumptions.
    4. If the context contains the answer, provide it clearly and completely.
    5. If multiple relevant items are present, list all of them.
    6. If the answer is not found in the context, reply:
    "I could not find this information in the available data."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']