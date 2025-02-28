import cloudinary
import cloudinary.uploader
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