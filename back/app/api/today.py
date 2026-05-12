"""
============================================
今日记录 API - 获取今天创建的所有内容
============================================
"""

from datetime import datetime, date
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.motto import Motto
from app.models.post import Post
from app.models.moment import Moment
from app.models.user import User

router = APIRouter(prefix="/api/today", tags=["今日记录"])


@router.get("")
async def get_today_summary(current_user: User = Depends(get_current_user)):
    """获取今日创建的所有记录（打卡、一句话、日精进、读书笔记）"""
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())

    # 今日打卡（动态）
    checkins = await Moment.filter(
        created_at__gte=today_start,
        created_at__lte=today_end,
    ).order_by("-created_at").all()

    # 今日一句话
    mottos = await Motto.filter(
        created_at__gte=today_start,
        created_at__lte=today_end,
    ).order_by("-created_at").all()

    # 今日文章（日精进 + 读书笔记）
    posts = await Post.filter(
        created_at__gte=today_start,
        created_at__lte=today_end,
        is_book=False,
    ).order_by("-created_at").all()

    return {
        "checkins": checkins,
        "mottos": mottos,
        "posts": posts,
    }
