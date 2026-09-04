import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = "app/rag/chroma_db"

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = client.get_collection(
    name="aegis_knowledge"
)


def retrieve_documents(query, top_k=3):
    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    retrieved_documents = []

    for document, metadata in zip(
        documents,
        metadatas
    ):
        retrieved_documents.append({
            "content": document,
            "source": metadata.get("source")
        })

    return retrieved_documents


if __name__ == "__main__":
    query = input("Ask AEGIS: ")

    results = retrieve_documents(query)

    print("\nRelevant knowledge:\n")

    for index, result in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print(f"Source: {result['source']}")
        print(result["content"])
        print()