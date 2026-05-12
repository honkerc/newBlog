"""
============================================
用户数据模型 - 请求和响应的数据结构
============================================
"""

from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    """登录请求体"""
    username: str = ""
    password: str = ""


class TokenResponse(BaseModel):
    """登录响应体"""
    access_token: str
    token_type: str = "bearer"
    username: str
    nickname: str = ""
    avatar: str = ""


class UserProfileResponse(BaseModel):
    """用户信息响应体"""
    id: int
    username: str
    nickname: str
    avatar: str
    bio: str
    email: str
    github: str = ""
    twitter: str = ""
    codepen: str = ""
    site_name: str
    site_description: str
    is_admin: bool
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """更新用户信息请求体"""
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None
    github: Optional[str] = None
    twitter: Optional[str] = None
    codepen: Optional[str] = None
    site_name: Optional[str] = None
    site_description: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    """修改密码请求体"""
    old_password: str
    new_password: str
