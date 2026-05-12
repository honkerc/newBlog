"""
============================================
文章模型 - 博客文章
============================================
使用 Tortoise ORM 定义 posts 表。
"""

from tortoise.models import Model
from tortoise import fields


class Post(Model):
    """博客文章模型"""

    # 表名
    class Meta:
        table = "posts"

    # ===== 核心字段 =====
    id = fields.IntField(pk=True, description="文章ID")
    title = fields.CharField(max_length=200, default="无标题", description="文章标题")
    content = fields.TextField(default="", description="Markdown 内容")
    summary = fields.CharField(max_length=500, default="", description="文章摘要")
    cover_url = fields.CharField(max_length=500, default="", description="封面图链接")
    category = fields.CharField(max_length=50, default="", description="分类：技术/生活/随笔")
    tag = fields.CharField(max_length=50, default="", description="标签")

    # ===== 状态 =====
    is_published = fields.BooleanField(default=False, description="是否已发布")
    is_top = fields.BooleanField(default=False, description="是否置顶")
    is_book = fields.BooleanField(default=False, description="是否为书籍介绍")

    # ===== 统计 =====
    view_count = fields.IntField(default=0, description="浏览次数")
    like_count = fields.IntField(default=0, description="点赞次数")

    # ===== 时间 =====
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    published_at = fields.DatetimeField(null=True, description="发布时间")

    def __str__(self):
        return f"<Post {self.id}: {self.title}>"
