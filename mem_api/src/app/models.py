from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Meme(Base):
    __tablename__ = "mems"

    id = Column(Integer, primary_key=True)
    title = Column(String, default="just a meme")
    image_url = Column(String, nullable=False)
    