from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class RelationshipType(str, Enum):
    """关系类型枚举"""
    INCLUDE = "include"
    EXTEND = "extend"
    ASSOCIATION = "association"
    GENERALIZATION = "generalization"
    COMPOSITION = "composition"
    AGGREGATION = "aggregation"

class Actor(BaseModel):
    """参与者模型"""
    name: str = Field(..., description="参与者名称")
    description: Optional[str] = Field(None, description="参与者描述")
    type: str = Field("primary", description="参与者类型：primary/secondary")

class UseCase(BaseModel):
    """用例模型"""
    name: str = Field(..., description="用例名称")
    description: Optional[str] = Field(None, description="用例描述")
    actor: str = Field(..., description="主要参与者")
    includes: List[str] = Field(default_factory=list, description="包含的用例")
    extends: List[str] = Field(default_factory=list, description="扩展的用例")
    preconditions: List[str] = Field(default_factory=list, description="前置条件")
    postconditions: List[str] = Field(default_factory=list, description="后置条件")

class UseCaseDiagram(BaseModel):
    """用例图模型"""
    name: str = Field(..., description="系统名称")
    description: Optional[str] = Field(None, description="系统描述")
    actors: List[Actor] = Field(default_factory=list, description="参与者列表")
    usecases: List[UseCase] = Field(default_factory=list, description="用例列表")

class Message(BaseModel):
    """消息模型"""
    name: str = Field(..., description="消息名称")
    sender: str = Field(..., description="发送方")
    receiver: str = Field(..., description="接收方")
    message_type: str = Field("synchronous", description="消息类型：synchronous/asynchronous")
    parameters: List[str] = Field(default_factory=list, description="参数列表")
    return_value: Optional[str] = Field(None, description="返回值")

class SystemSequenceDiagram(BaseModel):
    """系统顺序图模型"""
    name: str = Field(..., description="顺序图名称")
    description: Optional[str] = Field(None, description="顺序图描述")
    actors: List[str] = Field(default_factory=list, description="参与者列表")
    systems: List[str] = Field(default_factory=list, description="系统列表")
    messages: List[Message] = Field(default_factory=list, description="消息列表")

class Attribute(BaseModel):
    """属性模型"""
    name: str = Field(..., description="属性名称")
    type: str = Field(..., description="属性类型")
    visibility: str = Field("private", description="可见性：public/private/protected")
    multiplicity: str = Field("1", description="多重性")
    description: Optional[str] = Field(None, description="属性描述")

class Method(BaseModel):
    """方法模型"""
    name: str = Field(..., description="方法名称")
    parameters: List[str] = Field(default_factory=list, description="参数列表")
    return_type: Optional[str] = Field(None, description="返回类型")
    visibility: str = Field("public", description="可见性：public/private/protected")
    description: Optional[str] = Field(None, description="方法描述")

class Class(BaseModel):
    """类模型"""
    name: str = Field(..., description="类名称")
    description: Optional[str] = Field(None, description="类描述")
    attributes: List[Attribute] = Field(default_factory=list, description="属性列表")
    methods: List[Method] = Field(default_factory=list, description="方法列表")
    stereotypes: List[str] = Field(default_factory=list, description="构造型列表")

class Relationship(BaseModel):
    """关系模型"""
    name: Optional[str] = Field(None, description="关系名称")
    source: str = Field(..., description="源类")
    target: str = Field(..., description="目标类")
    type: RelationshipType = Field(..., description="关系类型")
    source_multiplicity: str = Field("1", description="源端多重性")
    target_multiplicity: str = Field("1", description="目标端多重性")
    description: Optional[str] = Field(None, description="关系描述")

class ConceptualClassDiagram(BaseModel):
    """概念类图模型"""
    name: str = Field(..., description="类图名称")
    description: Optional[str] = Field(None, description="类图描述")
    classes: List[Class] = Field(default_factory=list, description="类列表")
    relationships: List[Relationship] = Field(default_factory=list, description="关系列表")

class OCLConstraint(BaseModel):
    """OCL约束模型"""
    name: str = Field(..., description="约束名称")
    context: str = Field(..., description="约束上下文")
    type: str = Field(..., description="约束类型：inv/pre/post")
    expression: str = Field(..., description="OCL表达式")
    description: Optional[str] = Field(None, description="约束描述")

class DomainModel(BaseModel):
    """完整领域模型"""
    name: str = Field(..., description="项目名称")
    description: Optional[str] = Field(None, description="项目描述")
    usecase_diagram: UseCaseDiagram = Field(..., description="用例图")
    sequence_diagrams: List[SystemSequenceDiagram] = Field(default_factory=list, description="系统顺序图列表")
    class_diagram: ConceptualClassDiagram = Field(..., description="概念类图")
    ocl_constraints: List[OCLConstraint] = Field(default_factory=list, description="OCL约束列表")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据") 