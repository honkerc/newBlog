"""
============================================
文章数据模型 - 请求和响应的数据结构
============================================
定义文章相关的 API 请求和响应格式。
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostCreate(BaseModel):
    """
    创建文章请求体
    
    示例:
    {
        "title": "我的第一篇文章",
        "content": "# Hello World\n这是内容...",
        "summary": "文章摘要",
        "cover_url": "https://example.com/cover.jpg",
        "category": "技术",
        "tag": "Vue",
        "is_published": false
    }
    """
    title: str = "无标题"
    content: str = ""
    summary: str = ""
    cover_url: str = ""
    category: str = ""
    tag: str = ""
    is_published: bool = False
    is_book: bool = False


class PostUpdate(BaseModel):
    """
    更新文章请求体
    所有字段可选，只更新提供的字段。
    """
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    cover_url: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    is_published: Optional[bool] = None
    is_book: Optional[bool] = None


class PostResponse(BaseModel):
    """
    文章响应体
    """
    id: int
    title: str
    content: str
    summary: str
    cover_url: str
    category: str
    tag: str = ""
    is_published: bool
    is_top: bool
    is_book: bool = False
    view_count: int
    like_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
