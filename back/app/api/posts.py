"""
============================================
文章 API - 文章的增删改查
============================================
使用 Tortoise ORM 异步操作。

API 列表:
- GET    /api/posts              - 获取文章列表（公开，只返回已发布）
- GET    /api/posts/latest       - 获取最新文章（公开，首页用）
- GET    /api/posts/stats        - 获取文章统计数据（需登录）
- GET    /api/posts/{id}         - 获取文章详情（公开）
- POST   /api/posts              - 创建文章（需登录）
- PUT    /api/posts/{id}         - 更新文章（需登录）
- DELETE /api/posts/{id}         - 删除文章（需登录）
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.security import get_current_user
from app.models.post import Post
from app.models.moment import Moment
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate

router = APIRouter(prefix="/api/posts", tags=["文章"])


# ==================== 公开接口 ====================

@router.get("")
async def list_posts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    category: str = Query("", description="按分类筛选"),
    tag: str = Query("", description="按标签筛选"),
):
    """
    获取文章列表（公开）
    支持分页、分类和标签筛选，默认只返回已发布的。
    """
    query = Post.filter(is_published=True, is_book=False)

    if category:
        query = query.filter(category=category)
    if tag:
        query = query.filter(tag=tag)

    total = await query.count()
    posts = await query.order_by("-created_at").offset((page - 1) * page_size).limit(page_size)

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/books")
async def list_books():
    """
    获取书籍列表（公开）
    返回所有 is_book=True 的文章，按创建时间倒序。
    """
    books = await Post.filter(is_published=True, is_book=True, category="读书").order_by("-created_at").all()
    return {"items": books}


@router.get("/books/{tag}")
async def get_book_detail(tag: str):
    """
    获取书籍详情及其读书笔记（公开）
    根据 tag（书名）查找对应的书籍介绍和所有读书笔记。
    """
    # 查找书籍介绍
    book = await Post.filter(is_published=True, is_book=True, tag=tag, category="读书").first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书籍不存在")

    # 查找该书的读书笔记（is_book=False 且 tag 相同）
    notes = await Post.filter(is_published=True, is_book=False, tag=tag, category="读书").order_by("-created_at").all()

    return {
        "book": book,
        "notes": notes,
    }


@router.get("/latest")
async def list_latest_posts():
    """获取最新文章（首页用，取前3篇已发布的）"""
    posts = await Post.filter(is_published=True, is_book=False).order_by("-created_at").limit(3)
    return {"items": posts}


@router.get("/categories")
async def get_categories():
    """获取文章分类统计（公开，首页用）"""
    from tortoise.functions import Count
    
    categories = await Post.filter(is_published=True, is_book=False).annotate(count=Count("id")).group_by("category").values("category", "count")
    
    # 定义分类图标
    icon_map = {
        "技术": "⚙️",
        "设计": "🎨",
        "生活": "☕",
        "读书": "📖",
        "阅读": "📖",
        "旅行": "✈️",
        "思考": "💭",
    }
    
    result = []
    for cat in categories:
        if cat["category"]:
            result.append({
                "name": cat["category"],
                "icon": icon_map.get(cat["category"], "📄"),
                "count": cat["count"],
            })
    
    return {"items": result}


@router.get("/admin/all")
async def list_all_posts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    category: str = Query("", description="按分类筛选"),
    is_book: bool = Query(None, description="筛选是否为书籍"),
    current_user: User = Depends(get_current_user),
):
    """
    获取所有文章列表（需登录，包括草稿）
    """
    query = Post.all()

    if category:
        query = query.filter(category=category)
    if is_book is not None:
        query = query.filter(is_book=is_book)

    total = await query.count()
    posts = await query.order_by("-created_at").offset((page - 1) * page_size).limit(page_size)

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/stats")
async def get_post_stats(current_user: User = Depends(get_current_user)):
    """获取统计数据（需登录，仪表盘用）"""
    from app.models.comment import Comment
    from tortoise.functions import Sum
    
    post_count = await Post.all().count()
    moment_count = await Moment.all().count()
    comment_count = await Comment.all().count()
    
    # 计算总点赞数
    post_likes = await Post.all().annotate(total_likes=Sum("like_count")).first()
    moment_likes = await Moment.all().annotate(total_likes=Sum("like_count")).first()
    total_likes = (post_likes.total_likes or 0) + (moment_likes.total_likes or 0) if post_likes else 0
    
    return {
        "post_count": post_count,
        "moment_count": moment_count,
        "comment_count": comment_count,
        "total_likes": total_likes,
    }


@router.get("/search")
async def search_posts(
    q: str = Query("", description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
):
    """搜索文章（公开，按标题和内容模糊搜索）"""
    if not q:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}

    query = Post.filter(is_published=True, is_book=False)
    # SQLite 模糊搜索
    posts = await query.filter(
        title__icontains=q
    ).order_by("-created_at").offset((page - 1) * page_size).limit(page_size)

    # 也搜索内容
    content_posts = await query.filter(
        content__icontains=q
    ).order_by("-created_at").all()

    # 合并去重
    seen = set()
    result = []
    for p in posts + content_posts:
        if p.id not in seen:
            seen.add(p.id)
            result.append(p)

    total = len(result)
    result = result[:page_size]

    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/archive")
async def get_archive():
    """获取文章归档（公开，按年月分组）"""
    posts = await Post.filter(is_published=True, is_book=False).order_by("-published_at").all()

    archive = {}
    for p in posts:
        if p.published_at:
            key = p.published_at.strftime("%Y年%m月")
            if key not in archive:
                archive[key] = []
            archive[key].append({
                "id": p.id,
                "title": p.title,
                "published_at": p.published_at.isoformat(),
            })

    result = [{"month": k, "articles": v} for k, v in archive.items()]
    return {"items": result}


@router.get("/{post_id}")
async def get_post(post_id: int):
    """获取文章详情（公开）"""
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    # 增加浏览次数
    post.view_count += 1
    await post.save()

    return post


# ==================== 管理接口（需登录） ====================

@router.post("")
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_user),
):
    """创建文章"""
    post_data = data.dict()
    # 如果已发布，自动设置发布时间
    if post_data.get("is_published") and not post_data.get("published_at"):
        post_data["published_at"] = datetime.now()
    post = await Post.create(**post_data)
    return post


@router.put("/{post_id}")
async def update_post(
    post_id: int,
    data: PostUpdate,
    current_user: User = Depends(get_current_user),
):
    """更新文章"""
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    update_data = data.dict(exclude_unset=True)

    if update_data:
        # 如果设置为已发布且之前未发布，自动设置发布时间
        if update_data.get("is_published") and not post.published_at:
            update_data["published_at"] = datetime.now()
        await post.update_from_dict(update_data)
        await post.save()

    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
):
    """删除文章"""
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")

    await post.delete()
    return {"message": "文章已删除", "id": post_id}
