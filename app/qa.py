from openai import OpenAI

client = OpenAI()

from retriever import search

def ask(question):
    question = question[:1000]
    results = search(question)

    context = "\n\n".join(
        chunk["content"] for chunk in results 
    )

    prompt = f"""
    You are a smart codebase assistant.

    Answer the question using only the provided code context. Do not answer questions that are not related to the code context.
    Respond politely that this is out of scope for you. Only stay close to the code context, if any irrelevant question is asked which does not relate
    to the code context, politely decline. If the user asks how they can improve the code

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