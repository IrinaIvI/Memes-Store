from minio import Minio
from minio.error import S3Error
from io import BytesIO
from typing import Optional
from .config import settings

client = Minio(
    settings.MINIO_URL,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
)

def upload_file(file: BytesIO, file_name: str) -> Optional[str]:
    try:
        if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
            client.make_bucket(settings.MINIO_BUCKET_NAME)
        
        client.put_object(
            settings.MINIO_BUCKET_NAME,
            file_name,
            data=file,
            length=len(file.getvalue()),
            content_type="application/octet-stream"
        )

        return client.presigned_get_object(settings.MINIO_BUCKET_NAME, file_name)

    except S3Error as e:
        raise Exception(f"Error uploading file: {e}")