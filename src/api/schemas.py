from pydantic import BaseModel
from typing import List, Optional


# =========================
# TOP PRODUCTS
# =========================
class TopProduct(BaseModel):
    product: str
    mentions: int


class TopProductsResponse(BaseModel):
    limit: int
    data: List[TopProduct]


# =========================
# CHANNEL ACTIVITY
# =========================
class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int
    avg_views: float
    date: str


class ChannelActivityResponse(BaseModel):
    data: List[ChannelActivity]


# =========================
# MESSAGE SEARCH
# =========================
class MessageSearchResult(BaseModel):
    message_id: int
    message_text: Optional[str]
    views: Optional[int]
    forwards: Optional[int]


class MessageSearchResponse(BaseModel):
    data: List[MessageSearchResult]


# =========================
# VISUAL CONTENT STATS
# =========================
class VisualContentStat(BaseModel):
    image_category: str
    total_posts: int
    avg_views: float


class VisualContentResponse(BaseModel):
    data: List[VisualContentStat]