from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DOCUMENTS_DIR = Path("app/rag/documents")
CHROMA_DIR = Path("app/rag/chroma_db")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="aegis_knowledge"
)


def split_text(text):
    chunks = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def ingest_documents():
    documents = list(DOCUMENTS_DIR.glob("*.txt"))

    if not documents:
        print("No documents found.")
        return

    total_chunks = 0

    for document in documents:
        text = document.read_text(
            encoding="utf-8"
        )

        chunks = split_text(text)

        for index, chunk in enumerate(chunks):
            embedding = embedding_model.encode(
                chunk
            ).tolist()

            collection.upsert(
                ids=[
                    f"{document.stem}-{index}"
                ],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[
                    {
                        "source": document.name
                    }
                ]
            )

            total_chunks += 1

    print(
        f"Ingestion complete. "
        f"Documents: {len(documents)}, "
        f"Chunks: {total_chunks}"
    )


if __name__ == "__main__":
    ingest_documents()