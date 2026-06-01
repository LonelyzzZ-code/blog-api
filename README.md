# blog-api

基于 FastAPI 的博客后端 API，与 [blog-web](https://github.com/LonelyzzZ-code/blog-web) 配套使用。

## 技术栈

- **Python 3.10+**
- **FastAPI** — Web 框架
- **SQLAlchemy** — ORM
- **Pydantic** — 数据校验
- **Redis** — 缓存（可选）
- **Uvicorn** — ASGI 服务器

## 功能

- 文章 CRUD
- 评论 + 点赞
- 访问量统计
- API 文档（Swagger 自动生成）

## 快速开始

```bash
# 克隆
git clone https://github.com/LonelyzzZ-code/blog-api.git
cd blog-api

# 虚拟环境
python -m venv venv
venv\Scripts\activate       # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选，复制 .env.example）
cp .env.example .env

# 启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

启动后访问：
- API 文档：http://localhost:8000/docs
- 根路径：http://localhost:8000/

## 项目结构

```
app/
├── main.py          # 入口，挂载路由
├── config.py        # 配置管理（.env）
├── database.py      # 数据库连接 + 依赖注入
├── redis.py         # Redis 工具（可选）
├── models/          # ORM 模型
├── schemas/         # Pydantic 数据校验
└── routers/         # API 路由
```

## 路由

| 前缀 | 功能 |
|------|------|
| `/api/articles` | 文章 CRUD |
| `/api/comments` | 评论 + 点赞 |
| `/api/stats` | 访问量统计 |

## License

MIT
