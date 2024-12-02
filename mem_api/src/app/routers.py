from fastapi import APIRouter, Depends
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_all_memes, get_meme, post_meme, delete_meme
from .databases import get_db
from .schemas import MemeScheme

router = APIRouter(prefix='/memes')

@router.get('/', response_model=Union[List[MemeScheme], str])
async def route_get_all_memes(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_memes(db=db)

@router.get('/{id}', response_model=MemeScheme)
async def route_get_meme(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_meme(db=db, id=id)

@router.get('/')
async def hello():
    return {'msg': 'Hello'}