from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.routers import articles, comments, stats

app = FastAPI(
    title = settings.APP_TITLE,
    version=settings.APP_VERSION,
)

# ==================== CORS 中间件 ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许前端开发服务器
    allow_credentials=True,
    allow_methods=["*"],                     # 允许所有 HTTP 方法
    allow_headers=["*"],                     # 允许所有请求头
)

# ==================== 挂载路由 ====================
app.include_router(articles.router)
app.include_router(comments.router)
app.include_router(stats.router)

# ==================== 启动事件 ====================
@app.on_event("startup")
def startup():
    """应用启动时自动执行：创建所有数据库表"""
    Base.metadata.create_all(bind = engine)

#==================== 健康检查 ====================
@app.get("/")
def root():
    """根路径，用于检查服务是否在运行"""
    return {"message": "Blog API is running", "version": settings.APP_VERSION}
