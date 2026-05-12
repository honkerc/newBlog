"""
============================================
点赞模型 - 记录用户对动态的点赞
============================================
使用 Tortoise ORM 定义 likes 表。
基于 IP 地址记录，无需登录即可点赞。
"""

from tortoise.models import Model
from tortoise import fields


class Like(Model):
    """点赞记录"""

    class Meta:
        table = "likes"
        unique_together = (("moment_id", "ip_address"),)

    id = fields.IntField(pk=True, description="点赞ID")
    moment_id = fields.IntField(description="动态ID")
    ip_address = fields.CharField(max_length=64, description="点赞者IP")
    created_at = fields.DatetimeField(auto_now_add=True, description="点赞时间")

    def __str__(self):
        return f"<Like {self.id}: moment={self.moment_id}>"
