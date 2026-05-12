"""
============================================
一句话模型 - 简短语录/签名
============================================
"""

from tortoise.models import Model
from tortoise import fields


class Motto(Model):
    """一句话/语录模型"""

    class Meta:
        table = "mottos"

    # ===== 核心字段 =====
    id = fields.IntField(pk=True, description="ID")
    content = fields.TextField(description="语录内容")
    location = fields.CharField(max_length=200, default="", description="地点")
    images = fields.CharField(max_length=1000, default="", description="图片链接，逗号分隔")

    # ===== 状态 =====
    is_published = fields.BooleanField(default=True, description="是否可见")

    # ===== 时间 =====
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    def __str__(self):
        return f"<Motto {self.id}: {self.content[:30]}>"
