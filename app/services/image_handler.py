import base64
from ..core.config import GROQ_API_KEY
from groq import Groq

client = Groq(
    api_key=GROQ_API_KEY,
)

def describe_image(image_bytes: bytes) -> str:
    """
    Send image through GROQ api to retrieve description
    """
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image/chart/infographic in detail, including any numbers, labels, or data shown."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        max_completion_tokens=500
    )
    return completion.choices[0].message.content

def process_images(elements: list) -> list:
    """
    loop every element that is an image,
    returns the description and replaces the image itself
    """
    for element in elements:
        if element["type"] == "image":
            element["content"] = describe_image(element["content"])
    return elements