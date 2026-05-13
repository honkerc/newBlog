# 魂牵梦绕 · 个人博客系统

一个功能完整的个人博客系统，包含桌面端（Front）和移动端（Mini/Android App），支持文章管理、动态（朋友圈）、读书笔记、打卡、语录等功能。

## 技术栈

| 模块 | 技术 |
|------|------|
| **前端 (Front)** | Vue 3 + Vue Router + TipTap 编辑器 |
| **移动端 (Mini)** | Vue 3 + Capacitor (Android App) |
| **后端** | FastAPI + Tortoise ORM + SQLite |
| **部署** | Nginx + systemd / Docker |

## 功能特性

### 📝 文章系统
- Markdown 富文本编辑（基于 TipTap）
- 文章分类与标签
- 文章置顶、阅读统计
- 代码高亮、表格、任务列表

### 💬 动态（朋友圈）
- 多图上传与缩略图
- 分类筛选（朋友圈、运动、日常、学习）
- 点赞（基于 IP）、评论
- 图片预览

### 📖 读书模块
- 书籍管理（封面、作者、简介）
- 读书笔记（多篇笔记关联一本书）
- 标签关联

### 📅 今日记录
- 每日打卡汇总
- 今日语录、今日文章
- 热力图展示活动记录

### 💡 一言（语录）
- 随机展示语录
- 来源标注

### 🔐 管理后台
- 仪表盘数据统计
- 文章、动态、书籍、语录管理
- 文件管理、个人设置

### 📱 移动端 (Mini)
- 打卡、今日、一言、精进、读书
- 支持 Android App（Capacitor）
- 可配置后端服务器地址

## 项目结构

```
blog/
├── back/                    # 后端 (FastAPI)
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── auth.py     # 认证
│   │   │   ├── posts.py    # 文章
│   │   │   ├── moments.py  # 动态
│   │   │   ├── books.py    # 书籍
│   │   │   ├── mottos.py   # 语录
│   │   │   ├── upload.py   # 文件上传
│   │   │   ├── comments.py # 评论
│   │   │   ├── likes.py    # 点赞
│   │   │   ├── search.py   # 搜索
│   │   │   ├── heatmap.py  # 热力图
│   │   │   ├── feed.py     # 动态流
│   │   │   ├── today.py    # 今日记录
│   │   │   ├── tags.py     # 标签
│   │   │   ├── files.py    # 文件管理
│   │   │   ├── admin.py    # 管理后台
│   │   │   └── seed.py     # 测试数据
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 配置
│   │   │   ├── database.py # 数据库
│   │   │   ├── security.py # 安全
│   │   │   └── logger.py   # 日志
│   │   └── models/         # 数据模型
│   ├── uploads/            # 上传文件目录
│   └── requirements.txt
│
├── front/                   # 桌面端 (Vue 3)
│   ├── src/
│   │   ├── views/          # 页面
│   │   ├── components/     # 组件
│   │   ├── utils/          # 工具
│   │   ├── router/         # 路由
│   │   └── stores/         # 状态管理
│   └── public/
│
├── mini/                    # 移动端 (Vue 3 + Capacitor)
│   ├── src/
│   │   ├── views/          # 页面
│   │   └── utils/          # 工具
│   ├── android/            # Android 原生项目
│   └── capacitor.config.json
│
├── deploy/                  # 部署配置
│   ├── docker-compose.yml
│   ├── Dockerfile.*
│   └── nginx.*.conf
│
└── uploads/                 # 上传文件（开发环境）
```

## 快速开始

### 开发环境

```bash
# 1. 启动后端
cd back
pip install -r requirements.txt
python run.py
# 访问 http://localhost:8000/docs 查看 API 文档

# 2. 启动前端
cd front
npm install
npm run serve
# 访问 http://localhost:8080

# 3. 启动移动端
cd mini
npm install
npm run serve
# 访问 http://localhost:8081
```

### 环境变量

创建 `back/.env` 文件：

```ini
DATABASE_URL=sqlite:///blog.db
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-password
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
BASE_URL=http://localhost:8000
ENV=development
```

### 生产部署

详见 [deploy/UBUNTU_DEPLOY.md](deploy/UBUNTU_DEPLOY.md)

## API 概览

| 端点 | 说明 |
|------|------|
| `POST /api/auth/login` | 管理员登录 |
| `GET/POST /api/posts` | 文章列表/创建 |
| `GET/PUT/DELETE /api/posts/{id}` | 文章详情/更新/删除 |
| `GET/POST /api/moments` | 动态列表/创建 |
| `GET/POST /api/books` | 书籍列表/创建 |
| `GET/POST /api/mottos` | 语录列表/创建 |
| `POST /api/upload` | 文件上传 |
| `GET /api/today` | 今日记录汇总 |
| `GET /api/heatmap` | 热力图数据 |
| `GET /api/search` | 全局搜索 |

## 设计特色

- **黑色生命力主题** — 深色背景 + 绿色点缀（#00F2C0）
- **玻璃拟态** — 毛玻璃卡片效果
- **响应式布局** — 桌面端、平板、手机自适应
- **黑客打字机** — 首页终端风格动画
- **多主题切换** — 11 种主题色

## License

MIT
