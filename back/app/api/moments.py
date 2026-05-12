"""
============================================
动态 API - 动态的增删改查
============================================
使用 Tortoise ORM 异步操作。

API:
- GET    /api/moments          - 动态列表（公开，支持 category 筛选）
- GET    /api/moments/latest   - 最新动态（公开，首页用）
- GET    /api/moments/categories - 动态类别统计（公开）
- GET    /api/moments/{id}     - 动态详情（公开）
- POST   /api/moments          - 创建动态（需登录）
- PUT    /api/moments/{id}     - 更新动态（需登录）
- DELETE /api/moments/{id}     - 删除动态（需登录）
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.security import get_current_user
from app.models.moment import Moment
from app.models.user import User
from app.schemas.moment import MomentCreate, MomentUpdate

router = APIRouter(prefix="/api/moments", tags=["动态"])


# ==================== 公开接口 ====================

@router.get("")
async def list_moments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    category: str = Query("", description="按类别筛选"),
):
    """获取动态列表（公开）"""
    filters = {"is_published": True}
    if category:
        filters["category"] = category

    total = await Moment.filter(**filters).count()
    moments = await Moment.filter(**filters).order_by("-created_at").offset((page - 1) * page_size).limit(page_size)
    return {"items": moments, "total": total, "page": page, "page_size": page_size}


@router.get("/latest")
async def list_latest_moments():
    """获取最新动态（首页用，取前5条已发布的）"""
    moments = await Moment.filter(is_published=True).order_by("-created_at").limit(5)
    return {"items": moments}


@router.get("/categories")
async def list_categories():
    """获取动态类别统计"""
    from tortoise.functions import Count
    cats = await Moment.filter(is_published=True).annotate(count=Count("id")).group_by("category").values("category", "count")
    return {"items": cats}


@router.get("/{moment_id}")
async def get_moment(moment_id: int):
    """获取动态详情（公开）"""
    moment = await Moment.get_or_none(id=moment_id)
    if not moment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="动态不存在")
    return moment


# ==================== 管理接口 ====================

@router.post("")
async def create_moment(data: MomentCreate, current_user: User = Depends(get_current_user)):
    """创建动态"""
    moment = await Moment.create(**data.model_dump())
    return moment


@router.put("/{moment_id}")
async def update_moment(moment_id: int, data: MomentUpdate, current_user: User = Depends(get_current_user)):
    """更新动态"""
    moment = await Moment.get_or_none(id=moment_id)
    if not moment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="动态不存在")
    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        await moment.update_from_dict(update_data)
        await moment.save()
    return moment


@router.delete("/{moment_id}")
async def delete_moment(moment_id: int, current_user: User = Depends(get_current_user)):
    """删除动态"""
    moment = await Moment.get_or_none(id=moment_id)
    if not moment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="动态不存在")
    await moment.delete()
    return {"message": "动态已删除", "id": moment_id}
