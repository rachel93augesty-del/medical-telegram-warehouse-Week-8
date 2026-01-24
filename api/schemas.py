# api/schemas.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

# Top Products
class TopProductItem(BaseModel):
    product: str
    mentions: int

class TopProductsResponse(BaseModel):
    top_products: List[TopProductItem]

# Visual Content Stats
class VisualContentStatsResponse(BaseModel):
    channel_name: str
    total_messages: int
    messages_with_images: int
    image_percentage: float

# Channel Activity
class ChannelActivityItem(BaseModel):
    date: datetime
    message_count: int

class ChannelActivityResponse(BaseModel):
    channel_name: str
    activity: List[ChannelActivityItem]

# Message Search
class MessageItem(BaseModel):
    id: int
    channel_name: str
    text: str
    created_at: datetime

class MessageSearchResponse(BaseModel):
    messages: List[MessageItem]
