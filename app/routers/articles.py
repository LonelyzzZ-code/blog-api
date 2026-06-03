from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article, Comment
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from app import redis

router = APIRouter(prefix = "/api/articles",tags = ["articles"])

@router.get("/")#以/为路径，GET方式向服务器发送请求(写在函数上面，不能分离于函数存在)
def list_articles(
        page :int = Query(1,ge = 1),
        page_size :int = Query(10 , ge = 1, le = 100),
        db :Session = Depends(get_db)
):
        """
        分页获取文章列表
        - page: 第几页，默认 1
        - page_size: 每页几条，默认 10，最大 100
        - 按创建时间倒序（最新的排前面）
        Args:
            page (_type_, optional):页数. Defaults to Query(1,ge = 1)
            page_size:每页的行数int=Query(10 , ge = 1, le = 100)
            db:Session=Depends(get_db).
        """
        total = db.query(Article).count()
        items = (
            db.query(Article)
            .order_by(Article.created_at.desc())
            .offset((page - 1)*page_size)
            .limit(page_size)
            .all()
        )
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }


@router.post("/", status_code=201)
def create_article(
    data: ArticleCreate,
    db: Session = Depends(get_db),
):
    """创建新文章"""
    article = Article(**data.model_dump())  # Schema 转 ORM 对象
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.get("/{article_id}")
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    """获取某篇文章详情"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    redis.incr_view(article_id)
    article.views += 1
    db.commit()

    comment_count = db.query(Comment).filter(Comment.article_id == article_id).count()

    result = ArticleResponse.model_validate(article)  # ORM → Schema
    result.comment_count = comment_count
    return result

@router.put("/{article_id}")
def update_article(
    article_id: int,
    data: ArticleUpdate,
    db: Session = Depends(get_db)
):
    """
    更新文章（只更新用户传了的字段）
    - 通过 article_id 找到对应文章
    - model_dump(exclude_unset=True) 只取用户实际传了的字段，没传的不覆盖
    Args:
        article_id: 文章ID，来自 URL 路径
        data: 请求体，包含要更新的字段，全部可选
        db: 数据库会话
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    for key, value in data.model_dump(exclude_unset=True).items():
         setattr(article, key, value) #给article动态赋值

    db.commit()
    db.refresh(article)
    return article

@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    """
    删除文章
    - 通过 article_id 找到对应文章，不存在则 404
    - status_code=204 表示删除成功，无响应体
    Args:
        article_id: 文章ID，来自 URL 路径
        db: 数据库会话
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="文章不存在")

    db.delete(article)
    db.commit()
    

