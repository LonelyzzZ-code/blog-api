from fastapi import FastAPI
from app.database import engine, Base
from app.config import settings
from app.routers import articles, comments, stats

app = FastAPI(
    title = settings.APP_TITLE, 
    version=settings.APP_VERSION,
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
