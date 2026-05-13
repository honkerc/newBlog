"""
============================================
测试数据种子 - 生成初始文章和动态数据
============================================
首次启动时调用，如果数据库为空则填充测试数据。

生产环境（ENV=production）只创建一篇 Markdown 语法教程文章。
开发环境填充完整的测试数据。
"""

import os
from app.models.post import Post
from app.models.moment import Moment
from app.models.book import Book
from app.models.motto import Motto
from app.core.logger import logger
from datetime import datetime, timedelta


# ============================================
# 环境判断
# ============================================
IS_PRODUCTION = os.getenv("ENV", "development") == "production"


async def seed_data():
    """填充测试数据（仅当数据库为空时）"""

    post_count = await Post.all().count()

    if IS_PRODUCTION:
        # 生产环境：清空所有数据，只保留一篇 Markdown 教程文章
        # 先删除所有现有数据
        await Post.all().delete()
        await Moment.all().delete()
        await Book.all().delete()
        await Motto.all().delete()

        await Post.create(
            title="Markdown 语法完全指南",
            content="""# Markdown 语法完全指南

这是一篇展示所有 Markdown 语法样式的示例文章，涵盖了常用的 Markdown 格式。

---

## 1. 标题

# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题

---

## 2. 文本样式

**粗体文字** 和 *斜体文字* 以及 ***粗斜体文字***

~~删除线文字~~ 和 ==高亮文字==

这是 `行内代码` 示例

---

## 3. 引用

> 这是一段引用文字
> 可以有多行
>
> > 这是嵌套引用

---

## 4. 列表

### 无序列表

- 苹果
- 香蕉
- 橙子
  - 脐橙
  - 血橙

### 有序列表

1. 第一步
2. 第二步
3. 第三步

### 任务列表

- [x] 已完成任务
- [ ] 未完成任务
- [ ] 待办事项

---

## 5. 代码块

### Python

```python
def hello_world():
    \"\"\"打印 Hello World\"\"\"
    name = "世界"
    print(f"你好, {name}!")
    return True

# 调用函数
hello_world()
```

### JavaScript

```javascript
// 异步函数示例
async function fetchData(url) {
    try {
        const response = await fetch(url)
        const data = await response.json()
        return data
    } catch (error) {
        console.error('请求失败:', error)
        return null
    }
}
```

### CSS

```css
.glass-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
```

### HTML

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>示例页面</title>
</head>
<body>
    <div class="container">
        <h1>你好，世界！</h1>
    </div>
</body>
</html>
```

---

## 6. 表格

| 功能 | 语法 | 示例 |
|------|------|------|
| 粗体 | `**文字**` | **粗体** |
| 斜体 | `*文字*` | *斜体* |
| 链接 | `[文字](url)` | [点击这里](https://example.com) |
| 图片 | `![alt](url)` | ![示例图片](https://picsum.photos/id/1/600/400) |

### 对齐表格

| 左对齐 | 居中对齐 | 右对齐 |
|:-------|:--------:|-------:|
| 左 | 中 | 右 |
| 内容 | 内容 | 内容 |

---

## 7. 链接

[普通链接](https://example.com)

[带标题的链接](https://example.com "鼠标悬停提示")

**自动链接:** <https://example.com>

---

## 8. 图片

![风景图片](httpsAccess to fetch at 'http://mini.honkerc.cn:8000/api/auth/verify' from origin 'http://mini.honkerc.cn' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.了解此错误
:8000/api/auth/verify:1  Failed to load resource: net::ERR_FAILED://picsum.photos/id/101/600/400 "美丽的风景")

![随机图片](https://picsum.photos/id/102/600/400)

---

## 9. 分割线

---

***

___

---

## 10. 脚注

这是一段带有脚注的文字[^1]，这是另一个脚注[^2]。

[^1]: 这是脚注的内容
[^2]: 另一个脚注的详细说明

---

## 11. 数学公式（LaTeX）

行内公式：$E = mc^2$

独立公式：

$$
\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}
$$

---

## 12. 表情符号

:smile: :heart: :rocket: :fire: :star:

:100: :ok_hand: :muscle: :clap:

---

## 13. 定义列表

Markdown
: 一种轻量级标记语言，由 John Gruber 创建

HTML
: 超文本标记语言，网页的基础

CSS
: 层叠样式表，用于控制网页样式

---

## 14. 上标和下标

上标：X^2^ 或 X²

下标：H~2~O 或 H₂O

---

## 15. 折叠详情

<details>
<summary>点击展开查看更多</summary>

这里是折叠的内容，可以包含 **Markdown** 格式。

- 列表项 1
- 列表项 2
- 列表项 3

</details>

---

## 16. 警告块

> **注意：** 这是一个重要的提示信息。
>
> 请仔细阅读相关文档。

> **警告：** 请谨慎操作！
>
> 此操作不可撤销。

---

## 17. 混合排版示例

### 文章卡片

> **文章标题** — *2024年1月*
>
> 这是一篇示例文章的摘要内容。
>
> `阅读更多 →`

### 代码 + 说明

```python
# 斐波那契数列
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
```

> 上面的代码使用生成器实现了斐波那契数列，内存效率更高。

---

## 总结

本文展示了 Markdown 的常用语法，包括：

1. ✅ 标题和文本样式
2. ✅ 引用和列表
3. ✅ 代码块（多语言）
4. ✅ 表格和链接
5. ✅ 图片和分割线
6. ✅ 脚注和数学公式
7. ✅ 表情符号和特殊格式

> Markdown 让写作更专注于内容本身。""",
                summary="一篇展示所有 Markdown 语法样式的完整指南，包括标题、文本样式、代码块、表格、链接、图片、数学公式等 17 种常用格式。",
                cover_url="https://picsum.photos/id/1/600/400",
                category="技术",
                tag="Markdown",
                is_published=True,
                is_top=True,
                view_count=0,
                like_count=0,
                created_at=datetime.now(),
                published_at=datetime.now(),
            )
        logger.info("已创建 Markdown 语法教程文章")
        return

    # ============================================
    # 开发环境：填充完整的测试数据
    # ============================================

    moment_count = await Moment.all().count()
    book_count = await Book.all().count()
    motto_count = await Motto.all().count()

    if post_count > 0 and moment_count > 0 and book_count > 0 and motto_count > 0:
        return

    logger.info("填充测试数据...")

    if post_count == 0:
        posts_data = [
            # ===== 默认文章 1：Markdown 样式展示 =====
            {
                "title": "Markdown 语法完全指南",
                "content": """# Markdown 语法完全指南

这是一篇展示所有 Markdown 语法样式的示例文章，涵盖了常用的 Markdown 格式。

---

## 1. 标题

# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题

---

## 2. 文本样式

**粗体文字** 和 *斜体文字* 以及 ***粗斜体文字***

~~删除线文字~~ 和 ==高亮文字==

这是 `行内代码` 示例

---

## 3. 引用

> 这是一段引用文字
> 可以有多行
>
> > 这是嵌套引用

---

## 4. 列表

### 无序列表

- 苹果
- 香蕉
- 橙子
  - 脐橙
  - 血橙

### 有序列表

1. 第一步
2. 第二步
3. 第三步

### 任务列表

- [x] 已完成任务
- [ ] 未完成任务
- [ ] 待办事项

---

## 5. 代码块

### Python

```python
def hello_world():
    \"\"\"打印 Hello World\"\"\"
    name = "世界"
    print(f"你好, {name}!")
    return True

# 调用函数
hello_world()
```

### JavaScript

```javascript
// 异步函数示例
async function fetchData(url) {
    try {
        const response = await fetch(url)
        const data = await response.json()
        return data
    } catch (error) {
        console.error('请求失败:', error)
        return null
    }
}
```

### CSS

```css
.glass-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
```

### HTML

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>示例页面</title>
</head>
<body>
    <div class="container">
        <h1>你好，世界！</h1>
    </div>
</body>
</html>
```

---

## 6. 表格

| 功能 | 语法 | 示例 |
|------|------|------|
| 粗体 | `**文字**` | **粗体** |
| 斜体 | `*文字*` | *斜体* |
| 链接 | `[文字](url)` | [点击这里](https://example.com) |
| 图片 | `![alt](url)` | ![示例图片](https://picsum.photos/id/1/600/400) |

### 对齐表格

| 左对齐 | 居中对齐 | 右对齐 |
|:-------|:--------:|-------:|
| 左 | 中 | 右 |
| 内容 | 内容 | 内容 |

---

## 7. 链接

[普通链接](https://example.com)

[带标题的链接](https://example.com "鼠标悬停提示")

**自动链接:** <https://example.com>

---

## 8. 图片

![风景图片](https://picsum.photos/id/101/600/400 "美丽的风景")

![随机图片](https://picsum.photos/id/102/600/400)

---

## 9. 分割线

---

***

___

---

## 10. 脚注

这是一段带有脚注的文字[^1]，这是另一个脚注[^2]。

[^1]: 这是脚注的内容
[^2]: 另一个脚注的详细说明

---

## 11. 数学公式（LaTeX）

行内公式：$E = mc^2$

独立公式：

$$
\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}
$$

---

## 12. 表情符号

:smile: :heart: :rocket: :fire: :star:

:100: :ok_hand: :muscle: :clap:

---

## 13. 定义列表

Markdown
: 一种轻量级标记语言，由 John Gruber 创建

HTML
: 超文本标记语言，网页的基础

CSS
: 层叠样式表，用于控制网页样式

---

## 14. 上标和下标

上标：X^2^ 或 X²

下标：H~2~O 或 H₂O

---

## 15. 折叠详情

<details>
<summary>点击展开查看更多</summary>

这里是折叠的内容，可以包含 **Markdown** 格式。

- 列表项 1
- 列表项 2
- 列表项 3

</details>

---

## 16. 警告块

> **注意：** 这是一个重要的提示信息。
>
> 请仔细阅读相关文档。

> **警告：** 请谨慎操作！
>
> 此操作不可撤销。

---

## 17. 混合排版示例

### 文章卡片

> **文章标题** — *2024年1月*
>
> 这是一篇示例文章的摘要内容。
>
> `阅读更多 →`

### 代码 + 说明

```python
# 斐波那契数列
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
```

> 上面的代码使用生成器实现了斐波那契数列，内存效率更高。

---

## 总结

本文展示了 Markdown 的常用语法，包括：

1. ✅ 标题和文本样式
2. ✅ 引用和列表
3. ✅ 代码块（多语言）
4. ✅ 表格和链接
5. ✅ 图片和分割线
6. ✅ 脚注和数学公式
7. ✅ 表情符号和特殊格式

> Markdown 让写作更专注于内容本身。""",
                "summary": "一篇展示所有 Markdown 语法样式的完整指南，包括标题、文本样式、代码块、表格、链接、图片、数学公式等 17 种常用格式。",
                "cover_url": "https://picsum.photos/id/1/600/400",
                "category": "技术",
                "tag": "Markdown",
                "is_published": True,
                "is_top": True,
                "view_count": 256,
                "like_count": 89,
                "created_at": datetime.now() - timedelta(days=1),
                "published_at": datetime.now() - timedelta(days=1),
            },
            # ===== 默认文章 2：博客功能点介绍 =====
            {
                "title": "魂牵梦绕 · 博客功能全览",
                "content": """# 魂牵梦绕 · 博客功能全览

欢迎来到「魂牵梦绕」个人博客系统！本文详细介绍博客的所有功能和使用方法。

---

## 📝 文章系统

### 文章分类

博客文章分为三大类：

| 分类 | 说明 | 标签示例 |
|------|------|----------|
| **技术** | 编程、开发相关 | Vue, Python, CSS, TypeScript |
| **生活** | 日常记录、随笔 | 日精进, 咖啡, 旅行 |
| **思考** | 深度思考、感悟 | 独立开发, 人生感悟 |
| **读书** | 书籍介绍和读书笔记 | 原子习惯, 心流, 人类简史 |

### 文章功能

- ✅ **Markdown 渲染** — 支持完整的 Markdown 语法
- ✅ **代码高亮** — 支持多种编程语言
- ✅ **文章置顶** — 重要文章可以置顶显示
- ✅ **分类筛选** — 按分类和标签筛选文章
- ✅ **阅读统计** — 自动记录每篇文章的阅读次数

---

## 📖 读书模块

### 书籍管理

- **书籍介绍** — 展示书籍封面、作者、简介
- **读书笔记** — 为每本书写多篇读书笔记
- **标签关联** — 通过标签将书籍和笔记关联

### 使用方式

1. 在「读书」页面浏览所有书籍
2. 点击书籍查看详情和所有相关笔记
3. 在管理后台添加新书和笔记

---

## 💬 动态（朋友圈）

### 动态分类

| 分类 | 图标 | 说明 |
|------|------|------|
| **朋友圈** | 📸 | 生活照片、日常分享 |
| **运动** | 🏃 | 运动打卡、健身记录 |
| **日常** | ☀️ | 日常琐事、心情记录 |
| **学习** | 🎓 | 学习进度、知识分享 |

### 动态功能

- ✅ **图片上传** — 支持多图上传
- ✅ **分类筛选** — 按分类查看动态
- ✅ **点赞功能** — 基于 IP 的点赞，无需登录
- ✅ **评论互动** — 支持评论交流
- ✅ **图片预览** — 点击图片可放大查看

---

## 📅 今日记录

「今日」页面汇总当天的所有记录：

- 📌 今日打卡（动态）
- 📌 今日语录（一句话）
- 📌 今日文章（日精进/读书笔记）

---

## 💡 一句话（语录）

简约的语录展示页面，每天一句好句子。

- **随机展示** — 每次刷新随机显示
- **来源标注** — 显示语录出处或地点
- **管理后台** — 可增删改语录

---

## 🔍 搜索功能

全局搜索，支持：

- 文章标题搜索
- 文章内容搜索
- 实时搜索结果

---

## 📊 热力图

展示近 60 天的活动记录：

- 颜色越深，活动越多
- 鼠标悬停查看具体日期
- 直观了解自己的活跃度

---

## 🎨 设计特色

### 黑色生命力主题

- 深色背景，护眼舒适
- 绿色点缀（#00F2C0），充满生机
- 玻璃拟态卡片效果
- 流畅的过渡动画

### 响应式设计

- 桌面端：完整布局
- 平板端：自适应调整
- 手机端：优化触控体验

---

## 📱 Mini 版（移动端）

专为手机优化的轻量版本：

- **打卡** — 快速记录今日动态
- **今日** — 查看今日所有记录
- **一句话** — 随手记录灵感
- **文章** — 浏览和发布文章
- **读书** — 管理书籍和笔记

---

## 🔐 管理后台

### 功能列表

| 功能 | 说明 |
|------|------|
| **仪表盘** | 数据统计概览 |
| **文章管理** | 增删改查文章 |
| **动态管理** | 管理朋友圈动态 |
| **书籍管理** | 管理书籍和笔记 |
| **语录管理** | 管理一句话 |
| **文件管理** | 上传和管理文件 |
| **个人设置** | 修改个人信息和密码 |

### 访问方式

1. 点击底部「登录」按钮
2. 输入管理员账号密码
3. 进入管理后台

---

## 🚀 技术栈

### 前端

- **Vue 3** — 组合式 API
- **Vue Router** — 路由管理
- **Font Awesome** — 图标库

### 后端

- **FastAPI** — 高性能异步框架
- **Tortoise ORM** — 异步 ORM
- **SQLite** — 轻量数据库
- **JWT** — 认证机制

### 部署

- **Nginx** — 反向代理
- **Docker** — 容器化部署

---

## 💝 感谢使用

> 愿这个博客能陪伴你记录生活的每一个美好瞬间。

如有问题或建议，欢迎在评论区留言！""",
                "summary": "「魂牵梦绕」个人博客系统的完整功能指南，涵盖文章、读书、动态、今日记录、一句话、搜索、热力图等所有功能模块。",
                "cover_url": "https://picsum.photos/id/26/600/400",
                "category": "技术",
                "tag": "博客",
                "is_published": True,
                "is_top": True,
                "view_count": 189,
                "like_count": 76,
                "created_at": datetime.now() - timedelta(days=1),
                "published_at": datetime.now() - timedelta(days=1),
            },
            {
                "title": "Vue 3 组合式 API 最佳实践",
                "content": "## 前言\n\nComposition API 是 Vue 3 最重要的新特性之一。本文将深入探讨如何在实际项目中组织组合式函数。\n\n## 为什么使用 Composition API？\n\n- 更好的逻辑复用\n- 更灵活的代码组织\n- 更好的 TypeScript 支持\n\n## 总结\n\nComposition API 让 Vue 开发更加灵活和可维护。",
                "summary": "深入探讨 Composition API 在实际项目中的组织方式，以及如何写出可维护、可复用的组合函数。",
                "cover_url": "https://picsum.photos/id/1/600/400",
                "category": "技术",
                "tag": "Vue",
                "is_published": True,
                "is_top": True,
                "view_count": 128,
                "like_count": 42,
                "created_at": datetime.now() - timedelta(days=2),
                "published_at": datetime.now() - timedelta(days=2),
            },
            {
                "title": "玻璃拟态设计指南",
                "content": "## 什么是玻璃拟态？\n\n玻璃拟态（Glassmorphism）是一种通过背景模糊和半透明效果模拟玻璃质感的 UI 设计风格。\n\n## 核心原理\n\n```css\n.glass-card {\n  background: rgba(255, 255, 255, 0.1);\n  backdrop-filter: blur(20px);\n  border: 1px solid rgba(255, 255, 255, 0.1);\n  border-radius: 16px;\n}\n```\n\n## 最佳实践\n\n1. 使用深色背景衬托玻璃效果\n2. 模糊值建议在 10-30px 之间\n3. 边框透明度控制在 0.05-0.15",
                "summary": "从原理到实践，详解如何打造优雅的玻璃拟态 UI，以及在不同场景下的应用技巧。",
                "cover_url": "https://picsum.photos/id/26/600/400",
                "category": "设计",
                "tag": "UI",
                "is_published": True,
                "is_top": False,
                "view_count": 96,
                "like_count": 38,
                "created_at": datetime.now() - timedelta(days=5),
                "published_at": datetime.now() - timedelta(days=5),
            },
            {
                "title": "秋天的第一杯咖啡",
                "content": "周末去了家新开的咖啡馆，手冲哥伦比亚，果香四溢。\n\n窗外的银杏叶黄了，秋天真的来了。\n\n## 咖啡馆清单\n\n- 手冲哥伦比亚\n- 冰滴冷萃\n- 澳白\n\n每一杯都是不同的心情。",
                "summary": "周末去了家新开的咖啡馆，手冲哥伦比亚，果香四溢。窗外的银杏叶黄了，秋天真的来了。",
                "cover_url": "https://picsum.photos/id/431/600/400",
                "category": "生活",
                "tag": "咖啡",
                "is_published": True,
                "is_top": False,
                "view_count": 72,
                "like_count": 56,
                "created_at": datetime.now() - timedelta(days=8),
                "published_at": datetime.now() - timedelta(days=8),
            },
            # ===== 读书 - 书籍介绍（is_book=True） =====
            {
                "title": "《设计中的设计》",
                "content": "## 关于本书\n\n**作者：** 原研哉\n**出版年份：** 2003年\n**类别：** 设计理论\n\n### 内容简介\n\n《设计中的设计》是日本著名设计师原研哉的代表作。书中探讨了设计的本质——设计不是一种技能，而是感知世界的方式。\n\n### 核心观点\n\n- 设计不是填充，而是留白\n- 简约不是简单，而是极致的提炼\n- 好的设计让人感觉不到设计的存在\n- \"空\"的概念是日本设计的精髓\n\n### 推荐理由\n\n如果你对设计感兴趣，这本书会让你重新思考什么是好的设计。原研哉对\"空\"的理解让人印象深刻。",
                "summary": "原研哉经典设计著作，探讨设计的本质：设计不是一种技能，而是感知世界的方式。",
                "cover_url": "https://picsum.photos/id/20/600/400",
                "category": "读书",
                "tag": "设计中的设计",
                "is_published": True,
                "is_top": False,
                "is_book": True,
                "view_count": 55,
                "like_count": 33,
                "created_at": datetime.now() - timedelta(days=10),
                "published_at": datetime.now() - timedelta(days=10),
            },
            {
                "title": "《人类简史》",
                "content": "## 关于本书\n\n**作者：** 尤瓦尔·赫拉利\n**出版年份：** 2014年\n**类别：** 历史/社科\n\n### 内容简介\n\n《人类简史》以宏大的视角讲述了从认知革命到科学革命的人类发展史。\n\n### 三大革命\n\n1. **认知革命**（7万年前）—— 智人能够讨论虚构的事物，从而大规模合作\n2. **农业革命**（1.2万年前）—— 历史上最大的骗局，让更多人用更糟的方式生活\n3. **科学革命**（500年前）—— 承认无知，使欧洲人征服世界\n\n### 推荐理由\n\n这本书会颠覆你对人类历史的认知。我们以为自己在进步，但也许只是在换一种方式受苦。",
                "summary": "尤瓦尔·赫拉利用宏大的视角重新诠释了人类历史，从认知革命到科学革命，颠覆你对\"进步\"的认知。",
                "cover_url": "https://picsum.photos/id/0/600/400",
                "category": "读书",
                "tag": "人类简史",
                "is_published": True,
                "is_top": False,
                "is_book": True,
                "view_count": 89,
                "like_count": 45,
                "created_at": datetime.now() - timedelta(days=15),
                "published_at": datetime.now() - timedelta(days=15),
            },
            {
                "title": "《原子习惯》",
                "content": "## 关于本书\n\n**作者：** James Clear\n**出版年份：** 2018年\n**类别：** 自我提升\n\n### 内容简介\n\n《原子习惯》提供了建立好习惯、打破坏习惯的实用框架。\n\n### 习惯的四步模型\n\n1. **提示** —— 让习惯显而易见\n2. **渴望** —— 让习惯有吸引力\n3. **回应** —— 让习惯简便易行\n4. **奖励** —— 让习惯令人愉悦\n\n### 核心原则\n\n**1% 法则**：每天进步1%，一年后你会进步37倍。\n\n### 推荐理由\n\n与其做意志力的战士，不如做环境的建筑师。这本书会改变你对习惯的认知。",
                "summary": "James Clear 经典之作：每天进步1%，一年后你会进步37倍。环境设计比意志力更重要。",
                "cover_url": "https://picsum.photos/id/24/600/400",
                "category": "读书",
                "tag": "原子习惯",
                "is_published": True,
                "is_top": False,
                "is_book": True,
                "view_count": 156,
                "like_count": 78,
                "created_at": datetime.now() - timedelta(days=20),
                "published_at": datetime.now() - timedelta(days=20),
            },
            {
                "title": "《心流》",
                "content": "## 关于本书\n\n**作者：** 米哈里·契克森米哈赖\n**出版年份：** 1990年\n**类别：** 心理学\n\n### 内容简介\n\n《心流》探讨了最优体验的心理学，揭示了幸福的真正来源。\n\n### 什么是心流？\n\n心流是一种完全沉浸在某项活动中的状态，时间感消失，自我意识消失。\n\n### 心流的条件\n\n- 明确的目标\n- 即时的反馈\n- 挑战与技能的平衡\n\n### 推荐理由\n\n> 幸福不是偶然发生的，也不是金钱和权力能够买到的。它不取决于外部事件，而取决于我们如何解释它们。",
                "summary": "米哈里·契克森米哈赖的经典之作。幸福不是偶然发生的，而是取决于我们如何解释和体验生活。",
                "cover_url": "https://picsum.photos/id/26/600/400",
                "category": "读书",
                "tag": "心流",
                "is_published": True,
                "is_top": False,
                "is_book": True,
                "view_count": 112,
                "like_count": 56,
                "created_at": datetime.now() - timedelta(days=25),
                "published_at": datetime.now() - timedelta(days=25),
            },
            {
                "title": "《刻意练习》",
                "content": "## 关于本书\n\n**作者：** 安德斯·埃里克森\n**出版年份：** 2016年\n**类别：** 自我提升/心理学\n\n### 内容简介\n\n《刻意练习》揭示了天才的真正秘密——不是天赋，而是正确的练习方法。\n\n### 刻意练习 vs 天真的练习\n\n- **天真的练习**：重复做同样的事，期待进步\n- **刻意练习**：有目标、有反馈、有改进的练习\n\n### 刻意练习的四个特点\n\n1. 有明确的目标\n2. 专注\n3. 包含反馈\n4. 走出舒适区\n\n### 推荐理由\n\n> 天才不是天生的，而是练出来的。关键在于方法而非天赋。",
                "summary": "安德斯·埃里克森的研究表明，天才不是天生的，而是通过刻意练习培养出来的。关键在于方法而非天赋。",
                "cover_url": "https://picsum.photos/id/36/600/400",
                "category": "读书",
                "tag": "刻意练习",
                "is_published": True,
                "is_top": False,
                "is_book": True,
                "view_count": 98,
                "like_count": 52,
                "created_at": datetime.now() - timedelta(days=30),
                "published_at": datetime.now() - timedelta(days=30),
            },
            # ===== 读书 - 读书笔记（is_book=False，tag 对应书名） =====
            {
                "title": "《设计中的设计》读书笔记",
                "content": "原研哉对\"空\"的理解让人印象深刻。\n\n好的设计不是填充，而是留白。\n\n## 核心观点\n\n- 设计不是一种技能，而是感知世界的方式\n- 简约不是简单，而是极致的提炼\n- 好的设计让人感觉不到设计的存在\n\n读完后对 minimalism 有了新的认识。",
                "summary": "原研哉对\"空\"的理解让人印象深刻。好的设计不是填充，而是留白。读完后对 minimalism 有了新的认识。",
                "cover_url": "",
                "category": "读书",
                "tag": "设计中的设计",
                "is_published": True,
                "is_top": False,
                "is_book": False,
                "view_count": 55,
                "like_count": 33,
                "created_at": datetime.now() - timedelta(days=10),
                "published_at": datetime.now() - timedelta(days=10),
            },
            {
                "title": "《人类简史》读书笔记：从动物到上帝",
                "content": "## 认知革命\n\n大约7万年前，智人发生了认知革命，能够讨论虚构的事物，从而能够大规模合作。\n\n## 农业革命\n\n农业革命是历史上最大的骗局，它让更多的人以更糟糕的方式生活。\n\n## 科学革命\n\n科学革命的核心是承认无知，这使欧洲人能够征服世界。\n\n## 读后感\n\n这本书让我重新审视了人类的历史。我们以为自己在进步，但也许只是在换一种方式受苦。",
                "summary": "从认知革命到科学革命，尤瓦尔·赫拉利用宏大的视角重新诠释了人类历史。读完让人对\"进步\"有了新的思考。",
                "cover_url": "",
                "category": "读书",
                "tag": "人类简史",
                "is_published": True,
                "is_top": False,
                "is_book": False,
                "view_count": 89,
                "like_count": 45,
                "created_at": datetime.now() - timedelta(days=14),
                "published_at": datetime.now() - timedelta(days=14),
            },
            {
                "title": "《人类简史》读后感：虚构的力量",
                "content": "## 虚构的力量\n\n智人之所以能统治世界，不是因为个体更强大，而是因为能大规模合作。而大规模合作的基础是——相信虚构的故事。\n\n## 公司、金钱、国家\n\n- 公司是一个法律虚构\n- 金钱是一个共同相信的故事\n- 国家是一个想象的共同体\n\n## 思考\n\n我们生活在自己编织的故事里。这些故事让陌生人能够合作，但也让我们被故事束缚。",
                "summary": "智人之所以能统治世界，不是因为个体更强大，而是因为能大规模合作。而合作的基础是相信虚构的故事。",
                "cover_url": "",
                "category": "读书",
                "tag": "人类简史",
                "is_published": True,
                "is_top": False,
                "is_book": False,
                "view_count": 67,
                "like_count": 38,
                "created_at": datetime.now() - timedelta(days=13),
                "published_at": datetime.now() - timedelta(days=13),
            },
            {
                "title": "《原子习惯》精读笔记",
                "content": "## 习惯的四步模型\n\n1. 提示 - 让习惯显而易见\n2. 渴望 - 让习惯有吸引力\n3. 回应 - 让习惯简便易行\n4. 奖励 - 让习惯令人愉悦\n\n## 核心原则\n\n**1% 法则**：每天进步1%，一年后你会进步37倍。\n\n## 习惯叠加\n\n将新习惯与现有习惯绑定：\n\n> 在[现有习惯]之后，我将[新习惯]。\n\n## 环境设计\n\n与其做意志力的战士，不如做环境的建筑师。",
                "summary": "James Clear 的原子习惯法则：每天进步1%，一年后你会进步37倍。环境设计比意志力更重要。",
                "cover_url": "",
                "category": "读书",
                "tag": "原子习惯",
                "is_published": True,
                "is_top": False,
                "is_book": False,
                "view_count": 156,
                "like_count": 78,
                "created_at": datetime.now() - timedelta(days=19),
            },
            {
                "title": "《心流》读书笔记：最优体验的心理学",
                "content": "## 什么是心流？\n\n心流是一种完全沉浸在某项活动中的状态，时间感消失，自我意识消失。\n\n## 心流的条件\n\n- 明确的目标\n- 即时的反馈\n- 挑战与技能的平衡\n\n## 如何进入心流\n\n1. 设定清晰的目标\n2. 专注于当下\n3. 寻找适度的挑战\n4. 培养对活动的内在兴趣\n\n> 幸福不是偶然发生的，也不是金钱和权力能够买到的。它不取决于外部事件，而取决于我们如何解释它们。",
                "summary": "米哈里·契克森米哈赖的经典之作。幸福不是偶然发生的，而是取决于我们如何解释和体验生活。",
                "cover_url": "",
                "category": "读书",
                "tag": "心流",
                "is_published": True,
                "is_top": False,
                "is_book": False,
                "view_count": 112,
                "like_count": 56,
                "created_at": datetime.now() - timedelta(days=24),
                "published_at": datetime.now() - timedelta(days=24),
            },
            {
                "title": "《刻意练习》读书笔记",
                "content": "## 刻意练习 vs 天真的练习\n\n- 天真的练习：重复做同样的事，期待进步\n- 刻意练习：有目标、有反馈、有改进的练习\n\n## 刻意练习的四个特点\n\n1. 有明确的目标\n2. 专注\n3. 包含反馈\n4. 走出舒适区\n\n## 心理表征\n\n专家和新手的区别在于心理表征的质量。\n\n> 天才不是天生的，而是练出来的。",
                "summary": "安德斯·埃里克森的研究表明，天才不是天生的，而是通过刻意练习培养出来的。关键在于方法而非天赋。",
                "cover_url": "",
                "category": "读书",
                "tag": "刻意练习",
                "is_published": True,
                "is_top": False,
                "is_book": False,
                "view_count": 98,
                "like_count": 52,
                "created_at": datetime.now() - timedelta(days=29),
                "published_at": datetime.now() - timedelta(days=29),
            },
            # ===== 日精进 =====
            {
                "title": "Day 1：开始写日精进",
                "content": "## 为什么要写日精进？\n\n从今天开始，每天记录自己的成长和思考。\n\n## 今天的收获\n\n1. 完成了博客系统的读书页面开发\n2. 学习了 Vue 3 的组合式 API\n3. 读了一篇关于时间管理的文章\n\n## 明日计划\n\n- 继续完善博客功能\n- 读《原子习惯》第三章\n\n> 种一棵树最好的时间是十年前，其次是现在。",
                "summary": "从今天开始，每天记录自己的成长和思考。完成了博客系统的读书页面开发，学习了 Vue 3 的组合式 API。",
                "cover_url": "",
                "category": "生活",
                "tag": "日精进",
                "is_published": True,
                "is_top": False,
                "view_count": 34,
                "like_count": 12,
                "created_at": datetime.now() - timedelta(days=1),
                "published_at": datetime.now() - timedelta(days=1),
            },
            {
                "title": "Day 2：关于专注力的思考",
                "content": "## 今日感悟\n\n今天尝试了番茄工作法，25分钟专注 + 5分钟休息，效率确实提高了不少。\n\n## 专注力的四个杀手\n\n1. 手机通知 - 关掉所有非必要通知\n2. 多任务切换 - 一次只做一件事\n3. 完美主义 - 先完成再完美\n4. 环境干扰 - 创造安静的工作环境\n\n## 今日完成\n\n- [x] 完成博客日精进页面\n- [x] 读《原子习惯》30分钟\n- [ ] 运动30分钟\n\n> 专注不是天赋，是习惯。",
                "summary": "尝试了番茄工作法，效率确实提高了。总结了专注力的四个杀手：手机通知、多任务切换、完美主义、环境干扰。",
                "cover_url": "",
                "category": "思考",
                "tag": "日精进",
                "is_published": True,
                "is_top": False,
                "view_count": 28,
                "like_count": 18,
                "created_at": datetime.now() - timedelta(days=2),
                "published_at": datetime.now() - timedelta(days=2),
            },
            {
                "title": "Day 3：写作的力量",
                "content": "## 为什么要写作？\n\n写作是最好的思考方式。当你把想法写下来时，你才能真正理清思路。\n\n## 写作的四个层次\n\n1. 记录 - 把发生的事情记下来\n2. 反思 - 思考为什么发生\n3. 总结 - 提炼出可复用的经验\n4. 创造 - 产生新的想法\n\n## 今日金句\n\n> 写作不是为了传递思想，而是为了思考。\n\n## 今日完成\n\n- [x] 写了三篇读书笔记\n- [x] 优化了博客的 Markdown 渲染\n- [x] 跑步 5 公里",
                "summary": "写作是最好的思考方式。今天写了三篇读书笔记，优化了博客的 Markdown 渲染，还跑了 5 公里。",
                "cover_url": "https://picsum.photos/id/48/600/400",
                "category": "生活",
                "tag": "日精进",
                "is_published": True,
                "is_top": False,
                "view_count": 42,
                "like_count": 25,
                "created_at": datetime.now() - timedelta(days=3),
                "published_at": datetime.now() - timedelta(days=3),
            },
            {
                "title": "Day 4：学会拒绝",
                "content": "## 今日感悟\n\n学会拒绝是一种能力。不是所有的事情都值得做，不是所有的请求都需要答应。\n\n## 如何优雅地拒绝\n\n1. 明确自己的优先级\n2. 给出简短的理由\n3. 提供替代方案\n4. 不要过度道歉\n\n## 今日完成\n\n- [x] 拒绝了不必要的会议\n- [x] 完成了核心功能的开发\n- [x] 读完了《原子习惯》\n\n> 你的时间就是你的生命，别让别人浪费它。",
                "summary": "学会拒绝是一种能力。今天拒绝了不必要的会议，完成了核心功能开发，读完了《原子习惯》。",
                "cover_url": "",
                "category": "思考",
                "tag": "日精进",
                "is_published": True,
                "is_top": False,
                "view_count": 31,
                "like_count": 20,
                "created_at": datetime.now() - timedelta(days=4),
                "published_at": datetime.now() - timedelta(days=4),
            },
            {
                "title": "Day 5：周末复盘",
                "content": "## 本周复盘\n\n### 做得好的 👍\n\n1. 坚持写了 5 天的日精进\n2. 完成了博客的两个新页面\n3. 读了 2 本书\n\n### 需要改进的 👎\n\n1. 运动时间不够\n2. 睡眠质量需要提升\n3. 手机使用时间过长\n\n### 下周计划\n\n1. 每天运动 30 分钟\n2. 11 点前睡觉\n3. 读完《心流》\n\n> 复盘不是批评自己，而是为了更好地前进。",
                "summary": "本周复盘：坚持写了 5 天日精进，完成了博客新页面，读了 2 本书。下周目标是每天运动、早睡、读完《心流》。",
                "cover_url": "",
                "category": "生活",
                "tag": "日精进",
                "is_published": True,
                "is_top": False,
                "view_count": 47,
                "like_count": 32,
                "created_at": datetime.now() - timedelta(days=5),
                "published_at": datetime.now() - timedelta(days=5),
            },
            {
                "title": "从零搭建个人博客",
                "content": "记录从选型到部署的全过程。\n\n## 技术栈\n\n- 前端：Vue 3 + Vite\n- 后端：FastAPI + Tortoise ORM\n- 数据库：SQLite\n\n## 部署流程\n\n1. 购买域名和服务器\n2. 配置 Nginx 反向代理\n3. 使用 Docker 部署\n4. 配置 HTTPS",
                "summary": "记录从选型到部署的全过程，包括 Vue 3、Vite、Markdown 渲染、评论系统等。",
                "cover_url": "https://picsum.photos/id/60/600/400",
                "category": "技术",
                "tag": "博客",
                "is_published": True,
                "is_top": False,
                "view_count": 203,
                "like_count": 67,
                "created_at": datetime.now() - timedelta(days=12),
                "published_at": datetime.now() - timedelta(days=12),
            },
            {
                "title": "关于独立开发的思考",
                "content": "离开大厂一年了，从焦虑到从容。\n\n独立开发不只是写代码，更是对生活方式的重新定义。\n\n## 这一年我学到了\n\n1. 时间管理比技术更重要\n2. 做减法比做加法难\n3. 保持输出才能持续进步",
                "summary": "离开大厂一年了，从焦虑到从容。独立开发不只是写代码，更是对生活方式的重新定义。",
                "cover_url": "https://picsum.photos/id/20/600/400",
                "category": "思考",
                "tag": "独立开发",
                "is_published": False,
                "is_top": False,
                "view_count": 45,
                "like_count": 89,
                "created_at": datetime.now() - timedelta(days=18),
                "published_at": None,
            },
            {
                "title": "CSS Grid 布局完全掌握",
                "content": "从基础概念到高级技巧，用大量实例带你彻底搞懂 CSS Grid 布局。\n\n## 基础概念\n\n```css\n.container {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  gap: 16px;\n}\n```\n\n## 高级技巧\n\n- 命名网格线\n- 隐式网格\n- 自动填充",
                "summary": "从基础概念到高级技巧，用大量实例带你彻底搞懂 CSS Grid 布局。",
                "cover_url": "https://picsum.photos/id/36/600/400",
                "category": "技术",
                "tag": "CSS",
                "is_published": True,
                "is_top": False,
                "view_count": 167,
                "like_count": 71,
                "created_at": datetime.now() - timedelta(days=22),
                "published_at": datetime.now() - timedelta(days=22),
            },
            {
                "title": "TypeScript 类型体操入门",
                "content": "从基础类型到高级泛型，一步步掌握 TypeScript 类型系统的精髓。\n\n## 基础类型\n\n```typescript\ntype User = {\n  id: number\n  name: string\n  email: string\n}\n```\n\n## 高级技巧\n\n- 条件类型\n- 映射类型\n- 模板字面量类型",
                "summary": "从基础类型到高级泛型，一步步掌握 TypeScript 类型系统的精髓。",
                "cover_url": "https://picsum.photos/id/0/600/400",
                "category": "技术",
                "tag": "TypeScript",
                "is_published": True,
                "is_top": False,
                "view_count": 134,
                "like_count": 63,
                "created_at": datetime.now() - timedelta(days=28),
                "published_at": datetime.now() - timedelta(days=28),
            },
        ]

        for data in posts_data:
            await Post.create(**data)
        logger.info(f"{len(posts_data)} 篇文章已创建")

    if moment_count == 0:
        moments_data = [
            {
                "category": "moment",
                "content": "周末去了趟海边，日落时分的光线真的太美了。海浪声、海风声，还有远处传来的吉他声，一切都刚刚好。",
                "images": "https://picsum.photos/id/101/600/400,https://picsum.photos/id/102/600/400,https://picsum.photos/id/103/600/400",
                "is_published": True,
                "like_count": 28,
                "comment_count": 5,
                "created_at": datetime.now() - timedelta(hours=2),
            },
            {
                "category": "moment",
                "content": "新买了一把机械键盘，打字手感太棒了。深夜写代码的快乐又回来了 ⌨️✨",
                "images": "https://picsum.photos/id/60/600/400",
                "is_published": True,
                "like_count": 15,
                "comment_count": 3,
                "created_at": datetime.now() - timedelta(days=1),
            },
            {
                "category": "moment",
                "content": "今天尝试做了一道新菜——番茄牛腩，味道还不错！果然做饭和写代码一样，都需要耐心和调试 😄",
                "images": "https://picsum.photos/id/292/600/400,https://picsum.photos/id/312/600/400",
                "is_published": True,
                "like_count": 42,
                "comment_count": 8,
                "created_at": datetime.now() - timedelta(days=3),
            },
            {
                "category": "moment",
                "content": "读完了《设计中的设计》，原研哉对\"空\"的理解让人印象深刻。好的设计不是填充，而是留白。",
                "images": "",
                "is_published": True,
                "like_count": 33,
                "comment_count": 2,
                "created_at": datetime.now() - timedelta(days=5),
            },
            {
                "category": "moment",
                "content": "秋天的第一杯咖啡 ☕️ 配上窗外的落叶，氛围感拉满。",
                "images": "https://picsum.photos/id/431/600/400,https://picsum.photos/id/36/600/400,https://picsum.photos/id/48/600/400,https://picsum.photos/id/57/600/400",
                "is_published": True,
                "like_count": 56,
                "comment_count": 12,
                "created_at": datetime.now() - timedelta(days=7),
            },
            {
                "category": "fitness",
                "content": "晨跑 5 公里，配速 5'30\"，感觉状态不错。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(hours=3),
            },
            {
                "category": "reading",
                "content": "读《原子习惯》第三章：如何建立好习惯。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(hours=2),
            },
            {
                "category": "study",
                "content": "学习了 Vue 3 的 Teleport 和 Suspense 组件。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(hours=1),
            },
            {
                "category": "fitness",
                "content": "健身房力量训练 1 小时：胸+三头。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=1),
            },
            {
                "category": "reading",
                "content": "读《心流》第二章：意识与注意力。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=1),
            },
            {
                "category": "daily",
                "content": "今天完成了博客的打卡功能开发。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=2),
            },
            {
                "category": "fitness",
                "content": "游泳 1 小时，自由泳 1500 米。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=3),
            },
            {
                "category": "reading",
                "content": "读《刻意练习》第四章：心理表征。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=3),
            },
            {
                "category": "study",
                "content": "学习了 FastAPI 的依赖注入系统。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=4),
            },
            {
                "category": "daily",
                "content": "整理了书桌和书架，断舍离了 5 本书。",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=5),
            },
        ]

        for data in moments_data:
            await Moment.create(**data)
        logger.info(f"{len(moments_data)} 条动态已创建")

    if book_count == 0:
        books_data = [
            {
                "title": "设计中的设计",
                "author": "原研哉",
                "cover_url": "https://picsum.photos/id/20/600/400",
                "summary": "日本著名设计师原研哉的代表作，探讨设计的本质——设计不是一种技能，而是感知世界的方式。",
                "view_count": 55,
                "like_count": 33,
                "created_at": datetime.now() - timedelta(days=10),
            },
            {
                "title": "人类简史",
                "author": "尤瓦尔·赫拉利",
                "cover_url": "https://picsum.photos/id/0/600/400",
                "summary": "以宏大的视角讲述了从认知革命到科学革命的人类发展史，颠覆你对\"进步\"的认知。",
                "view_count": 89,
                "like_count": 45,
                "created_at": datetime.now() - timedelta(days=15),
            },
            {
                "title": "原子习惯",
                "author": "James Clear",
                "cover_url": "https://picsum.photos/id/24/600/400",
                "summary": "每天进步1%，一年后你会进步37倍。环境设计比意志力更重要。",
                "view_count": 156,
                "like_count": 78,
                "created_at": datetime.now() - timedelta(days=20),
            },
            {
                "title": "心流",
                "author": "米哈里·契克森米哈赖",
                "cover_url": "https://picsum.photos/id/26/600/400",
                "summary": "幸福不是偶然发生的，而是取决于我们如何解释和体验生活。",
                "view_count": 112,
                "like_count": 56,
                "created_at": datetime.now() - timedelta(days=25),
            },
            {
                "title": "刻意练习",
                "author": "安德斯·埃里克森",
                "cover_url": "https://picsum.photos/id/36/600/400",
                "summary": "天才不是天生的，而是通过刻意练习培养出来的。关键在于方法而非天赋。",
                "view_count": 98,
                "like_count": 52,
                "created_at": datetime.now() - timedelta(days=30),
            },
        ]

        for data in books_data:
            await Book.create(**data)
        logger.info(f"{len(books_data)} 本书籍已创建")

    if motto_count == 0:
        mottos_data = [
            {
                "content": "种一棵树最好的时间是十年前，其次是现在。",
                "location": "书房",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=1),
            },
            {
                "content": "生活不是等待暴风雨过去，而是学会在雨中翩翩起舞。",
                "location": "咖啡馆",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=3),
            },
            {
                "content": "世界上只有一种真正的英雄主义，那就是在认清生活真相之后依然热爱生活。",
                "location": "罗曼·罗兰",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=7),
            },
            {
                "content": "人生没有白走的路，每一步都算数。",
                "location": "书房",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=14),
            },
            {
                "content": "愿你历尽千帆，归来仍是少年。",
                "location": "路上",
                "is_published": True,
                "created_at": datetime.now() - timedelta(days=21),
            },
        ]

        for data in mottos_data:
            await Motto.create(**data)
        logger.info(f"{len(mottos_data)} 条语录已创建")

    logger.info("测试数据填充完成")
