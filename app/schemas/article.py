from pydantic import BaseModel
#所有 Schema 类都要继承它，就像 Model 继承 Base 一样,不继承 BaseModel，Pydantic 不认识你的类，不会自动校验
from datetime import datetime
from typing import Optional

#create Article
class ArticleCreate(BaseModel):
    title:str
    content:str
    summary:str|None = None

#update Article
class ArticleUpdate(BaseModel):
    title:str|None = None
    content:str|None = None
    summary:str|None = None

#Response
class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: str | None
    views: int
    created_at: datetime
    updated_at: datetime
    comment_count: int = 0 
    class Config:
        from_attributes = True