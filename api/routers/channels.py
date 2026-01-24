# api/routers/channels.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from api.database import SessionLocal
from api.models import Message
from api.schemas import ChannelActivityResponse, ChannelActivityItem

router = APIRouter(prefix="/channels", tags=["Channels"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{channel_name}/activity", response_model=ChannelActivityResponse)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    try:
        messages = db.query(Message).filter(Message.channel_name == channel_name).all()
        if not messages:
            raise HTTPException(status_code=404, detail="Channel not found")

        activity_dict = {}
        for msg in messages:
            date_str = msg.created_at.date()
            activity_dict[date_str] = activity_dict.get(date_str, 0) + 1

        activity_list = [
            ChannelActivityItem(date=datetime.combine(date, datetime.min.time()), message_count=count)
            for date, count in sorted(activity_dict.items())
        ]

        return ChannelActivityResponse(channel_name=channel_name, activity=activity_list)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch channel activity: {e}")
