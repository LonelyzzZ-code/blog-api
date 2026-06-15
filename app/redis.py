#连接 Redis 缓存服务器，提供读缓存、写缓存、计数器等功能。如果没配 Redis，所有方法自动降级返回默认值，不报错
import redis
from .config import settings
#尝试链接Redis，失败就置为None
try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL) if settings.REDIS_URL else None
except Exception as e:
    redis_client = None

def get_redis():
    """
    返回Redis链接
    可能为None
    """
    return redis_client

def cache_get(key :str) -> str|None:
    """
    从缓存读取数据，Redis没链接就返回None
    """
    if redis_client is None:
        return None
    try:
        return redis_client.get(key)
    except Exception:
        return None

def cache_set(key :str,value :str,expire :int = 3600) ->bool:
    """
    往缓存写数据
    Args:
        key (str): 缓存的键名
        value (str): 缓存的值
        expire (int, optional): 过期的时间. Defaults to 3600.

    Returns:
        bool: 返回布尔值
    """
    if redis_client is None:
        return False
    try:
        redis_client.set(key,value,ex = expire)
        return True
    except Exception:
        return False

def incr_view(article_id:int)->int:
    """
    文章访问量+1，返回当前的访问量
    如果没链接Redis，则返回0
    """
    if redis_client is None:
        return 0
    try:
        return redis_client.incr(f"article:view:{article_id}")#.incr(key)传入key时key会自动加一，并入写入数据
    except Exception:
        return 0
    
def get_views(article_id: int) -> int | None:
    """
    获取某篇文章的访问量
    返回None表示Redis没数据
    """
    if redis_client is None:
        return None
    try:
        val = redis_client.get(f"article:view:{article_id}")
        return int(val) if val else None
    except Exception:
        return None