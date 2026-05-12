"""
============================================
日志模块 - 记录应用运行日志
============================================
提供统一的日志记录功能，支持控制台输出和文件记录。

使用方式:
    from app.core.logger import logger
    logger.info("服务启动成功")
    logger.error("数据库连接失败", exc_info=True)
"""

import sys
import logging
from pathlib import Path

# ===== 日志目录 =====
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"

# 确保日志目录存在
LOG_DIR.mkdir(exist_ok=True)


def setup_logger() -> logging.Logger:
    """
    配置并返回日志记录器
    
    日志格式: [2026-05-03 23:30:00] INFO app.main - 服务启动成功
    """
    logger = logging.getLogger("blog")
    logger.setLevel(logging.DEBUG)

    # 日志格式
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ---- 控制台输出 ----
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    # 设置编码为 utf-8，避免 GBK 编码错误
    if hasattr(console_handler, 'stream') and hasattr(console_handler.stream, 'reconfigure'):
        try:
            console_handler.stream.reconfigure(encoding='utf-8')
        except Exception:
            pass
    logger.addHandler(console_handler)

    # ---- 文件输出 ----
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# 创建全局日志实例
logger = setup_logger()
