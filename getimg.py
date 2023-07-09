import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import tqdm
import os

def download_images(name, category, headers):
    url = f"https://www.google.com/search?hl=en&authuser=0&tbm=isch&sxsrf&q={urllib.parse.quote(name)}+{urllib.parse.quote(category)}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    image_urls = [img['src'] for img in soup.find_all('img')]
    image_urls = image_urls[1:]  # ignore the first url as it is a Google logo

    os.makedirs(f'images/{name}', exist_ok=True)
    for i, url in enumerate(image_urls):
        urllib.request.urlretrieve(url, f'images/{name}/{category}_{i}.jpg')

def main():
    with open('names.json', 'r') as file:
        data = json.load(file)
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Referer': 'https://www.google.com'
    }

    for name, categories in tqdm.tqdm(data.items(), desc="Downloading"):
        for category in categories:
            try:
                download_images(name, category, headers)
            except Exception as e:
                print(f"Error occurred while downloading images for {name} {category}: {e}")

if __name__ == "__main__":
    main()
