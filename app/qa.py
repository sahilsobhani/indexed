from openai import OpenAI

client = OpenAI()

from retriever import search

def ask(question):

    results = search(question)

    context = "\n\n".join(
        chunk["content"] for chunk in results 
    )

    prompt = f"""
    You are a smart codebase assistant.

    Answer the question using only the provided code context

    CODE CONTEXT:
    {context}

    QUESTION OF THE USER:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages = [
            {
                "role":"user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content