from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from io import BytesIO
from .minio_client import upload_file

router = APIRouter(prefix='api_store')

@router.post("/upload/")
async def upload_meme(file: UploadFile):
    try:
        file_data = await file.read()
        file_bytes = BytesIO(file_data)
        
        file_url = upload_file(file_bytes, file.filename)
        
        return JSONResponse(content={"url": file_url}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))