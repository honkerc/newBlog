"""
============================================
评论数据模型 - 请求和响应的数据结构
============================================
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class CommentCreate(BaseModel):
    """创建评论请求体"""
    author: str = "匿名"
    email: str = ""
    content: str = ""
    parent_id: Optional[int] = None


class CommentResponse(BaseModel):
    """评论响应体"""
    id: int
    post_id: int
    author: str
    email: str
    content: str
    parent_id: Optional[int] = None
    is_approved: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    """评论列表响应体"""
    items: List[CommentResponse]
    total: int
