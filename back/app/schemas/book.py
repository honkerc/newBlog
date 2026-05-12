"""
============================================
书籍数据模型 - 请求和响应的数据结构
============================================
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BookCreate(BaseModel):
    """创建书籍请求体"""
    title: str
    author: str = ""
    cover_url: str = ""
    summary: str = ""


class BookUpdate(BaseModel):
    """更新书籍请求体"""
    title: Optional[str] = None
    author: Optional[str] = None
    cover_url: Optional[str] = None
    summary: Optional[str] = None


class BookResponse(BaseModel):
    """书籍响应体"""
    id: int
    title: str
    author: str = ""
    cover_url: str = ""
    summary: str = ""
    view_count: int
    like_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
