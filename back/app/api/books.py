"""
============================================
书籍 API - 独立于文章的书籍管理
============================================
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/api/books", tags=["书籍"])


# ============================================
# 公开接口
# ============================================

@router.get("", response_model=dict)
async def get_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """获取书籍列表（公开）"""
    total = await Book.all().count()
    books = (
        await Book.all()
        .order_by("-created_at")
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return {
        "items": [BookResponse.model_validate(b).model_dump() for b in books],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int):
    """获取书籍详情（公开）"""
    book = await Book.get_or_none(id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    return book


@router.get("/by-tag/{tag}", response_model=dict)
async def get_book_by_tag(tag: str):
    """通过 tag 获取书籍详情（兼容旧版，tag 即书名）"""
    book = await Book.get_or_none(title=tag)
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")

    # 查找关联的读书笔记（通过 tag 字段匹配的文章）
    from app.models.post import Post
    notes = await Post.filter(tag=tag, is_published=True).order_by("-created_at")

    from app.schemas.post import PostResponse
    return {
        "book": BookResponse.model_validate(book).model_dump(),
        "notes": [PostResponse.model_validate(n).model_dump() for n in notes],
    }


# ============================================
# 管理接口（需认证）
# ============================================

@router.post("", response_model=BookResponse)
async def create_book(data: BookCreate, _=Depends(get_current_user)):
    """创建书籍"""
    book = await Book.create(**data.model_dump())
    return book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, data: BookUpdate, _=Depends(get_current_user)):
    """更新书籍"""
    book = await Book.get_or_none(id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")

    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        await book.update_from_dict(update_data).save()
        await book.refresh_from_db()

    return book


@router.delete("/{book_id}")
async def delete_book(book_id: int, _=Depends(get_current_user)):
    """删除书籍"""
    book = await Book.get_or_none(id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    await book.delete()
    return {"message": "书籍已删除", "id": book_id}
