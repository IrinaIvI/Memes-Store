from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import MemeScheme
from .models import Meme
from typing import List


async def get_all_memes(db: AsyncSession) -> List[MemeScheme]:
    try:
        result = await db.execute(select(Meme))
        memes = result.scalars().all()

        response = [
            {
                "id": meme.id,
                "title": meme.title,
                "image_url": meme.image_url,
            }
            for meme in memes
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')

    return response

async def get_meme(db: AsyncSession, id: int) -> MemeScheme:
    try:
        result = await db.execute(select(Meme).where(Meme.id == id))
        meme = result.scalars().first() 

        if not meme:
            raise HTTPException(status_code=404, detail="Meme not found")

        return MemeScheme(id=meme.id, title=meme.title, image_url=meme.image_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')
    
async def post_meme(db: AsyncSession) -> str: # нужна картинка и текст
    pass

async def delete_meme(db: AsyncSession, id: int) -> None:
    pass