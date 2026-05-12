"""
============================================
评论 API - 文章评论的增删改查
============================================
使用 Tortoise ORM 异步操作。

API:
- GET    /api/comments/{post_id}  - 获取文章评论列表（公开）
- POST   /api/comments/{post_id}  - 发表评论（公开）
- DELETE /api/comments/{id}       - 删除评论（需登录）
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentListResponse

router = APIRouter(prefix="/api/comments", tags=["评论"])


@router.get("/{post_id}", response_model=CommentListResponse)
async def list_comments(post_id: int):
    """获取文章评论列表（公开）"""
    comments = await Comment.filter(post_id=post_id, is_approved=True).order_by("created_at")
    return CommentListResponse(
        items=[CommentResponse.from_attributes(c) for c in comments],
        total=len(comments),
    )


@router.post("/{post_id}", response_model=CommentResponse)
async def create_comment(post_id: int, data: CommentCreate):
    """发表评论（公开）"""
    if not data.content or not data.content.strip():
        raise HTTPException(status_code=400, detail="评论内容不能为空")

    comment = await Comment.create(
        post_id=post_id,
        author=data.author or "匿名",
        email=data.email or "",
        content=data.content.strip(),
        parent_id=data.parent_id,
    )
    return CommentResponse.from_attributes(comment)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
):
    """删除评论（需登录）"""
    comment = await Comment.get_or_none(id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="评论不存在")
    await comment.delete()
    return {"message": "评论已删除", "id": comment_id}
