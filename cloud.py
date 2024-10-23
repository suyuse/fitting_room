import cloudinary
import cloudinary.uploader
import asyncio

cloudinary.config(
    cloud_name="dxqzvydku",
    api_key="311346433922211",
    api_secret="9vQgdHUdUfG44N8yCQ6cvtUTO2w",
    secure=True
)


async def upload_image_to_cloudinary(image_path):
    try:
        upload_result = cloudinary.uploader.upload(image_path)
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return None