import json
from openai import OpenAI
from pathlib import Path
from retriever import search

client = OpenAI()

CONVERSATION_PATH = Path("storage/conversation.json")
MAX_HISTORY_TURNS = 3

def load_conversation():
    """Load saved conversation history."""
    if not CONVERSATION_PATH.exists():
        return []

    with open(CONVERSATION_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_conversation(history):
    """Save conversation history to disk."""
    CONVERSATION_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CONVERSATION_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def format_history(history):
    """Format recent turns for retrieval and prompting."""
    recent_history = history[-MAX_HISTORY_TURNS:]

    return "\n".join(
        f"{message['role'].capitalize()}: {message['content']}"
        for message in recent_history
    )

def ask(question, history=None):
    """Answer using code context plus recent conversation."""
    question = question[:1000]

    if history is None:
        history = load_conversation()

    conversation_context = format_history(history)
    retrieval_query = question
    if conversation_context:
        retrieval_query = f"{conversation_context}\nUser: {question}"

    results = search(retrieval_query)

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

    history_block = conversation_context or "No previous conversation."

    prompt = f"""
    You are a smart codebase assistant.

    Answer the question using only the provided code context. Do not answer questions that are not related to the code context.
    Respond politely that this is out of scope for you. Only stay close to the code context, if any irrelevant question is asked which does not relate
    to the code context, politely decline. If the user asks how they can improve the code, you can proceed with suggestions.
    If the answer is about where logic is located, include the file name or file path when it is present in the code context.
    Use the conversation history to resolve follow-up references like "that", "this", or "the previous function".

    CONVERSATION HISTORY:
    {history_block}

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

    answer = response.choices[0].message.content

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    save_conversation(history)

    return answer
