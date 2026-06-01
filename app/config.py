#配置文件
from pydantic_settings import BaseSettings
#引入BaseSettings类
#BaseSettings 是 Pydantic 提供的一个特殊类，它能自动读取 .env 文件和系统环境变量，然后把值映射到类的属性上

class Settings(BaseSettings):
    DATABASE_URL: str #BaseSettings类会根据名字自动在env中索取地址，不需要填
    REDIS_URL:str | None = None #| None就是对REDIS_URL做空值判断，如果没有就直接跳过
    APP_TITLE:str = "0.1.0"
    SECRET_KEY:str = "change-me"

    class Config:
        env_file = ".env" #这不是普通的类，这是Pydantic的配置类

settings = Settings() #创建全局实例


