"""
============================================
热力图 API - 获取最近 N 天的活动数据
============================================
返回每天的文章/动态/评论数量，用于前端热力图展示。
"""

from datetime import datetime, timedelta, date
from fastapi import APIRouter, Query
from app.models.post import Post
from app.models.moment import Moment
from app.models.comment import Comment
from app.models.book import Book
from app.models.motto import Motto
from app.models.user import User

router = APIRouter(prefix="/api/heatmap", tags=["热力图"])


@router.get("")
async def get_heatmap_data(
    days: int = Query(60, ge=1, le=365, description="热力图显示最近天数"),
):
    """
    获取热力图数据（公开）
    返回最近 N 天每天的文章、动态、评论、书籍、语录数量。
    stats.days 显示博客从创建到现在的运行天数。
    """
    today = date.today()
    start_date = today - timedelta(days=days - 1)

    # 获取所有数据
    posts = await Post.all().order_by("-created_at")
    moments = await Moment.all().order_by("-created_at")
    comments = await Comment.all().order_by("-created_at")
    books = await Book.all().order_by("-created_at")
    mottos = await Motto.all().order_by("-created_at")

    # 按日期分组
    result = []
    for i in range(days):
        d = start_date + timedelta(days=i)
        date_str = d.isoformat()

        post_count = sum(1 for p in posts if p.created_at and p.created_at.date() == d)
        moment_count = sum(1 for m in moments if m.created_at and m.created_at.date() == d)
        comment_count = sum(1 for c in comments if c.created_at and c.created_at.date() == d)
        book_count = sum(1 for b in books if b.created_at and b.created_at.date() == d)
        motto_count = sum(1 for m in mottos if m.created_at and m.created_at.date() == d)

        result.append({
            "date": date_str,
            "posts": post_count,
            "moments": moment_count,
            "comments": comment_count,
            "books": book_count,
            "mottos": motto_count,
        })

    # 统计总数
    total_posts = await Post.all().count()
    total_moments = await Moment.all().count()
    total_books = await Book.all().count()
    total_mottos = await Motto.all().count()
    # 博客已运行天数 = 从第一个用户创建到现在的天数（至少 1 天）
    first_user = await User.all().order_by("created_at").first()
    if first_user and first_user.created_at:
        blog_days = max(1, (today - first_user.created_at.date()).days)
    else:
        blog_days = 1

    return {
        "items": result,
        "stats": {
            "days": blog_days,
            "posts": total_posts,
            "moments": total_moments,
            "books": total_books,
            "mottos": total_mottos,
        },
    }
