from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from fastapi import UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import MemeScheme
from .models import Meme
from typing import List
import httpx

async def get_all_memes(db: AsyncSession) -> List[MemeScheme]:
    try:
        result = await db.execute(select(Meme))
        memes = result.scalars().all()

        if memes:

            response = [
                {
                    "id": meme.id,
                    "title": meme.title,
                    "image_url": meme.image_url,
                }
                for meme in memes
            ]
        else:
            return JSONResponse("There is no any meme")

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
    
async def post_meme(db: AsyncSession, text: str, file: UploadFile = File(...)) -> str:
    try:
        file_content = await file.read()
        files = {'photo': (file.filename, file_content, file.content_type)}
        
        response = await handle_request(
            url='http://auth-service:8001/mem_store/upload_file',
            parameters={},  
            files=files,
            request_type="POST",
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, 
                                detail="Failed to upload the file to external service")
    
        file_url = response.json().get("file_url") 
    
        new_meme = Meme(text=text, image_url=file_url)
        
        db.add(new_meme)
        await db.commit()
        await db.refresh(new_meme) 
        
        return JSONResponse("Meme is uploaded successfully!")

    except Exception as e:
        await db.rollback() 
        raise HTTPException(status_code=500, detail=f'Error occurred: {str(e)}')

async def delete_meme(db: AsyncSession, id: int) -> None:
    try:
        result = await db.execute(select(Meme).where(Meme.id == id))
        meme = result.scalars().first()

        if meme:
            await db.delete(meme)
            await db.commit()
        else:
            raise HTTPException(status_code=404, detail="Meme not found")
    except Exception as e:

        await db.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    
async def update_meme(id: int, text: str, db: AsyncSession, file: UploadFile = File(...)):
    try:
        meme = db.execute(select(Meme).where(Meme.id == id))

        if not meme:
            raise HTTPException(status_code=404, detail="Meme not found")
        
        meme.text = text

        if file:
            file_content = await file.read()
            files = {'photo': (file.filename, file_content, file.content_type)}
            
            response = await handle_request(
                url='http://auth-service:8001/mem_store/upload_file',  
                parameters={},
                files=files,
                request_type="POST",
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, 
                                    detail="Failed to upload the file to external service")
            
            file_url = response.json().get("file_url")
            meme.image_url = file_url 

        db.add(meme)
        await db.commit()

        await db.refresh(meme)
        
        return JSONResponse("Meme updated successfully!")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}')


async def handle_request(url: str, parameters: dict = None, files: dict = None, request_type: str = 'get'):
    async with httpx.AsyncClient() as client:
        if request_type == 'POST':
            response = await client.post(url, params=parameters, files=files, timeout=10)
        else:
            response = await client.get(url, params=parameters, timeout=10)
        return response.json()