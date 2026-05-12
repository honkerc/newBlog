"""
============================================
博客后端启动脚本
============================================
使用方式:
    1. 安装依赖: pip install -r requirements.txt
    2. 启动服务: python run.py

启动后访问:
    - API 接口:     http://localhost:8000
    - API 文档:     http://localhost:8000/docs
    - 管理员:       admin / admin123
"""

import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("  魂牵梦绕 - 博客后端")
    print("  Tortoise ORM + FastAPI")
    print("=" * 50)
    print()
    print("  启动服务...")
    print(f"  API:     http://localhost:8000")
    print(f"  文档:    http://localhost:8000/docs")
    print(f"  管理员:  admin / admin123")
    print()
    print("=" * 50)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
