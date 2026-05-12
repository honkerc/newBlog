# 魂牵梦绕 - 博客后端

基于 **FastAPI + Tortoise ORM** 的个人博客后端 API 服务。

## 📁 目录结构

```
back/
├── app/                    # 应用主目录
│   ├── __init__.py
│   ├── main.py             # FastAPI 入口，注册路由和生命周期
│   │
│   ├── api/                # API 路由层（处理 HTTP 请求）
│   │   ├── __init__.py
│   │   ├── auth.py         # 认证接口：登录、验证令牌
│   │   ├── posts.py        # 文章接口：增删改查（/api/posts/*）
│   │   ├── moments.py      # 动态接口：增删改查（/api/moments/*）
│   │   └── upload.py       # 文件上传接口（/api/upload/*）
│   │
│   ├── models/             # 数据库模型层（Tortoise ORM）
│   │   ├── __init__.py
│   │   ├── post.py         # 文章模型（只有分类，无标签）
│   │   ├── moment.py       # 动态模型
│   │   └── user.py         # 用户模型（单管理员）
│   │
│   ├── schemas/            # 数据验证层（Pydantic）
│   │   ├── __init__.py
│   │   ├── post.py         # 文章创建/更新/响应
│   │   ├── moment.py       # 动态创建/更新/响应
│   │   └── user.py         # 登录请求/令牌响应
│   │
│   └── core/               # 核心功能层
│       ├── __init__.py
│       ├── config.py       # 配置管理（读取 .env）
│       ├── database.py     # Tortoise ORM 连接配置
│       ├── security.py     # JWT 令牌 + 密码加密
│       └── logger.py       # 日志模块（控制台+文件）
│
├── logs/                   # 日志文件目录（自动创建）
├── uploads/                # 上传文件存储目录
├── .env                    # 环境变量配置
├── requirements.txt        # Python 依赖
├── run.py                  # 启动脚本
└── README.md               # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd back
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

编辑 `.env` 文件，可修改：
- 数据库类型（默认 SQLite，无需安装）
- 管理员账号密码（默认 admin / admin123）
- JWT 密钥

### 3. 启动服务

```bash
python run.py
```

服务启动后：
- API 地址: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 管理员: admin / admin123

## 🔌 API 接口列表

### 公开接口（无需登录）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | API 状态检查 |
| GET | `/api/health` | 健康检查 |
| GET | `/api/posts` | 获取文章列表（支持分页、分类筛选） |
| GET | `/api/posts/{id}` | 获取文章详情（自动增加浏览次数） |
| GET | `/api/moments` | 获取动态列表（支持分页） |
| GET | `/api/moments/{id}` | 获取动态详情 |

### 管理接口（需要登录）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 管理员登录 |
| GET | `/api/auth/verify` | 验证令牌 |
| POST | `/api/posts` | 创建文章 |
| PUT | `/api/posts/{id}` | 更新文章 |
| DELETE | `/api/posts/{id}` | 删除文章 |
| POST | `/api/moments` | 创建动态 |
| PUT | `/api/moments/{id}` | 更新动态 |
| DELETE | `/api/moments/{id}` | 删除动态 |
| POST | `/api/upload` | 上传文件 |

## 🔐 认证方式

使用 JWT Bearer Token 认证（单用户系统）：

1. 调用 `POST /api/auth/login` 获取令牌
2. 在请求头中添加: `Authorization: Bearer <token>`

默认管理员账号：`admin` / `admin123`

## 🗄️ 数据库

使用 **Tortoise ORM**（异步 ORM 框架）。

- 开发环境：SQLite（无需安装数据库），文件保存在 `back/blog.db`
- 生产环境：可切换到 MySQL，修改 `.env` 中的 `DATABASE_URL` 即可

### 文章模型（Post）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Int | 主键 |
| title | String(200) | 文章标题 |
| content | Text | Markdown 内容 |
| summary | String(500) | 文章摘要 |
| cover_url | String(500) | 封面图链接 |
| category | String(50) | 分类（技术/生活/随笔） |
| is_published | Boolean | 是否已发布 |
| is_top | Boolean | 是否置顶 |
| view_count | Int | 浏览次数 |
| like_count | Int | 点赞次数 |
| created_at | Datetime | 创建时间 |
| updated_at | Datetime | 更新时间 |
| published_at | Datetime | 发布时间 |

## 📝 日志

日志文件保存在 `back/logs/app.log`，自动按天轮转。

日志格式：`[2026-05-03 23:30:00] INFO app.main - 服务启动成功`

## 💡 前后端交互

前端 `front/src/stores/auth.js` 已配置好 API 地址 `http://localhost:8000`。

确保：
1. 先启动后端: `cd back && python run.py`
2. 再启动前端: `cd front && npm run serve`
3. 访问前端: http://localhost:8080
