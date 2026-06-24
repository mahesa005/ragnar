from groq import Groq
from ..core.config import GROQ_API_KEY, LLM_TEMPERATURE, LLM_MAX_TOKENS, LLM_TOP_P

client = Groq(
    api_key=GROQ_API_KEY,
)

def clean_response(response: str) -> str:
    """
    clean LLM response: remove thinking tags, remove markdown formatting
    """
    import re

    # Remove thinking tags and content
    if "<think>" in response:
        think_end = response.find("</think>")
        if think_end != -1:
            response = response[think_end + 8:].strip()
        else:
            response = response.split("<think>", 1)[1].strip()

    # Remove markdown bold/italic formatting
    response = re.sub(r'\*\*(.+?)\*\*', r'\1', response)  # **bold** → bold
    response = re.sub(r'\*(.+?)\*', r'\1', response)      # *italic* → italic
    response = re.sub(r'\_(.+?)\_', r'\1', response)      # _italic_ → italic

    # Remove markdown list markers
    response = re.sub(r'^\s*[-*+]\s+', '', response, flags=re.MULTILINE)  # - item → item

    # Clean up extra whitespace
    response = re.sub(r'\n\s*\n+', '\n\n', response)  # multiple newlines → double newline

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