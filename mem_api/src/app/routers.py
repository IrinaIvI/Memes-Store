from fastapi import APIRouter
from .crud import get_all_memes, get_meme, post_meme, delete_meme

router = APIRouter(prefix='/api_meme')