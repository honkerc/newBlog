"""
============================================
数据库配置 - Tortoise ORM
============================================
使用 Tortoise ORM 管理数据库连接。
Tortoise 是异步 ORM，支持 SQLite / MySQL / PostgreSQL。

配置参考:
    TORTOISE_ORM = {
        "connections": {"default": "sqlite://./blog.db"},
        "apps": {"models": {"models": ["app.models", "aerich.models"], "default_connection": "default"}},
    }
"""

from tortoise import Tortoise
from app.core.config import settings


# ===== Tortoise ORM 配置 =====
TORTOISE_CONFIG = {
    "connections": {
        "default": settings.DATABASE_URL,  # 从 .env 读取
    },
    "apps": {
        "models": {
            "models": [
                "app.models.post",    # 文章模型
                "app.models.moment",  # 动态模型
                "app.models.user",    # 用户模型
                "app.models.comment", # 评论模型
                "app.models.tag",     # 标签模型
                "app.models.book",    # 书籍模型
                "app.models.motto",   # 一句话模型
            ],
            "default_connection": "default",
        },
    },
    # SQLite 需要这个设置来支持多线程
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}


async def init_db():
    """
    初始化数据库连接并创建表
    
    应用启动时调用，会自动创建所有表（如果不存在）。
    """
    await Tortoise.init(config=TORTOISE_CONFIG)
    # 创建表（如果不存在）
    await Tortoise.generate_schemas(safe=True)


async def close_db():
    """
    关闭数据库连接
    
    应用关闭时调用，释放数据库资源。
    """
    await Tortoise.close_connections()
