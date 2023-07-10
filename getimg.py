import os
import string
import cv2
import requests
import json
import subprocess
from tqdm import tqdm

class ImageDownloader:
    def __init__(self):
        self.sanitized_search_term = ''

    @staticmethod
    def sanitize_filename(filename):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        sanitized_filename = ''.join(c for c in filename if c in valid_chars)
        return sanitized_filename

    def is_face_present(self, image_path):
        try:
            image = cv2.imread(image_path)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            return len(faces) > 0
        except cv2.error as e:
            print(f"Error processing image '{image_path}': {str(e)}")
            return False

    def download_images(self, image_links, search_term):
        if not os.path.exists('images'):
            os.makedirs('images')
        self.sanitized_search_term = self.sanitize_filename(search_term)
        for i, url in enumerate(image_links, start=1):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    image_path = f'images/{self.sanitized_search_term}-{str(i).zfill(2)}.jpg'
                    try:
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        if not self.is_face_present(image_path):
                            print(f"No face detected in '{image_path}'. Skipping.")
                            os.remove(image_path)
                        else:
                            self.convert_image_to_ascii(image_path)
                    except (IOError, cv2.error) as e:
                        print(f"Error processing image '{image_path}': {str(e)}")
                        if os.path.exists(image_path):
                            os.remove(image_path)
                else:
                    print(f"Failed to download image from '{url}' with status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while downloading image from '{url}': {str(e)}")

    @staticmethod
    def convert_image_to_ascii(image_path):
        command = ['python', 'ascii_converter.py', image_path]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("An error occurred while converting the image to ASCII:", result.stderr)

    def get_image_links(self, api_key, cse_id, search_term, num_images):
        url = "https://www.googleapis.com/customsearch/v1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': search_term,
            'searchType': 'image',
            'num': num_images,
            'start': 1
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            image_links = [item['link'] for item in response_data.get('items', [])]
            return image_links

    def get_names_and_categories(self, file_name):
        with open(file_name, 'r') as file:
            return json.load(file)

    def get_google_creds(self, file_name):
        with open(file_name, 'r') as file:
            creds = json.load(file)
            return creds['api_key'], creds['cse_id']

    def main(self):
        api_key, cse_id = self.get_google_creds('.google_creds.json')
        names_and_categories = self.get_names_and_categories('names.json')
        num_images = 5
        for name, categories in tqdm(names_and_categories.items(), desc='Processing names'):
            search_terms = [' '.join([name] + [category]) for category in categories] + [name]
            for search_term in search_terms:
                print(f"Searching for '{search_term}'...")
                image_links = self.get_image_links(api_key, cse_id, search_term, num_images)
                if image_links:
                    self.download_images(image_links, search_term.replace(' ', '_'))
                print(f"Finished searching for '{search_term}'.")

if __name__ == "__main__":
    downloader = ImageDownloader()
    downloader.main()
