from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


"""
Multimodal AI refers to artificial intelligence (AI) systems that can process and integrate data from multiple sources (modalities) simultaneously, such as text, images, audio, and video, to produce more comprehensive and nuanced outputs
"""

# using new syntax of openai sdk for calling apis
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Tell me the caption for the attached image",
                },
                {
                    "type": "input_image",
                    "image_url": "https://images.pexels.com/photos/879109/pexels-photo-879109.jpeg",
                },
            ],
        }
    ],
)

print(response.output_text)
