"""
============================================
搜索 API - 统一搜索文章和动态
============================================
支持按关键词搜索文章标题/内容和动态内容，
返回匹配关键词前后的上下文片段。
"""

import re
from fastapi import APIRouter, Query
from app.models.post import Post
from app.models.moment import Moment

router = APIRouter(prefix="/api/search", tags=["搜索"])

# 上下文截取宽度（关键词前后各取多少字符）
CONTEXT_WIDTH = 60


def extract_snippet(text: str, keyword: str, max_len: int = 200) -> str:
    """
    从文本中提取包含关键词的上下文片段。
    找到关键词位置，取前后 CONTEXT_WIDTH 字符，用 ... 表示截断。
    """
    if not text or not keyword:
        return (text or "")[:max_len]

    # 不区分大小写查找
    lower_text = text.lower()
    lower_keyword = keyword.lower()
    idx = lower_text.find(lower_keyword)

    if idx == -1:
        return text[:max_len]

    start = max(0, idx - CONTEXT_WIDTH)
    end = min(len(text), idx + len(keyword) + CONTEXT_WIDTH)

    snippet = ""
    if start > 0:
        snippet += "..."
    snippet += text[start:end]
    if end < len(text):
        snippet += "..."

    if len(snippet) > max_len:
        snippet = snippet[:max_len] + "..."

    return snippet


@router.get("")
async def search_all(
    q: str = Query("", description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=50, description="每页数量"),
):
    """
    统一搜索（公开）
    同时搜索文章和动态，按时间倒序排列。
    返回匹配关键词前后的上下文片段。
    """
    if not q:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}

    keyword = q.strip()

    # 搜索文章（标题和内容）
    posts = await Post.filter(
        is_published=True
    ).filter(
        title__icontains=keyword
    ).order_by("-created_at").limit(page_size).all()

    # 搜索文章内容
    content_posts = await Post.filter(
        is_published=True
    ).filter(
        content__icontains=keyword
    ).order_by("-created_at").limit(page_size).all()

    # 搜索动态
    moments = await Moment.filter(
        is_published=True
    ).filter(
        content__icontains=keyword
    ).order_by("-created_at").limit(page_size).all()

    # 合并去重
    seen_post_ids = set()
    merged = []

    for p in posts + content_posts:
        if p.id not in seen_post_ids:
            seen_post_ids.add(p.id)

            # 判断匹配来源
            matched_in_title = keyword.lower() in (p.title or "").lower()
            matched_in_content = keyword.lower() in (p.content or "").lower()

            # 提取上下文片段
            if matched_in_title:
                snippet = extract_snippet(p.title, keyword)
            else:
                snippet = extract_snippet(p.content, keyword)

            merged.append({
                "type": "post",
                "id": p.id,
                "title": p.title,
                "snippet": snippet,
                "matched_in_title": matched_in_title,
                "matched_in_content": matched_in_content,
                "category": p.category,
                "cover_url": p.cover_url,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "url": f"/post/{p.id}",
            })

    for m in moments:
        snippet = extract_snippet(m.content, keyword)
        merged.append({
            "type": "moment",
            "id": m.id,
            "title": "",
            "snippet": snippet,
            "matched_in_title": False,
            "matched_in_content": True,
            "category": "",
            "cover_url": "",
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "url": f"/moments",
        })

    # 按时间倒序
    merged.sort(key=lambda x: x["created_at"] or "", reverse=True)

    total = len(merged)
    start = (page - 1) * page_size
    items = merged[start:start + page_size]

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }
