import os
import base64
from dotenv import load_dotenv
import requests

def get_image_path(image_name):
    """Get the image path from the assets/images directory."""
    current_dir = os.getcwd()
    image_dir = os.path.join(current_dir, 'assets', 'images')
    # Assuming the image name is known, you can replace 'image.jpg' with the actual image name
    image_path = os.path.join(image_dir, image_name)
    return image_path

def encode_image(image_path):
    """Convert the image to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def call_openai_api(api_key, base64_image, message, model = "gpt-4o-mini", max_tokens=2000):
    """Call the OpenAI API with the base64-encoded image."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": message},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def display_result(response):
    """Display the result from the OpenAI API."""
    if response and "choices" in response and len(response["choices"]) > 0:
        print(response["choices"][0]["message"]["content"])
    else:
        print("No valid response received from the API.")

def main():

    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    message = "give me angular code"

    # Get the image path
    image_path = get_image_path("login.png")

    # Convert the image to base64
    base64_image = encode_image(image_path)

    # Call the OpenAI API
    response = call_openai_api(api_key, base64_image, message)

    # Display the result
    display_result(response)

if __name__ == "__main__":
    main()
