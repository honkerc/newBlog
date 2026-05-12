"""
============================================
标签 API - 文章标签的增删改查
============================================
使用 Tortoise ORM 异步操作。

API:
- GET    /api/tags           - 获取所有标签（公开）
- POST   /api/tags           - 创建标签（需登录）
- DELETE /api/tags/{id}      - 删除标签（需登录）
- GET    /api/posts?tag=xxx  - 按标签筛选文章（在 posts.py 中实现）
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.tag import Tag
from app.models.user import User
from app.schemas.tag import TagCreate, TagResponse, TagListResponse

router = APIRouter(prefix="/api/tags", tags=["标签"])


@router.get("", response_model=TagListResponse)
async def list_tags():
    """获取所有标签（公开）"""
    tags = await Tag.all().order_by("name")
    return TagListResponse(
        items=[TagResponse.from_attributes(t) for t in tags],
    )


@router.post("", response_model=TagResponse)
async def create_tag(
    data: TagCreate,
    current_user: User = Depends(get_current_user),
):
    """创建标签（需登录）"""
    if not data.name or not data.name.strip():
        raise HTTPException(status_code=400, detail="标签名称不能为空")

    existing = await Tag.get_or_none(name=data.name.strip())
    if existing:
        return TagResponse.from_attributes(existing)

    tag = await Tag.create(name=data.name.strip())
    return TagResponse.from_attributes(tag)


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
):
    """删除标签（需登录）"""
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="标签不存在")
    await tag.delete()
    return {"message": "标签已删除", "id": tag_id}
