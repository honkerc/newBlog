"""
============================================
动态数据模型 - 请求和响应的数据结构
============================================
定义动态相关的 API 请求和响应格式。
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MomentCreate(BaseModel):
    """
    创建动态请求体
    
    示例:
    {
        "content": "今天天气真好！",
        "category": "moment",
        "images": "https://example.com/img1.jpg,https://example.com/img2.jpg",
        "is_published": true
    }
    """
    category: str = "moment"
    content: str = ""
    images: str = ""
    is_published: bool = True


class MomentUpdate(BaseModel):
    """
    更新动态请求体
    所有字段可选，只更新提供的字段。
    """
    category: Optional[str] = None
    content: Optional[str] = None
    images: Optional[str] = None
    is_published: Optional[bool] = None
    is_top: Optional[bool] = None


class MomentResponse(BaseModel):
    """
    动态响应体
    """
    id: int
    category: str
    content: str
    images: str
    is_published: bool
    is_top: bool
    like_count: int
    comment_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
