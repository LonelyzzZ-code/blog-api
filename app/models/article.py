#文章表
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship #关系映射，用来定义表与表之间的关系
from app.database import Base

class Article(Base):
    __tablename__ = "articles"# 数据库里表的名字
    # ===================== 字段定义 =====================
    id = Column(Integer, primary_key=True, autoincrement=True)
    #文章标题
    title = Column(String(200),index = True,nullable = False)
    #文章正文
    content = Column(Text,nullable = False)
    #文章摘要
    summary = Column(String(1000),nullable = True)
    #访问量
    views = Column(Integer,default = 0,server_default = "0")
    #创建时间
    created_at = Column(DateTime,server_default = func.now())
    #更新时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())#onupdate自动更新,当这行数据被修改时，自动修改为等号后的数值

    # ===================== 关联关系 =====================

    comments = relationship("Comment",back_populates = "article",cascade="all, delete-orphan")
    


