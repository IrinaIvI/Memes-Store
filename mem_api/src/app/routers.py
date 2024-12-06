from fastapi import APIRouter, Depends
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_all_memes, get_meme, post_meme, delete_meme, update_meme
from .databases import get_db
from .schemas import MemeScheme
from fastapi import UploadFile, File

router = APIRouter(prefix='/memes')

@router.get('/', response_model=Union[list[MemeScheme], str])
async def route_get_all_memes(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_memes(db=db)

@router.get('/{id}', response_model=MemeScheme)
async def route_get_meme(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_meme(db=db, id=id)

@router.delete('/{id}', response_model=str)
async def route_delete_meme(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await delete_meme(db=db, id=id)

@router.post('/', response_model=str)
async def route_post_meme(text: str, db: Annotated[AsyncSession, Depends(get_db)], file: UploadFile = File(...)):
    return await post_meme(text=text, db=db, file=file)

@router.put('/{id}')
async def route_update_meme(id: int, text: str, db: Annotated[AsyncSession, Depends(get_db)], file: UploadFile = File(...)):
    return await update_meme(id=id, text=text, db=db, file=file)

