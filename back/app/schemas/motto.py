"""
============================================
一句话数据模型 - 请求和响应的数据结构
============================================
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MottoCreate(BaseModel):
    """创建语录请求体"""
    content: str
    location: str = ""
    images: str = ""
    is_published: bool = True


class MottoUpdate(BaseModel):
    """更新语录请求体"""
    content: Optional[str] = None
    location: Optional[str] = None
    images: Optional[str] = None
    is_published: Optional[bool] = None


class MottoResponse(BaseModel):
    """语录响应体"""
    id: int
    content: str
    location: str = ""
    images: str = ""
    is_published: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
