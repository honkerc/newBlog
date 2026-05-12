"""
============================================
评论模型 - 文章评论
============================================
使用 Tortoise ORM 定义 comments 表。
支持嵌套回复（通过 parent_id）。
"""

from tortoise.models import Model
from tortoise import fields


class Comment(Model):
    """文章评论模型"""

    class Meta:
        table = "comments"

    # ===== 核心字段 =====
    id = fields.IntField(pk=True, description="评论ID")
    post_id = fields.IntField(description="关联文章ID")
    author = fields.CharField(max_length=50, default="匿名", description="评论者名称")
    email = fields.CharField(max_length=200, default="", description="评论者邮箱")
    content = fields.TextField(default="", description="评论内容")
    parent_id = fields.IntField(null=True, description="回复的评论ID")

    # ===== 状态 =====
    is_approved = fields.BooleanField(default=True, description="是否审核通过")

    # ===== 时间 =====
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    def __str__(self):
        return f"<Comment {self.id} on Post {self.post_id}>"
