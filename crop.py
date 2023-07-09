import os
import io
import cv2
from google.cloud import vision_v1p3beta1 as vision
from PIL import Image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './.google_creds.json'
client = vision.ImageAnnotatorClient()

def detect_face(face_file):
    print(f"Processing image: {face_file}")
    with io.open(face_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.face_detection(image=image)
    face_annotations = response.face_annotations

    if not face_annotations:
        print(f"No face detected in the image {face_file}. Skipping this image.")
        return None

    face_bounds = []
    for face in face_annotations:
        vertices = face.bounding_poly.vertices
        face_bounds.append((vertices[0].x, vertices[0].y, vertices[2].x, vertices[2].y))

    return face_bounds

def crop_face(img_path, output_path):
    bounds = detect_face(img_path)

    if bounds:
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to read image {img_path}, skipping cropping.")
            return

        for i, bound in enumerate(bounds):
            x, y, w, h = bound
            crop_img = img[y:h, x:w]
            # This line has been modified to include directory names in the output file name
            cropped_image_name = f"{output_path}/{os.path.dirname(img_path).replace('./images/', '').replace('/', '_')}_{os.path.basename(img_path).split('.')[0]}_{i}.jpg"

            cv2.imwrite(cropped_image_name, crop_img)
            print(f"Face detected and cropped image saved as {cropped_image_name}")
    else:
        print(f"No faces detected in {img_path}, skipping cropping.")

# Base directory where all subdirectories containing images are located
base_directory = './images'

# Output directory
output_path = './crop'

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Get list of image files in the 'images' directory and subdirectories and crop faces for each image
for root, dirs, files in os.walk(base_directory):
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(root, file)
            crop_face(img_path, output_path)
