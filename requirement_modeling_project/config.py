"""
配置文件 - 包含API配置和常量
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
BASE_URL = "https://api.chatfire.cn/v1"
API_KEY = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"

# 代理配置 - 支持VPN
PROXY_CONFIG = {
    "http": "http://127.0.0.1:7890",  # 用户确认的代理端口
    "https": "http://127.0.0.1:7890"
}

# 备用代理配置（如果7890端口不行，可以尝试其他端口）
PROXY_CONFIG_ALTERNATIVE = {
    "http": "http://127.0.0.1:1080",  # 另一个常见端口
    "https": "http://127.0.0.1:1080"
}

# 模型配置
DEFAULT_MODEL = "gpt-4o"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# 需求建模相关配置
REQUIREMENT_MODELING_PROMPT = """
你是一个专业的需求分析师和软件架构师。请根据用户提供的需求描述，生成结构化的需求模型。

请按照以下JSON格式输出需求模型：

{
  "project_name": "项目名称",
  "description": "项目总体描述",
  "stakeholders": [
    {
      "name": "利益相关者名称",
      "role": "角色描述",
      "responsibilities": ["职责1", "职责2"]
    }
  ],
  "functional_requirements": [
    {
      "id": "FR001",
      "title": "功能需求标题",
      "description": "详细描述",
      "priority": "高/中/低",
      "acceptance_criteria": ["验收标准1", "验收标准2"]
    }
  ],
  "non_functional_requirements": [
    {
      "id": "NFR001",
      "category": "性能/安全性/可用性/可维护性",
      "title": "非功能需求标题",
      "description": "详细描述",
      "metrics": "可量化的指标"
    }
  ],
  "use_cases": [
    {
      "id": "UC001",
      "title": "用例标题",
      "actor": "参与者",
      "preconditions": ["前置条件1", "前置条件2"],
      "main_flow": ["步骤1", "步骤2", "步骤3"],
      "postconditions": ["后置条件1", "后置条件2"]
    }
  ],
  "data_models": [
    {
      "name": "数据模型名称",
      "description": "描述",
      "attributes": [
        {
          "name": "属性名",
          "type": "数据类型",
          "description": "属性描述",
          "constraints": "约束条件"
        }
      ]
    }
  ],
  "system_architecture": {
    "overview": "系统架构概述",
    "components": [
      {
        "name": "组件名称",
        "description": "组件描述",
        "responsibilities": ["职责1", "职责2"]
      }
    ],
    "interfaces": [
      {
        "name": "接口名称",
        "description": "接口描述",
        "input": "输入参数",
        "output": "输出参数"
      }
    ]
  }
}

请确保输出的JSON格式正确，内容详实且符合软件工程最佳实践。
""" 