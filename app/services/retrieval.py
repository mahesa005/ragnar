import chromadb
from ..core.config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, CHROMA_MAX_QUERY_RESULT

def chroma_db_query(query: list[str]):
    """
    send a query to the chroma db
    output: list of n relevant chunks including their metadata
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
    results = []

    query_results = collection.query(
        query_texts=query,
        n_results=CHROMA_MAX_QUERY_RESULT
    )
    for doc, meta in zip(query_results["documents"][0], query_results["metadatas"][0]):
        results.append({"text": doc, "metadata": meta})
    return results