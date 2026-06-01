from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"
    # ===================== 字段定义 =====================
    id = Column(Integer,primary_key = True,autoincrement = True)
    article_id = Column(Integer,ForeignKey("articles.id"),index = True,nullable = False)
    #ForeignKey在指定article_id的来源为articles
    author = Column(String(100),nullable = False)
    content = Column(Text,nullable = False)
    likes =  Column(Integer,default = 0)
    created_at = Column(DateTime,server_default = func.now())
    article = relationship("Article",back_populates = "comments")