"""
============================================
点赞 API - 动态点赞/取消点赞
============================================
基于 IP 地址记录，无需登录即可点赞。

API:
- POST   /api/likes/{moment_id}  - 点赞/取消点赞（切换）
- GET    /api/likes/{moment_id}  - 查询当前 IP 是否已点赞
"""

from fastapi import APIRouter, HTTPException, status, Request
from app.models.moment import Moment
from app.models.like import Like

router = APIRouter(prefix="/api/likes", tags=["点赞"])


def get_client_ip(request: Request) -> str:
    """获取客户端 IP 地址"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/{moment_id}")
async def toggle_like(moment_id: int, request: Request):
    """点赞/取消点赞（切换）"""
    moment = await Moment.get_or_none(id=moment_id)
    if not moment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="动态不存在")

    ip = get_client_ip(request)

    # 检查是否已点赞
    existing = await Like.get_or_none(moment_id=moment_id, ip_address=ip)

    if existing:
        # 取消点赞
        await existing.delete()
        moment.like_count = max(0, moment.like_count - 1)
        await moment.save()
        return {"liked": False, "like_count": moment.like_count}
    else:
        # 点赞
        await Like.create(moment_id=moment_id, ip_address=ip)
        moment.like_count += 1
        await moment.save()
        return {"liked": True, "like_count": moment.like_count}


@router.get("/{moment_id}")
async def get_like_status(moment_id: int, request: Request):
    """查询当前 IP 是否已点赞"""
    ip = get_client_ip(request)
    liked = await Like.exists(moment_id=moment_id, ip_address=ip)
    return {"liked": liked}
