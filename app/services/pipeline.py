from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..core.config import CHUNK_SIZE, CHUNK_OVERLAP
from ..services.extract import extract_pdf
from ..services.image_handler import process_images
from ..services.embed import store_to_chromadb
from ..services.query import llm_query
from ..services.retrieval import chroma_db_query


def run_ingestion_pipeline(pdf_path: str):
    elements = extract_pdf(pdf_path)
    elements = process_images(elements)
    pages = group_by_page(elements)
    chunks = chunk_pages(pages)
    
    store_to_chromadb(chunks)
    
    return chunks

def chunk_pages(pages: dict) -> list:
    """
    chunk text based on page, each chunk has page_num meta data
    output: list of dict {"text": chunk_text, "page_num": page_num}
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    all_chunks = []
    for page_num, text in pages.items():
        chunks = splitter.split_text(text)
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "page_num": page_num
            })
    
    return all_chunks

def group_by_page(elements: list) -> dict:
    """
    group all elements by page_num
    output: dict {page_num: "combined text of page"}
    """
    pages = {}
    for element in elements:
        page_num = element["page_num"]
        content = str(element["content"])  # table is a list, convert to string
        
        if page_num not in pages:
            pages[page_num] = ""
        pages[page_num] += content + "\n"
    
    return pages

def retrieval_pipeline(query: list[str]):
    RAG_results = chroma_db_query(query)
    return llm_query(query, RAG_results)