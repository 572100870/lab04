"""
OpenAI API 配置文件
"""
import os
from typing import Dict, Any

# OpenAI API 配置 - 使用VPN代理
BASE_URL: str = "http://127.0.0.1:7890/v1"  # VPN代理接口
API_KEY: str = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"

# 模型配置
DEFAULT_MODEL: str = "gpt-4o"
TEMPERATURE: float = 0.7
MAX_TOKENS: int = 4000

# 需求建模相关配置
REQUIREMENT_TEMPLATES = {
    "functional": "功能需求",
    "non_functional": "非功能需求", 
    "user_story": "用户故事",
    "use_case": "用例",
    "business_rule": "业务规则"
}

# 输出格式配置
OUTPUT_FORMATS = {
    "json": "JSON格式",
    "yaml": "YAML格式", 
    "markdown": "Markdown格式",
    "xml": "XML格式"
}

# 多智能体工作流配置
AGENT_CONFIGS = {
    "requirement_analyzer": {
        "name": "需求分析智能体",
        "description": "负责分析用户需求并提取关键信息",
        "model": DEFAULT_MODEL,
        "temperature": 0.3
    },
    "model_generator": {
        "name": "模型生成智能体", 
        "description": "负责生成结构化的需求模型",
        "model": DEFAULT_MODEL,
        "temperature": 0.5
    },
    "validator": {
        "name": "验证智能体",
        "description": "负责验证生成的需求模型的完整性和一致性",
        "model": DEFAULT_MODEL,
        "temperature": 0.2
    }
} 