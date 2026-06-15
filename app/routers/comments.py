from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article, Comment
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix = "/api/comments" , tags = ["comments"])
# ==================== 某篇文章的评论列表 ====================
@router.get("/")
def list_comments(
    article_id: int = Query(..., description = "文章ID"), #...代表无默认值
    db: Session = Depends(get_db)
):
    """
    获取指定文章的所有评论，按时间正序（最早的在前面）
    Args:
        article_id (id, optional): 文章ID. Defaults to Query(..., description = "文章ID").
    """

    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    comments = (
        db.query(Comment)
        .filter(Comment.article_id == article_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return comments
# ==================== 创建评论 ====================
@router.post("/",status_code = 201)
def create_comment(
    data: CommentCreate,
    article_id: int = Query(..., description="文章 ID"),
    db:Session = Depends(get_db)
):
    """
    为指定文章添加一条评论
    Args:
        article_id (int, optional): . Defaults to Query(..., description="文章 ID").
        data (CommentCreate, optional): . Defaults to None.
        db (Session, optional): . Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    comment = Comment(
        article_id = article_id,
        author = data.author,
        content = data.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# ==================== 点赞 ====================
@router.put("/{comment_id}/like")
def like_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """
    给某条评论点赞
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    comment.likes += 1
    db.commit()
    db.refresh(comment)
    return {"likes" :comment.likes}