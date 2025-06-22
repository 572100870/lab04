import os
from typing import Literal
from pydantic import BaseModel

class Config(BaseModel):
    """项目配置类"""
    base_url: str = "https://api.chatfire.cn/v1"
    api_key: str = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"
    proxy_host: str = "127.0.0.1"
    proxy_port: int = 7890
    model: str = "gpt-4o"
    
    class Config:
        env_file = ".env"

# 全局配置实例
config = Config()

# 代理设置 - 修正为httpx支持的格式
PROXIES = f"http://{config.proxy_host}:{config.proxy_port}" 