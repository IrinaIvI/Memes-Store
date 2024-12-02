from fastapi import FastAPI
from .routers import router

app = FastAPI(title='Memes Store')
app.include_router(router)
