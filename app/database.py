#数据库链接
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config import settings #引入配置文件

engine = create_engine(
    settings.DATABASE_URL,
    connect_args = {"check_same_thread" :False}
)
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)
Base = declarative_base() # Base 就是一个普通的 Python 类，但它内部绑定了 SQLAlchemy 的元数据注册表（MetaData），用来记录所有表结构
def get_db():
    db = SessionLocal()
    try:
        yield db #yield是return是升级版，yield等db函数结束后还会继续执行代码
    finally:
        db.close()
        