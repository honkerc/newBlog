# Ubuntu 部署指南

将博客系统部署到 Ubuntu 服务器，使用 Docker + Nginx 反向代理，绑定域名 `honkerc.cn`。

---

## 1. 安装 Docker

```bash
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
```

## 2. 安装 Nginx

```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

## 3. 配置 Nginx

```bash
sudo nano /etc/nginx/sites-available/honkerc.cn
```

```nginx
# 前端 (front)
server {
    listen 80;
    server_name honkerc.cn;

    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 移动端 (mini)
server {
    listen 80;
    server_name mini.honkerc.cn;

    location /api/ {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/honkerc.cn /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 4. 配置 SSL（可选）

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d honkerc.cn -d mini.honkerc.cn
```

## 5. 部署

```bash
# 上传项目到服务器
cd /opt
git clone https://github.com/你的用户名/blog.git
cd blog/deploy

# 配置环境变量
cp .env.example .env
nano .env
```

`.env` 文件中的 `SECRET_KEY` 用于 JWT 令牌加密，**务必修改为随机字符串**：

```bash
openssl rand -hex 32
```

```bash
# 启动服务
./deploy.sh
```

## 6. 构建 Android APK

```bash
cd mini
npm run sync          # 构建 Web 资源并同步到 Android
npm run android:open  # 用 Android Studio 打开
```

在 Android Studio 中点击 **Build → Build APK(s)**，生成的 APK 在 `mini/android/app/build/outputs/apk/debug/app-debug.apk`。

> Android 原生应用的 API 地址在 `mini/src/utils/api.js` 中配置，当前为 `http://honkerc.cn`。

## 7. 常用命令

```bash
docker compose logs -f          # 查看日志
docker compose restart          # 重启服务
docker compose down             # 停止服务
docker compose up -d --build    # 更新代码后重新构建
```
