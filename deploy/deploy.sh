#!/bin/bash
# ============================================
# 博客系统 - 一键部署脚本
# ============================================
# 使用方式:
#   chmod +x deploy.sh
#   ./deploy.sh
# ============================================

set -e

echo "============================================"
echo "  魂牵梦绕 - 博客系统部署"
echo "============================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "[错误] 未安装 Docker，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "[错误] 未安装 docker-compose，请先安装 docker-compose"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "[提示] 未找到 .env 文件，从 .env.example 创建..."
    cp .env.example .env
    echo "[警告] 请修改 .env 文件中的配置（特别是 SECRET_KEY 和 ADMIN_PASSWORD）"
    echo ""
    read -p "按回车键继续使用默认配置部署，或 Ctrl+C 取消后修改 .env 文件..."
fi

# 加载环境变量
set -a
source .env 2>/dev/null || true
set +a

echo "[1/3] 构建 Docker 镜像..."
docker-compose build

echo ""
echo "[2/3] 启动服务..."
docker-compose up -d

echo ""
echo "[3/3] 检查服务状态..."
sleep 3
docker-compose ps

echo ""
echo "============================================"
echo "  部署完成！"
echo "============================================"
echo ""
echo "  访问地址:"
echo "  前端 (front):  http://localhost:8080"
echo "  前端 (mini):   http://localhost:3001"
echo "  API 后端:      http://localhost:8000"
echo "  API 文档:      http://localhost:8000/docs"
echo ""
echo "  管理命令:"
echo "  查看日志:  docker-compose logs -f"
echo "  重启服务:  docker-compose restart"
echo "  停止服务:  docker-compose down"
echo ""
echo "============================================"
