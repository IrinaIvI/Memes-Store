from minio import Minio
from minio.error import S3Error
from io import BytesIO
from typing import Optional
from .config import MINIO_ACCESS_KEY, MINIO_BUCKET_NAME, MINIO_SECRET_KEY, MINIO_URL
import logging
import os

logging.basicConfig(level=logging.INFO)

MINIO_URL = os.getenv("MINIO_URL", "host.docker.internal:9000") 
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio_access_key")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio_secret_key")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "memes")

client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


if not Minio.bucket_exists(MINIO_BUCKET_NAME):
    Minio.make_bucket(MINIO_BUCKET_NAME)

def upload_file(file: BytesIO, file_name: str) -> Optional[str]:
    try:
        Minio.put_object(
            MINIO_BUCKET_NAME,
            file_name,
            data=file,
            length=file.getbuffer().nbytes,
            content_type="application/octet-stream"
        )
        
        original_minio_str = Minio.presigned_get_object(MINIO_BUCKET_NAME, file_name)
        logging.info(original_minio_str)

        return original_minio_str

    except S3Error as e:
        raise Exception(f"Error uploading file: {e}")