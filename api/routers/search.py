# api/routers/search.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from api.database import SessionLocal
from api.models import Message
from api.schemas import MessageItem, MessageSearchResponse

router = APIRouter(prefix="/search", tags=["Search"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/messages", response_model=MessageSearchResponse)
def search_messages(query: str = Query(..., min_length=1), limit: int = 20, db: Session = Depends(get_db)):
    try:
        messages = db.query(Message).filter(Message.text.ilike(f"%{query}%")).limit(limit).all()
        result = [
            MessageItem(
                id=msg.id,
                channel_name=msg.channel_name,
                text=msg.text,
                created_at=msg.created_at
            )
            for msg in messages
        ]
        return MessageSearchResponse(messages=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search messages: {e}")
