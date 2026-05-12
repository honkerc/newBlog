"""
============================================
动态 Feed API - 动态时间线
============================================
所有动态（朋友圈/健身/阅读/学习/日常）统一返回。
"""

from fastapi import APIRouter, Query
from app.models.moment import Moment

router = APIRouter(prefix="/api/feed", tags=["动态"])


@router.get("")
async def get_feed(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(30, ge=1, le=100, description="每页数量"),
    category: str = Query("", description="按类别筛选"),
):
    """获取动态时间线（公开）"""
    filters = {"is_published": True}
    if category:
        filters["category"] = category

    total = await Moment.filter(**filters).count()
    items = await Moment.filter(**filters).order_by("-created_at").offset(
        (page - 1) * page_size
    ).limit(page_size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }
