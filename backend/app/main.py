from fastapi import FastAPI
from .db.database import Base
from .db.database import engine

from app.db.models.init import User, File
from app.db.models.user import User
from app.db.models.file import File
from app.db.models.text import Text

app = FastAPI(
    title="Enterprise RAG Application",
    description="A Retrieval-Augmented Generation (RAG) application for enterprise use cases.",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Backend running in cool way....."}