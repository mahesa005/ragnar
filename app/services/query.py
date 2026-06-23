from groq import Groq
from ..core.config import GROQ_API_KEY, LLM_TEMPERATURE, LLM_MAX_TOKENS, LLM_TOP_P

client = Groq(
    api_key=GROQ_API_KEY,
)

def clean_response(response: str) -> str:
    """
    clean LLM response: remove thinking tags, format newlines, clean up markup
    """
    # Remove thinking tags
    if "</think>" in response:
        response = response.split("</think>", 1)[1].strip()

    # Clean up escaped newlines and other formatting
    response = response.replace("\\n", "\n")
    response = response.replace("\\_", "_")
    response = response.replace("\\*", "*")

    return response.strip()


def format_context(chunks: list) -> str:
    """
    format retrieved chunks into a readable context string for the LLM
    """
    formatted = ""
    for chunk in chunks:
        formatted += f"[Halaman {chunk['metadata']['page_num']}]\n{chunk['text']}\n\n"
    return formatted

def llm_query(question: str, chunks: list) -> str:
    """
    send question + retrieved context to LLM, return generated answer
    """
    context = format_context(chunks)

    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "system",
                "content": "Return an answer that is suitable for the query, based on the document chunks you received. Use the most relevant information (you can combine or choose which chunk will be used). Return an answer and give the relevant metadata (page number) as a citation."
            },
            {
                "role": "user",
                "content": f"Pertanyaan: {question}\n\nKonteks:\n{context}"
            }
        ],
        temperature=LLM_TEMPERATURE,
        max_completion_tokens=LLM_MAX_TOKENS,
        top_p=LLM_TOP_P,
        stream=False,
        stop=None
    )

    response = completion.choices[0].message.content
    return clean_response(response)