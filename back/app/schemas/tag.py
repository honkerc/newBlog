"""
============================================
标签数据模型 - 请求和响应的数据结构
============================================
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class TagCreate(BaseModel):
    """创建标签请求体"""
    name: str


class TagResponse(BaseModel):
    """标签响应体"""
    id: int
    name: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """标签列表响应体"""
    items: List[TagResponse]
