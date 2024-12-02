from pydantic import BaseModel

class MemeScheme(BaseModel):
    id: int
    title: str
    image_url: str
