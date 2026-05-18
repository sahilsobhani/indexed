from openai import OpenAI

client = OpenAI()

from retriever import search

def ask(question):
    question = question[:1000]
    results = search(question)

    context_parts = []
    for chunk in results:
        context_parts.append(
            "\n".join(
                [
                    f"Type: {chunk.get('type', 'unknown')}",
                    f"Name: {chunk.get('name', 'unknown')}",
                    f"File Name: {chunk.get('file_name', 'unknown')}",
                    f"File Path: {chunk.get('file_path', chunk.get('file', 'unknown'))}",
                    "Code:",
                    chunk.get("content", ""),
                ]
            )
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
    You are a smart codebase assistant.

    Answer the question using only the provided code context. Do not answer questions that are not related to the code context.
    Respond politely that this is out of scope for you. Only stay close to the code context, if any irrelevant question is asked which does not relate
    to the code context, politely decline. If the user asks how they can improve the code.
    If the answer is about where logic is located, include the file name or file path when it is present in the code context.

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
