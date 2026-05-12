"""
============================================
用户模型 - 单管理员账号
============================================
使用 Tortoise ORM 定义 users 表。
单用户系统，只有一个管理员账号。
包含头像、昵称、简介等个人信息。
"""

from tortoise.models import Model
from tortoise import fields


class User(Model):
    """管理员用户模型（单用户）"""

    class Meta:
        table = "users"

    # ===== 账号 =====
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    hashed_password = fields.CharField(max_length=255, description="加密后的密码")
    is_admin = fields.BooleanField(default=True, description="是否为管理员")

    # ===== 个人信息 =====
    nickname = fields.CharField(max_length=100, default="", description="昵称")
    avatar = fields.CharField(max_length=500, default="", description="头像URL")
    bio = fields.CharField(max_length=500, default="", description="个人简介")
    email = fields.CharField(max_length=200, default="", description="邮箱")
    github = fields.CharField(max_length=500, default="", description="GitHub 链接")
    twitter = fields.CharField(max_length=500, default="", description="Twitter 链接")
    codepen = fields.CharField(max_length=500, default="", description="CodePen 链接")
    site_name = fields.CharField(max_length=100, default="魂牵梦绕", description="站点名称")
    site_description = fields.CharField(max_length=500, default="个人博客", description="站点描述")

    # ===== 时间 =====
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    def __str__(self):
        return f"<User {self.username}>"
