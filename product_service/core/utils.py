import cloudinary
import cloudinary.uploader
import requests
import tempfile
import os
from decouple import config
from cloudinary.utils import cloudinary_url


def upload_images(images):
    uploaded_images = []
    for image in images:
        try:
            upload_result = cloudinary.uploader.upload(image)
            uploaded_images.append(upload_result['secure_url'])
        except Exception as e:
            print(f"Error uploading image: {e}")
            continue
    return uploaded_images

def get_user(user_id):
    user_service_url = config('USER_SERVICE_URL')
    url = f'{user_service_url}/api/auth/users/{user_id}/'
    response = requests.get(url)
    return response.json()

def save_uploaded_images_as_temp_files(images):
    """
    Saves uploaded images as temporary files and returns their file paths.

    Args:
        images (list): List of InMemoryUploadedFile objects (Django request.FILES)

    Returns:
        list: List of temporary file paths
    """
    image_paths = []
    for image in images:
        try:
            file_ext = os.path.splitext(image.name)[1] or ".jpg"  # Default to .jpg if no extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
            temp_file.write(image.read())
            temp_file.close()
            image_paths.append(temp_file.name)
        except Exception as e:
            print(f"Error saving image {image.name}: {e}")
    return image_paths
