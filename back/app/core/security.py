"""
============================================
安全模块 - JWT 认证 + 密码加密
============================================
使用 Tortoise ORM 异步操作数据库。
单用户系统，只有一个管理员账号。

密码加密使用 hashlib.sha256（避免 bcrypt 的 72 字节限制）。
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.logger import logger
from app.models.user import User

# ===== JWT 认证 =====
security_scheme = HTTPBearer(auto_error=False)


# ===== 密码加密（使用 hashlib，避免 bcrypt 72字节限制） =====
def get_password_hash(password: str) -> str:
    """
    密码哈希：sha256(password + salt)
    返回格式: salt$hash
    """
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${pwd_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        salt, pwd_hash = hashed_password.split("$")
        return hashlib.sha256((plain_password + salt).encode()).hexdigest() == pwd_hash
    except (ValueError, AttributeError):
        return False


# ===== JWT 令牌 =====
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT 令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ===== 获取当前用户 =====
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> User:
    """
    获取当前登录用户（异步）
    从请求头提取 JWT 令牌，验证并返回管理员用户。
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请先登录",
        )

    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的认证令牌")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的认证令牌")

    user = await User.get_or_none(id=int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")

    return user


# ===== 创建默认管理员 =====
async def create_default_admin():
    """
    创建默认管理员账号（首次启动时调用）
    单用户系统，如果已存在则跳过。
    """
    existing = await User.get_or_none(username=settings.ADMIN_USERNAME)
    if existing:
        return

    await User.create(
        username=settings.ADMIN_USERNAME,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        is_admin=True,
        nickname="管理员",
        avatar="",
        bio="这个人很懒，什么都没写...",
        site_name="魂牵梦绕",
        site_description="个人博客",
    )
    logger.info(f"管理员账号已创建: {settings.ADMIN_USERNAME}")
