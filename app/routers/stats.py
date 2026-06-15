from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article
from app import redis

router = APIRouter(prefix="/api/stats", tags=["stats"])

# ==================== 单篇文章访问量 ====================
@router.get("/views")
def get_article_views(
    article_id: int = Query(...,description = "文章ID"),
    db: Session = Depends(get_db)
):
    """
    获取某篇文章的访问量
    优先从Redis取，Redis 没有再从数据库取
    Args:
        article_id (int, optional): 文章id. Defaults to Query(...,description = "文章ID").
        db (Session, optional): 创建数据库接口. Defaults to Depends(get_db).
    """
    views = redis.get_views(article_id)
    if views is None:
        article = db.query(Article).filter(Article.id == article_id).first()
        views = article.views if article else 0
    return {"article_id": article_id, "views": views}

# ==================== 访问量排行榜 ====================
@router.get("/top")
def get_top_articles(
    limit: int = Query(10, ge = 1, le = 50),
    db: Session = Depends(get_db)
):
    """
    返回访问量最高的 N 篇文章，直接从数据库查
    Args:
        limit (int, optional): 文章数量限制. Defaults to Query(10, ge = 1, le = 50).
        db (Session, optional): 创建数据库接口. Defaults to Depends(get_db).
    """
    articles = (
        db.query(Article)
        .order_by(Article.views.desc())
        .limit(limit)
        .all()
    )
    return [
        {"id": a.id, "title": a.title, "views": a.views}
        for a in articles
    ]