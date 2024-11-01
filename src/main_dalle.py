import openai
import os
import requests
from dotenv import dotenv_values

# Set up OpenAI credentials
CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG.get("KEY") or os.environ.get("OPEN_AI_KEY")
OPEN_AI_ORG = CONFIG.get("ORG") or os.environ.get("OPEN_AI_ORG")

openai.api_key = OPEN_AI_KEY
openai.organization = OPEN_AI_ORG

def load_file(filename: str) -> str:
    """Loads content from a specified file"""
    with open(filename, "r") as fh:
        return fh.read()

# Updated function to generate image using the latest DALL-E API syntax
def generate_image_prompt(description):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=description,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

# Function to download and save the image
def save_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image, status code: {response.status_code}")

def main():
    num_images = 12  # Set to the number of panels
    for i in range(1, num_images + 1):
        prompt_filename = f"prompts/prompt_{i}.txt"
        prompt = load_file(prompt_filename)

        # Generate image
        image_url = generate_image_prompt(prompt)

        # Save image
        save_image(image_url, f"img/panel_{i}.png")
        print(f"Generated and saved image for Panel {i}")

if __name__ == "__main__":
    main()
