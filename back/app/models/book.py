"""
============================================
书籍模型 - 独立于文章的书籍管理
============================================
使用 Tortoise ORM 定义 books 表。
"""

from tortoise.models import Model
from tortoise import fields


class Book(Model):
    """书籍模型"""

    class Meta:
        table = "books"

    # ===== 核心字段 =====
    id = fields.IntField(pk=True, description="书籍ID")
    title = fields.CharField(max_length=200, description="书名")
    author = fields.CharField(max_length=100, default="", description="作者")
    cover_url = fields.CharField(max_length=500, default="", description="封面图链接")
    summary = fields.TextField(default="", description="书籍简介（支持 Markdown）")

    # ===== 统计 =====
    view_count = fields.IntField(default=0, description="浏览次数")
    like_count = fields.IntField(default=0, description="点赞次数")

    # ===== 时间 =====
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    def __str__(self):
        return f"<Book {self.id}: {self.title}>"
