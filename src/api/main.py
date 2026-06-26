from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import text

from .db import engine

from .queries import (
    get_top_products,
    get_channel_activity,
    search_messages,
    get_visual_content_stats
)

from .schemas import (
    TopProductsResponse,
    ChannelActivityResponse,
    MessageSearchResponse,
    VisualContentResponse
)

app = FastAPI(title="Telegram Analytics API")


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def home():
    return {"message": "API running"}


# -------------------------
# 1. TOP PRODUCTS
# -------------------------
@app.get("/api/reports/top-products", response_model=TopProductsResponse)
def top_products(limit: int = Query(10, ge=1, le=100)):
    with engine.connect() as conn:
        result = conn.execute(text(get_top_products(limit)))
        rows = [dict(r._mapping) for r in result]

    return {"limit": limit, "data": rows}


# -------------------------
# 2. CHANNEL ACTIVITY
# -------------------------
@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivityResponse)
def channel_activity(channel_name: str):
    with engine.connect() as conn:
        result = conn.execute(text(get_channel_activity(channel_name)))
        rows = [dict(r._mapping) for r in result]

    return {"data": rows}


# -------------------------
# 3. MESSAGE SEARCH
# -------------------------
@app.get("/api/search/messages", response_model=MessageSearchResponse)
def message_search(
    query: str,
    limit: int = Query(20, ge=1, le=100)
):
    with engine.connect() as conn:
        result = conn.execute(text(search_messages(query, limit)))
        rows = [dict(r._mapping) for r in result]

    if not rows:
        raise HTTPException(status_code=404, detail="No messages found")

    return {"data": rows}


# -------------------------
# 4. VISUAL CONTENT STATS
# -------------------------
@app.get("/api/reports/visual-content", response_model=VisualContentResponse)
def visual_content():
    with engine.connect() as conn:
        result = conn.execute(text(get_visual_content_stats()))
        rows = [dict(r._mapping) for r in result]

    return {"data": rows}