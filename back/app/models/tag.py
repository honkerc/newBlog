"""
============================================
标签模型 - 文章标签
============================================
使用 Tortoise ORM 定义 tags 和 post_tags 表。
多对多关系：一篇文章可以有多个标签，一个标签可以属于多篇文章。
"""

from tortoise.models import Model
from tortoise import fields


class Tag(Model):
    """标签模型"""

    class Meta:
        table = "tags"

    id = fields.IntField(pk=True, description="标签ID")
    name = fields.CharField(max_length=50, unique=True, description="标签名称")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    def __str__(self):
        return f"<Tag {self.name}>"


class PostTag(Model):
    """文章-标签关联表"""

    class Meta:
        table = "post_tags"

    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField("models.Post", related_name="post_tags", description="文章")
    tag = fields.ForeignKeyField("models.Tag", related_name="post_tags", description="标签")

    def __str__(self):
        return f"<PostTag post={self.post_id} tag={self.tag_id}>"
