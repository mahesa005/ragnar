import chromadb
from ..core.config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME

def store_to_chromadb(chunks: list):
    """
    embed (default chromadb) and store chunks to chromadb
    input: list of dict {"text": ..., "page_num": ...}
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"page_num": chunk["page_num"]} for chunk in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )