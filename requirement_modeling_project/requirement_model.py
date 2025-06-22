"""
需求模型数据结构定义
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum


class Priority(str, Enum):
    """优先级枚举"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class Category(str, Enum):
    """非功能需求类别枚举"""
    PERFORMANCE = "性能"
    SECURITY = "安全性"
    USABILITY = "可用性"
    MAINTAINABILITY = "可维护性"
    SCALABILITY = "可扩展性"
    RELIABILITY = "可靠性"


class Stakeholder(BaseModel):
    """利益相关者模型"""
    name: str = Field(..., description="利益相关者名称")
    role: str = Field(..., description="角色描述")
    responsibilities: List[str] = Field(default_factory=list, description="职责列表")


class FunctionalRequirement(BaseModel):
    """功能需求模型"""
    id: str = Field(..., description="需求ID")
    title: str = Field(..., description="需求标题")
    description: str = Field(..., description="详细描述")
    priority: Priority = Field(..., description="优先级")
    acceptance_criteria: List[str] = Field(default_factory=list, description="验收标准")
    
    @validator('id')
    def validate_id(cls, v):
        if not v.startswith('FR'):
            raise ValueError('功能需求ID必须以FR开头')
        return v


class NonFunctionalRequirement(BaseModel):
    """非功能需求模型"""
    id: str = Field(..., description="需求ID")
    category: Category = Field(..., description="需求类别")
    title: str = Field(..., description="需求标题")
    description: str = Field(..., description="详细描述")
    metrics: str = Field(..., description="可量化的指标")
    
    @validator('id')
    def validate_id(cls, v):
        if not v.startswith('NFR'):
            raise ValueError('非功能需求ID必须以NFR开头')
        return v


class UseCase(BaseModel):
    """用例模型"""
    id: str = Field(..., description="用例ID")
    title: str = Field(..., description="用例标题")
    actor: str = Field(..., description="参与者")
    preconditions: List[str] = Field(default_factory=list, description="前置条件")
    main_flow: List[str] = Field(..., description="主要流程")
    postconditions: List[str] = Field(default_factory=list, description="后置条件")
    
    @validator('id')
    def validate_id(cls, v):
        if not v.startswith('UC'):
            raise ValueError('用例ID必须以UC开头')
        return v


class DataAttribute(BaseModel):
    """数据属性模型"""
    name: str = Field(..., description="属性名")
    type: str = Field(..., description="数据类型")
    description: str = Field(..., description="属性描述")
    constraints: Optional[str] = Field(None, description="约束条件")


class DataModel(BaseModel):
    """数据模型"""
    name: str = Field(..., description="数据模型名称")
    description: str = Field(..., description="描述")
    attributes: List[DataAttribute] = Field(default_factory=list, description="属性列表")


class SystemComponent(BaseModel):
    """系统组件模型"""
    name: str = Field(..., description="组件名称")
    description: str = Field(..., description="组件描述")
    responsibilities: List[str] = Field(default_factory=list, description="职责列表")


class SystemInterface(BaseModel):
    """系统接口模型"""
    name: str = Field(..., description="接口名称")
    description: str = Field(..., description="接口描述")
    input: str = Field(..., description="输入参数")
    output: str = Field(..., description="输出参数")


class SystemArchitecture(BaseModel):
    """系统架构模型"""
    overview: str = Field(..., description="系统架构概述")
    components: List[SystemComponent] = Field(default_factory=list, description="组件列表")
    interfaces: List[SystemInterface] = Field(default_factory=list, description="接口列表")


class RequirementModel(BaseModel):
    """完整的需求模型"""
    project_name: str = Field(..., description="项目名称")
    description: str = Field(..., description="项目总体描述")
    stakeholders: List[Stakeholder] = Field(default_factory=list, description="利益相关者列表")
    functional_requirements: List[FunctionalRequirement] = Field(default_factory=list, description="功能需求列表")
    non_functional_requirements: List[NonFunctionalRequirement] = Field(default_factory=list, description="非功能需求列表")
    use_cases: List[UseCase] = Field(default_factory=list, description="用例列表")
    data_models: List[DataModel] = Field(default_factory=list, description="数据模型列表")
    system_architecture: SystemArchitecture = Field(..., description="系统架构")
    
    class Config:
        schema_extra = {
            "example": {
                "project_name": "在线图书管理系统",
                "description": "一个基于Web的图书管理系统，支持图书借阅、归还、查询等功能",
                "stakeholders": [
                    {
                        "name": "图书管理员",
                        "role": "系统管理员",
                        "responsibilities": ["图书管理", "用户管理", "借阅记录管理"]
                    }
                ],
                "functional_requirements": [
                    {
                        "id": "FR001",
                        "title": "图书查询功能",
                        "description": "用户可以通过多种方式查询图书信息",
                        "priority": "高",
                        "acceptance_criteria": ["支持按书名查询", "支持按作者查询", "支持按ISBN查询"]
                    }
                ],
                "non_functional_requirements": [
                    {
                        "id": "NFR001",
                        "category": "性能",
                        "title": "响应时间要求",
                        "description": "系统响应时间应在3秒内",
                        "metrics": "页面加载时间 < 3秒"
                    }
                ],
                "use_cases": [
                    {
                        "id": "UC001",
                        "title": "用户登录",
                        "actor": "用户",
                        "preconditions": ["用户已注册"],
                        "main_flow": ["输入用户名和密码", "系统验证身份", "登录成功"],
                        "postconditions": ["用户成功登录系统"]
                    }
                ],
                "data_models": [
                    {
                        "name": "用户模型",
                        "description": "用户基本信息",
                        "attributes": [
                            {
                                "name": "user_id",
                                "type": "Integer",
                                "description": "用户唯一标识",
                                "constraints": "主键，自增"
                            }
                        ]
                    }
                ],
                "system_architecture": {
                    "overview": "采用MVC架构模式",
                    "components": [
                        {
                            "name": "用户管理模块",
                            "description": "处理用户相关操作",
                            "responsibilities": ["用户注册", "用户登录", "用户信息管理"]
                        }
                    ],
                    "interfaces": [
                        {
                            "name": "用户认证接口",
                            "description": "用户登录认证",
                            "input": "用户名、密码",
                            "output": "认证结果、用户信息"
                        }
                    ]
                }
            }
        }


def validate_requirement_model(data: Dict[str, Any]) -> RequirementModel:
    """
    验证并创建需求模型实例
    
    Args:
        data: 原始数据字典
        
    Returns:
        验证后的需求模型实例
    """
    return RequirementModel(**data)


def requirement_model_to_dict(model: RequirementModel) -> Dict[str, Any]:
    """
    将需求模型转换为字典
    
    Args:
        model: 需求模型实例
        
    Returns:
        字典格式的需求模型
    """
    return model.dict()


def requirement_model_to_json(model: RequirementModel, indent: int = 2) -> str:
    """
    将需求模型转换为JSON字符串
    
    Args:
        model: 需求模型实例
        indent: JSON缩进
        
    Returns:
        JSON字符串
    """
    return model.json(indent=indent, ensure_ascii=False) 