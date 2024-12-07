from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MINIO_URL: str = "https://localhost:9000"
    MINIO_ACCESS_KEY: str = "minioaccesskey"
    MINIO_SECRET_KEY: str = "miniosecretkey"
    MINIO_BUCKET_NAME: str = "memes"
    
    # class Config:
    #     env_file = ".env"

settings = Settings()