"""
============================================
一句话 API - 简短语录/签名的增删改查
============================================
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.security import get_current_user
from app.models.motto import Motto
from app.models.user import User
from app.schemas.motto import MottoCreate, MottoUpdate

router = APIRouter(prefix="/api/mottos", tags=["一句话"])


# ==================== 公开接口 ====================

@router.get("")
async def list_mottos(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
):
    """获取语录列表（公开）"""
    total = await Motto.filter(is_published=True).count()
    items = await Motto.filter(is_published=True).order_by("-created_at").offset((page - 1) * page_size).limit(page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/latest")
async def list_latest_mottos():
    """获取最新语录（首页用，取前5条）"""
    items = await Motto.filter(is_published=True).order_by("-created_at").limit(5)
    return {"items": items}


@router.get("/{motto_id}")
async def get_motto(motto_id: int):
    """获取语录详情（公开）"""
    motto = await Motto.get_or_none(id=motto_id)
    if not motto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="语录不存在")
    return motto


# ==================== 管理接口 ====================

@router.post("")
async def create_motto(data: MottoCreate, current_user: User = Depends(get_current_user)):
    """创建语录"""
    motto = await Motto.create(**data.model_dump())
    return motto


@router.put("/{motto_id}")
async def update_motto(motto_id: int, data: MottoUpdate, current_user: User = Depends(get_current_user)):
    """更新语录"""
    motto = await Motto.get_or_none(id=motto_id)
    if not motto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="语录不存在")
    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        await motto.update_from_dict(update_data)
        await motto.save()
    return motto


@router.delete("/{motto_id}")
async def delete_motto(motto_id: int, current_user: User = Depends(get_current_user)):
    """删除语录"""
    motto = await Motto.get_or_none(id=motto_id)
    if not motto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="语录不存在")
    await motto.delete()
    return {"message": "语录已删除", "id": motto_id}
