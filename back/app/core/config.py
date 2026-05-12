"""
============================================
配置文件 - 管理所有环境变量和全局设置
============================================
这个文件负责从 .env 文件读取配置，
所有其他模块都从这里获取配置信息。
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


class Settings:
    """
    应用配置类
    
    所有配置项都集中在这里，方便管理和修改。
    使用方式: from app.core import settings
    """

    # ===== 数据库配置 =====
    # 数据库连接地址，从 .env 读取，默认使用 SQLite
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite://./blog.db")

    # ===== JWT 认证配置 =====
    # 用于签名 JWT 令牌的密钥（生产环境一定要改！）
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    # 加密算法
    ALGORITHM: str = "HS256"
    # 令牌过期时间（分钟），默认 24 小时
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # ===== 管理员账号 =====
    # 首次启动时自动创建管理员用户
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")

    # ===== 文件上传配置 =====
    # 上传文件存储目录
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    # 最大上传大小（字节），默认 10MB
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))
    # 后端服务地址（用于拼接完整 URL）
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")


# 创建全局配置实例
# 其他模块通过 `from app.core import settings` 使用
settings = Settings()
