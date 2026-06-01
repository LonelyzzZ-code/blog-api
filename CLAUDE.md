# CLAUDE.md

这是 blog-api 项目，基于 FastAPI 的博客后端服务。

## 技术栈

- **Web 框架**: FastAPI（异步 ASGI 框架）
- **服务器**: Uvicorn
- **ORM**: SQLAlchemy（同步模式，非 async）
- **数据校验**: Pydantic（与 FastAPI 深度集成）
- **缓存**: Redis（可选，用于热点数据缓存、访问量统计）
- **配置管理**: python-dotenv（`.env` 文件）

## 项目结构

```
E:\blog-api\
├── requirements.txt          ← 依赖清单
├── app\
│   ├── __init__.py
│   ├── main.py               ← 应用入口，FastAPI 实例化，挂载路由
│   ├── config.py             ← 配置管理（DB URL、Redis URL、密钥等，从 .env 读取）
│   ├── database.py           ← SQLAlchemy Engine + SessionLocal，依赖注入 get_db
│   ├── redis.py              ← Redis 连接与工具函数（可选模块）
│   ├── models\
│   │   ├── __init__.py
│   │   ├── article.py        ← 文章 ORM 模型（title, content, created_at 等）
│   │   └── comment.py        ← 评论 ORM 模型（关联 article_id, 点赞数等）
│   ├── schemas\
│   │   ├── __init__.py
│   │   ├── article.py        ← 文章的 Pydantic Schema（Create/Update/Response）
│   │   └── comment.py        ← 评论的 Pydantic Schema（Create/Response）
│   └── routers\
│       ├── __init__.py
│       ├── articles.py       ← 文章 CRUD 接口
│       ├── comments.py       ← 评论 + 点赞接口
│       └── stats.py          ← 访问量统计接口
```

## 约定

- **路由前缀**: 文章 `/api/articles`，评论 `/api/comments`，统计 `/api/stats`
- **数据库**: 使用同步 SQLAlchemy（`session.execute()` / `session.add()`），每个请求通过 FastAPI 依赖注入获取独立 session
- **Schema 命名**: `ArticleCreate`、`ArticleUpdate`、`ArticleResponse`，评论同理
- **模型**: 表名用蛇形命名（snake_case），公共字段抽到 Base 类
- **Redis**: 可选启用，如果 `REDIS_URL` 未配置则优雅降级，不阻塞主流程
- **环境变量**: 所有配置通过 `config.py` 统一读取，不支持硬编码

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器（热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 格式化与代码检查（预留）
# black app/
# ruff check app/
```

## 编码风格

- 使用 Python 类型注解（type hints），所有函数签名标注参数和返回值类型
- 路由函数用 `def`（非 `async def`），因为 SQLAlchemy 同步 session 会阻塞事件循环
- 错误处理返回统一的 JSON 格式：`{"detail": "错误描述"}`
- 不写无意义的注释，代码自解释优先
- imports 顺序：标准库 → 第三方库 → 本地模块

## 注意事项

- 这是新项目，所有 `.py` 文件内容待填充
- `app/CLAUDE.md` 已存在但为空，如需子目录级指令可在那里补充
- 涉及到 .env、数据库密码、密钥等敏感信息，不要在对话中暴露
- 代码生成参考：C:\Users\伍活豪\Desktop\blog-api-代码生成指南.txt，生成/修改任何文件前先对照该指南
- 知识点笔记：C:\Users\伍活豪\Desktop\项目笔记\，遇到不懂的概念简洁整理后归档于此
