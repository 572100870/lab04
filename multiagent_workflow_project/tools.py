from typing import List, Dict, Any, Optional
from dsl_models import (
    DomainModel, UseCaseDiagram, SystemSequenceDiagram, 
    ConceptualClassDiagram, OCLConstraint, UseCase, Actor,
    Class, Relationship, Message
)
import json
import os
from datetime import datetime

def save_domain_model(model: DomainModel, filename: str = None) -> str:
    """
    保存领域模型到JSON文件
    
    Args:
        model: 领域模型对象
        filename: 文件名，如果不提供则自动生成
    
    Returns:
        保存的文件路径
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"domain_model_{timestamp}.json"
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    
    # 转换为JSON并保存
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(model.model_dump(), f, ensure_ascii=False, indent=2)
    
    return f"领域模型已保存到: {filepath}"

def load_domain_model(filename: str) -> DomainModel:
    """
    从JSON文件加载领域模型
    
    Args:
        filename: 文件名
    
    Returns:
        领域模型对象
    """
    filepath = os.path.join("output", filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return DomainModel(**data)

def validate_use_case_diagram(usecase_diagram: UseCaseDiagram) -> Dict[str, Any]:
    """
    验证用例图的完整性和一致性
    
    Args:
        usecase_diagram: 用例图对象
    
    Returns:
        验证结果
    """
    errors = []
    warnings = []
    
    # 检查用例名称唯一性
    usecase_names = [uc.name for uc in usecase_diagram.usecases]
    if len(usecase_names) != len(set(usecase_names)):
        errors.append("存在重复的用例名称")
    
    # 检查参与者名称唯一性
    actor_names = [actor.name for actor in usecase_diagram.actors]
    if len(actor_names) != len(set(actor_names)):
        errors.append("存在重复的参与者名称")
    
    # 检查用例中的参与者是否存在
    for usecase in usecase_diagram.usecases:
        if usecase.actor not in actor_names:
            errors.append(f"用例 '{usecase.name}' 的参与者 '{usecase.actor}' 不存在")
    
    # 检查包含和扩展的用例是否存在
    for usecase in usecase_diagram.usecases:
        for included in usecase.includes:
            if included not in usecase_names:
                errors.append(f"用例 '{usecase.name}' 包含的用例 '{included}' 不存在")
        
        for extended in usecase.extends:
            if extended not in usecase_names:
                errors.append(f"用例 '{usecase.name}' 扩展的用例 '{extended}' 不存在")
    
    # 检查是否有孤立用例（没有参与者）
    for usecase in usecase_diagram.usecases:
        if not usecase.actor:
            warnings.append(f"用例 '{usecase.name}' 没有指定参与者")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "usecase_count": len(usecase_diagram.usecases),
        "actor_count": len(usecase_diagram.actors)
    }

def generate_sequence_diagram_from_usecase(usecase: UseCase, system_name: str) -> SystemSequenceDiagram:
    """
    根据用例自动生成系统顺序图
    
    Args:
        usecase: 用例对象
        system_name: 系统名称
    
    Returns:
        系统顺序图对象
    """
    # 创建基本的顺序图
    sequence_diagram = SystemSequenceDiagram(
        name=f"{usecase.name}_Sequence",
        description=f"用例 '{usecase.name}' 的系统顺序图",
        actors=[usecase.actor],
        systems=[system_name],
        messages=[]
    )
    
    # 添加基本的交互消息
    sequence_diagram.messages.append(Message(
        name=f"执行{usecase.name}",
        sender=usecase.actor,
        receiver=system_name,
        message_type="synchronous",
        parameters=[],
        return_value="结果"
    ))
    
    return sequence_diagram

def extract_classes_from_usecases(usecase_diagram: UseCaseDiagram) -> List[Class]:
    """
    从用例图中提取潜在的概念类
    
    Args:
        usecase_diagram: 用例图对象
    
    Returns:
        概念类列表
    """
    classes = []
    
    # 为每个参与者创建类
    for actor in usecase_diagram.actors:
        classes.append(Class(
            name=actor.name,
            description=f"参与者: {actor.description or actor.name}",
            attributes=[],
            methods=[],
            stereotypes=["actor"]
        ))
    
    # 为每个用例创建类
    for usecase in usecase_diagram.usecases:
        classes.append(Class(
            name=usecase.name,
            description=f"用例: {usecase.description or usecase.name}",
            attributes=[],
            methods=[],
            stereotypes=["usecase"]
        ))
    
    return classes

def generate_ocl_constraints(usecase_diagram: UseCaseDiagram, class_diagram: ConceptualClassDiagram) -> List[OCLConstraint]:
    """
    根据用例图和类图生成OCL约束
    
    Args:
        usecase_diagram: 用例图对象
        class_diagram: 类图对象
    
    Returns:
        OCL约束列表
    """
    constraints = []
    
    # 为每个用例生成前置条件约束
    for usecase in usecase_diagram.usecases:
        if usecase.preconditions:
            for i, precondition in enumerate(usecase.preconditions):
                constraints.append(OCLConstraint(
                    name=f"{usecase.name}_Precondition_{i+1}",
                    context=usecase.name,
                    type="pre",
                    expression=precondition,
                    description=f"用例 '{usecase.name}' 的前置条件"
                ))
        
        if usecase.postconditions:
            for i, postcondition in enumerate(usecase.postconditions):
                constraints.append(OCLConstraint(
                    name=f"{usecase.name}_Postcondition_{i+1}",
                    context=usecase.name,
                    type="post",
                    expression=postcondition,
                    description=f"用例 '{usecase.name}' 的后置条件"
                ))
    
    # 为类生成不变量约束
    for cls in class_diagram.classes:
        # 检查属性多重性约束
        for attr in cls.attributes:
            if attr.multiplicity != "1":
                constraints.append(OCLConstraint(
                    name=f"{cls.name}_{attr.name}_Multiplicity",
                    context=cls.name,
                    type="inv",
                    expression=f"self.{attr.name}.size() >= 0",
                    description=f"类 '{cls.name}' 属性 '{attr.name}' 的多重性约束"
                ))
    
    return constraints

def export_to_plantuml(domain_model: DomainModel) -> str:
    """
    将领域模型导出为PlantUML格式
    
    Args:
        domain_model: 领域模型对象
    
    Returns:
        PlantUML代码
    """
    plantuml_code = []
    
    # 用例图
    plantuml_code.append("@startuml")
    plantuml_code.append("title " + domain_model.usecase_diagram.name)
    
    # 添加参与者
    for actor in domain_model.usecase_diagram.actors:
        plantuml_code.append(f"actor \"{actor.name}\" as {actor.name.replace(' ', '_')}")
    
    # 添加用例
    for usecase in domain_model.usecase_diagram.usecases:
        plantuml_code.append(f"usecase \"{usecase.name}\" as {usecase.name.replace(' ', '_')}")
    
    # 添加关系
    for usecase in domain_model.usecase_diagram.usecases:
        plantuml_code.append(f"{usecase.actor.replace(' ', '_')} --> {usecase.name.replace(' ', '_')}")
        
        for included in usecase.includes:
            plantuml_code.append(f"{usecase.name.replace(' ', '_')} ..> {included.replace(' ', '_')} : <<include>>")
        
        for extended in usecase.extends:
            plantuml_code.append(f"{usecase.name.replace(' ', '_')} ..> {extended.replace(' ', '_')} : <<extend>>")
    
    plantuml_code.append("@enduml")
    
    return "\n".join(plantuml_code)

def analyze_domain_complexity(domain_model: DomainModel) -> Dict[str, Any]:
    """
    分析领域模型的复杂度
    
    Args:
        domain_model: 领域模型对象
    
    Returns:
        复杂度分析结果
    """
    usecase_count = len(domain_model.usecase_diagram.usecases)
    actor_count = len(domain_model.usecase_diagram.actors)
    class_count = len(domain_model.class_diagram.classes)
    relationship_count = len(domain_model.class_diagram.relationships)
    constraint_count = len(domain_model.ocl_constraints)
    
    # 计算复杂度指标
    complexity_score = (usecase_count * 0.3 + 
                       actor_count * 0.2 + 
                       class_count * 0.3 + 
                       relationship_count * 0.1 + 
                       constraint_count * 0.1)
    
    complexity_level = "简单"
    if complexity_score > 10:
        complexity_level = "复杂"
    elif complexity_score > 5:
        complexity_level = "中等"
    
    return {
        "complexity_score": round(complexity_score, 2),
        "complexity_level": complexity_level,
        "metrics": {
            "usecase_count": usecase_count,
            "actor_count": actor_count,
            "class_count": class_count,
            "relationship_count": relationship_count,
            "constraint_count": constraint_count
        },
        "recommendations": [
            "建议将复杂用例拆分为更小的用例",
            "考虑使用泛化关系简化类图",
            "确保OCL约束的可读性和可维护性"
        ] if complexity_score > 10 else [
            "模型结构清晰，复杂度适中",
            "可以适当增加细节描述"
        ]
    } 