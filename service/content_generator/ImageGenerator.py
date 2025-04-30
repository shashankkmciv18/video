import os

import requests
from dotenv import load_dotenv

load_dotenv()
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")  # Replace with your Unsplash API key
resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources"))
background_image_path = os.path.join(resources_dir, 'background.jpg')


def fetch_background_image():
    query = "nature"
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    image_url = response.json()['urls']['regular']
    img_data = requests.get(image_url).content
    with open(background_image_path, 'wb') as handler:
        handler.write(img_data)
