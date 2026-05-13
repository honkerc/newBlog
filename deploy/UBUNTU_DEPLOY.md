# Ubuntu 部署指南

将博客系统部署到 Ubuntu 服务器，使用 systemd 管理服务 + Nginx 反向代理，绑定域名 `honkerc.cn`。

---

## 1. 安装依赖

```bash
# Python
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx

# Node.js (用于构建前端)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt install -y nodejs
```

## 2. 克隆项目

```bash
cd /opt
sudo git clone https://github.com/你的用户名/blog.git
sudo chown -R $USER:$USER blog
cd blog     
```

## 3. 配置后端

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r back/requirements.txt
pip install uvicorn     

# 配置环境变量
cp back/.env back/.env.production
nano back/.env.production
```

`.env.production` 内容：

```ini
DATABASE_URL=sqlite:///blog.db
SECRET_KEY=你的随机密钥
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ADMIN_USERNAME=admin
ADMIN_PASSWORD=你的密码
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
BASE_URL=http://honkerc.cn
ENV=production
```

生成 SECRET_KEY：

```bash
openssl rand -hex 32
```

## 4. 构建前端

```bash
# 构建 front
cd front
npm install
npm run build

# 构建 mini
cd ../mini
npm install
npm run build
```

## 5. 配置 Nginx

```bash
sudo nano /etc/nginx/sites-available/honkerc.cn
```

```nginx
# 前端 (front)
server {
    listen 80;
    server_name honkerc.cn;

    # 客户端上传大小限制（10MB）
    client_max_body_size 10M;

    # 前端静态文件
    root /opt/blog/front/dist;
    index index.html;

    # API 反向代理到后端（CORS 由后端 FastAPI 处理）
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 上传文件（反向代理到后端，由后端处理文件服务）
    location /uploads/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # SPA 路由
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# 移动端 (mini)
server {
    listen 80;
    server_name mini.honkerc.cn;

    # 客户端上传大小限制（10MB）
    client_max_body_size 10M;

    root /opt/blog/mini/dist;
    index index.html;

    # API 反向代理到后端（CORS 由后端 FastAPI 处理）
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 上传文件（反向代理到后端，由后端处理文件服务）
    location /uploads/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        expires 30d;
        add_header Cache-Control
}
```

```bash
sudo ln -s /etc/nginx/sites-available/honkerc.cn /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 6. 配置 SSL（可选）

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d honkerc.cn -d mini.honkerc.cn
```

## 7. 创建 systemd 服务

```bash
sudo nano /etc/systemd/system/blog-backend.service
```

```ini
[Unit]
Description=Blog Backend API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/blog/back
EnvironmentFile=/opt/blog/back/.env.production
ExecStart=/opt/blog/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable blog-backend
sudo systemctl start blog-backend
```

## 8. 初始化数据

```bash
cd /opt/blog
source venv/bin/activate
python -c "
from app.database import init_db
from app.security import create_default_admin
from app.api.seed import seed_data
import asyncio

async def init():
    await init_db()
    await create_default_admin()
    await seed_data()
    print('初始化完成！')

asyncio.run(init())
"
```

## 9. 更新代码

```bash
cd /opt/blog
git pull                    # 拉取最新代码

# 更新后端
source venv/bin/activate
pip install -r back/requirements.txt  # 更新依赖
sudo systemctl restart blog-backend   # 重启后端

# 更新前端
cd front
npm install
npm run build

cd ../mini
npm install
npm run build
```

## 10. 常用命令

```bash
sudo systemctl status blog-backend    # 查看后端状态
sudo systemctl restart blog-backend   # 重启后端
sudo systemctl stop blog-backend      # 停止后端
sudo journalctl -u blog-backend -f    # 查看后端日志
sudo systemctl reload nginx           # 重载 Nginx
```
