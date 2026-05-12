"""
============================================
动态模型 - 朋友圈/打卡/日常记录
============================================
使用 Tortoise ORM 定义 moments 表。
"""

from tortoise.models import Model
from tortoise import fields


class Moment(Model):
    """动态模型"""

    class Meta:
        table = "moments"

    # ===== 核心字段 =====
    id = fields.IntField(pk=True, description="动态ID")
    category = fields.CharField(max_length=50, default="moment", description="动态类别: moment/sports/daily/study")
    content = fields.TextField(default="", description="动态内容（Markdown）")
    images = fields.CharField(max_length=1000, default="", description="图片链接，逗号分隔")

    # ===== 状态 =====
    is_published = fields.BooleanField(default=True, description="是否可见")
    is_top = fields.BooleanField(default=False, description="是否置顶")

    # ===== 统计 =====
    like_count = fields.IntField(default=0, description="点赞次数")
    comment_count = fields.IntField(default=0, description="评论次数")

    # ===== 时间 =====
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    def __str__(self):
        return f"<Moment {self.id}: {self.category}>"
