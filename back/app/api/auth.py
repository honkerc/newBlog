"""
============================================
认证 API - 管理员登录 + 用户信息
============================================
单用户系统，提供登录、令牌验证、用户信息管理接口。

API:
- POST /api/auth/login       - 管理员登录
- GET  /api/auth/verify      - 验证令牌
- GET  /api/auth/profile     - 获取用户信息
- PUT  /api/auth/profile     - 更新用户信息
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import verify_password, create_access_token, get_current_user, get_password_hash
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserProfileResponse, UserProfileUpdate, ChangePasswordRequest

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    管理员登录
    
    验证用户名密码，返回 JWT 令牌和用户信息。
    默认账号: admin / admin123
    """
    user = await User.get_or_none(username=request.username)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(
        access_token=access_token,
        username=user.username,
        nickname=user.nickname or "",
        avatar=user.avatar or "",
    )


@router.get("/public")
async def get_public_profile():
    """获取公开的用户信息（无需登录，首页用）"""
    user = await User.first()
    if not user:
        return {
            "avatar": "",
            "nickname": "Clay",
            "bio": "高敏天赋者 · 终身学习者 · 重构自我中",
            "github": "",
            "twitter": "",
            "codepen": "",
            "site_name": "魂牵梦绕",
            "site_description": "个人博客",
        }
    return {
        "avatar": user.avatar or "",
        "nickname": user.nickname or "Clay",
        "bio": user.bio or "高敏天赋者 · 终身学习者 · 重构自我中",
        "github": user.github or "",
        "twitter": user.twitter or "",
        "codepen": user.codepen or "",
        "site_name": user.site_name or "魂牵梦绕",
        "site_description": user.site_description or "个人博客",
    }


@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    """验证令牌是否有效，返回用户基本信息"""
    return {
        "valid": True,
        "username": current_user.username,
        "nickname": current_user.nickname or "",
        "avatar": current_user.avatar or "",
    }


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """获取当前用户完整信息"""
    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        nickname=current_user.nickname or "",
        avatar=current_user.avatar or "",
        bio=current_user.bio or "",
        email=current_user.email or "",
        github=current_user.github or "",
        twitter=current_user.twitter or "",
        codepen=current_user.codepen or "",
        site_name=current_user.site_name or "魂牵梦绕",
        site_description=current_user.site_description or "个人博客",
        is_admin=current_user.is_admin,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
    )


@router.put("/password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
):
    """修改密码"""
    if not verify_password(request.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="当前密码错误")
    if len(request.new_password) < 6:
        raise HTTPException(status_code=400, detail="新密码至少 6 位")

    current_user.hashed_password = get_password_hash(request.new_password)
    await current_user.save()
    return {"message": "密码修改成功"}


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
):
    """更新用户信息"""
    update_data = update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="没有需要更新的字段")

    for key, value in update_data.items():
        setattr(current_user, key, value)

    await current_user.save()

    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        nickname=current_user.nickname or "",
        avatar=current_user.avatar or "",
        bio=current_user.bio or "",
        email=current_user.email or "",
        github=current_user.github or "",
        twitter=current_user.twitter or "",
        codepen=current_user.codepen or "",
        site_name=current_user.site_name or "魂牵梦绕",
        site_description=current_user.site_description or "个人博客",
        is_admin=current_user.is_admin,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
    )
