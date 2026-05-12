"""
============================================
FastAPI 主应用 - 博客后端入口
============================================
使用 Tortoise ORM 作为数据库框架。

启动: python run.py
文档: http://localhost:8000/docs
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import init_db, close_db
from app.core.security import create_default_admin
from app.core.logger import logger
from app.core.config import settings
from app.api import auth, posts, moments, upload, comments, tags, search, heatmap, books, mottos, today, admin, files, feed, likes
from app.api.seed import seed_data

import os


# ============================================
# 应用生命周期管理
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭时的处理"""
    logger.info("博客后端服务启动中...")
    
    # 启动时：初始化数据库
    await init_db()
    await create_default_admin()
    await seed_data()
    logger.info("数据库初始化完成")
    logger.info(f"API 文档: http://localhost:8000/docs")
    logger.info(f"默认管理员: {settings.ADMIN_USERNAME} / {settings.ADMIN_PASSWORD}")
    
    yield  # 应用运行中
    
    # 关闭时：关闭数据库连接
    await close_db()
    logger.info("服务已关闭")


# ============================================
# 创建 FastAPI 应用
# ============================================
app = FastAPI(
    title="魂牵梦绕 - 博客 API",
    description="个人博客系统后端 API 接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ============================================
# CORS 跨域配置
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 注册 API 路由
# ============================================
app.include_router(auth.router)      # /api/auth/*
app.include_router(posts.router)     # /api/posts/*
app.include_router(moments.router)   # /api/moments/*
app.include_router(upload.router)    # /api/upload/*
app.include_router(comments.router)  # /api/comments/*
app.include_router(tags.router)      # /api/tags/*
app.include_router(search.router)    # /api/search/*
app.include_router(heatmap.router)   # /api/heatmap/*
app.include_router(books.router)     # /api/books/*
app.include_router(mottos.router)    # /api/mottos/*
app.include_router(today.router)     # /api/today/*
app.include_router(admin.router)     # /api/admin/*
app.include_router(feed.router)      # /api/feed/*
app.include_router(files.router)     # /api/files/*
app.include_router(likes.router)     # /api/likes/*

# ============================================
# 静态文件服务（上传文件）
# ============================================
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


# ============================================
# 根路径
# ============================================
@app.get("/")
async def root():
    return {
        "name": "魂牵梦绕 - 博客 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "服务运行正常"}
