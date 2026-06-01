from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    author:str
    content:str

class CommentResponse(BaseModel):
    id:int
    article_id:int
    author: str
    content: str
    likes: int
    created_at: datetime

    class Config:
        from_attributes = True
    #这里涉及ORM对象转型Schemas，所以要加上这句代码