import base64
from ..core.config import GROQ_API_KEY, IMAGE_DESCRIPTION_TEMPERATURE, IMAGE_DESCRIPTION_MAX_TOKENS, IMAGE_BATCH_SIZE
from groq import Groq

client = Groq(
    api_key=GROQ_API_KEY,
)

def describe_images_batch(image_bytes_list: list[bytes]) -> list[str]:
    """
    send multiple images in one request, return list of descriptions
    descriptions separated by double newlines in response
    """
    content = [
        {
            "type": "text",
            "text": "Describe each image in detail, including any numbers, labels, or data shown. Separate each description with a blank line."
        }
    ]

    for img_bytes in image_bytes_list:
        base64_image = base64.b64encode(img_bytes).decode('utf-8')
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
        })

    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{"role": "user", "content": content}],
        temperature=IMAGE_DESCRIPTION_TEMPERATURE,
        max_completion_tokens=IMAGE_DESCRIPTION_MAX_TOKENS
    )

    response_text = completion.choices[0].message.content
    descriptions = [desc.strip() for desc in response_text.split("\n\n") if desc.strip()]
    return descriptions

def process_images(elements: list) -> list:
    """
    process images in batches, replace image content with descriptions
    """
    image_elements = [e for e in elements if e["type"] == "image"]

    if not image_elements:
        return elements

    print(f"Total images to process: {len(image_elements)}")

    all_descriptions = []

    for i in range(0, len(image_elements), IMAGE_BATCH_SIZE):
        batch = image_elements[i:i+IMAGE_BATCH_SIZE]
        batch_num = (i // IMAGE_BATCH_SIZE) + 1
        print(f"Processing batch {batch_num} ({len(batch)} images)...")

        descriptions = describe_images_batch([e["content"] for e in batch])
        all_descriptions.extend(descriptions)

    # map descriptions back to elements
    img_idx = 0
    for element in elements:
        if element["type"] == "image":
            element["content"] = all_descriptions[img_idx]
            img_idx += 1

    return elements