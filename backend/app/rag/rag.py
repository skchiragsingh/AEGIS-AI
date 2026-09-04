from app.rag.retriever import retrieve_documents
from app.rag.llm import generate_answer


def ask_aegis(query):
    results = retrieve_documents(query)

    context = "\n\n".join(
        result["content"]
        for result in results
    )

    prompt = f"""
You are AEGIS, an AI incident response assistant.

Use the following AEGIS knowledge base to answer the user's question.

Knowledge Base:
{context}

User Question:
{query}

Instructions:
- Answer using the provided knowledge.
- Do not invent facts that are not supported by the knowledge base.
- Give practical and clear guidance.
- If the knowledge base does not contain enough information, say so.

Answer:
"""

    return generate_answer(prompt)


if __name__ == "__main__":
    query = input("Ask AEGIS: ")

    answer = ask_aegis(query)

    print("\nAEGIS:")
    print(answer)