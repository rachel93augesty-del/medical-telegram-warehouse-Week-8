# api/routers/reports.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from collections import Counter
from typing import List

from api.database import SessionLocal
from api.models import Message
from api.schemas import TopProductsResponse, TopProductItem, VisualContentStatsResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Top products endpoint
@router.get("/top-products", response_model=TopProductsResponse)
def get_top_products(limit: int = Query(10, gt=0), db: Session = Depends(get_db)):
    try:
        messages = db.query(Message.text).all()
        all_words = []
        for (text,) in messages:
            if text:
                all_words.extend(text.lower().split())
        top_counts = Counter(all_words).most_common(limit)
        return TopProductsResponse(
            top_products=[TopProductItem(product=p, mentions=c) for p, c in top_counts]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get top products: {e}")

# Visual content stats
@router.get("/visual-content", response_model=List[VisualContentStatsResponse])
def visual_content_stats(db: Session = Depends(get_db)):
    try:
        channels = db.query(Message.channel_name).distinct().all()
        stats = []
        for (channel_name,) in channels:
            total = db.query(Message).filter(Message.channel_name == channel_name).count()
            with_images = db.query(Message).filter(Message.channel_name == channel_name, Message.has_image == True).count()
            percentage = (with_images / total * 100) if total else 0
            stats.append(VisualContentStatsResponse(
                channel_name=channel_name,
                total_messages=total,
                messages_with_images=with_images,
                image_percentage=round(percentage, 2)
            ))
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get visual stats: {e}")
