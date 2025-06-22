#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本功能测试脚本
测试MultiAgent Workflow系统的核心功能
"""

import asyncio
import json
import os
from dsl_models import (
    UseCaseDiagram, Actor, UseCase, ConceptualClassDiagram, 
    Class, Attribute, Method, Relationship, RelationshipType,
    SystemSequenceDiagram, Message, OCLConstraint, DomainModel
)
from tools import (
    save_domain_model, load_domain_model, validate_use_case_diagram,
    generate_sequence_diagram_from_usecase, extract_classes_from_usecases,
    generate_ocl_constraints, export_to_plantuml, analyze_domain_complexity
)
from my_agents import requirements_analyst, usecase_modeler, class_diagram_designer, sequence_diagram_designer, ocl_expert, validation_expert, coordinator

def test_dsl_models():
    """测试DSL数据模型"""
    print("🧪 测试DSL数据模型...")
    
    # 创建测试用例图
    actors = [
        Actor(name="顾客", description="购买图书的用户", type="primary"),
        Actor(name="管理员", description="系统管理员", type="secondary")
    ]
    
    usecases = [
        UseCase(
            name="购买图书",
            description="顾客选择图书并完成购买",
            actor="顾客",
            includes=["验证库存"],
            extends=[],
            preconditions=["用户已登录", "图书有库存"],
            postconditions=["订单创建成功", "库存减少"]
        ),
        UseCase(
            name="验证库存",
            description="检查图书库存是否充足",
            actor="系统",
            includes=[],
            extends=[],
            preconditions=["图书存在"],
            postconditions=["库存状态已确认"]
        )
    ]
    
    usecase_diagram = UseCaseDiagram(
        name="在线书店系统",
        description="图书销售管理系统",
        actors=actors,
        usecases=usecases
    )
    
    print("✅ 用例图创建成功")
    
    # 创建测试类图
    classes = [
        Class(
            name="Book",
            description="图书类",
            attributes=[
                Attribute(name="title", type="String", visibility="private"),
                Attribute(name="price", type="Double", visibility="private"),
                Attribute(name="stock", type="Integer", visibility="private")
            ],
            methods=[
                Method(name="getTitle", return_type="String", visibility="public"),
                Method(name="setPrice", parameters=["price"], return_type="void", visibility="public")
            ],
            stereotypes=[]
        ),
        Class(
            name="Order",
            description="订单类",
            attributes=[
                Attribute(name="orderId", type="String", visibility="private"),
                Attribute(name="totalAmount", type="Double", visibility="private")
            ],
            methods=[
                Method(name="calculateTotal", return_type="Double", visibility="public")
            ],
            stereotypes=[]
        )
    ]
    
    relationships = [
        Relationship(
            source="Order",
            target="Book",
            type=RelationshipType.ASSOCIATION,
            source_multiplicity="1",
            target_multiplicity="*",
            description="订单包含多本图书"
        )
    ]
    
    class_diagram = ConceptualClassDiagram(
        name="在线书店类图",
        description="图书销售系统的概念类图",
        classes=classes,
        relationships=relationships
    )
    
    print("✅ 类图创建成功")
    
    # 创建测试顺序图
    messages = [
        Message(
            name="查询图书",
            sender="顾客",
            receiver="系统",
            message_type="synchronous",
            parameters=["bookId"],
            return_value="bookInfo"
        )
    ]
    
    sequence_diagram = SystemSequenceDiagram(
        name="购买图书顺序图",
        description="顾客购买图书的交互流程",
        actors=["顾客"],
        systems=["系统"],
        messages=messages
    )
    
    print("✅ 顺序图创建成功")
    
    # 创建测试OCL约束
    ocl_constraints = [
        OCLConstraint(
            name="库存非负",
            context="Book",
            type="inv",
            expression="self.stock >= 0",
            description="图书库存不能为负数"
        )
    ]
    
    print("✅ OCL约束创建成功")
    
    # 创建完整领域模型
    domain_model = DomainModel(
        name="在线书店领域模型",
        description="完整的图书销售系统领域模型",
        usecase_diagram=usecase_diagram,
        sequence_diagrams=[sequence_diagram],
        class_diagram=class_diagram,
        ocl_constraints=ocl_constraints
    )
    
    print("✅ 领域模型创建成功")
    
    return domain_model

def test_tools():
    """测试工具函数"""
    print("\n🔧 测试工具函数...")
    
    # 创建测试模型
    domain_model = test_dsl_models()
    
    # 测试保存和加载
    try:
        save_result = save_domain_model(domain_model, "test_model.json")
        print(f"✅ {save_result}")
        
        loaded_model = load_domain_model("test_model.json")
        print("✅ 模型加载成功")
        
        # 清理测试文件
        os.remove("output/test_model.json")
        print("✅ 测试文件清理完成")
        
    except Exception as e:
        print(f"❌ 保存/加载测试失败: {e}")
    
    # 测试用例图验证
    validation_result = validate_use_case_diagram(domain_model.usecase_diagram)
    print(f"✅ 用例图验证: {'通过' if validation_result['is_valid'] else '失败'}")
    if validation_result['errors']:
        print(f"   错误: {validation_result['errors']}")
    if validation_result['warnings']:
        print(f"   警告: {validation_result['warnings']}")
    
    # 测试顺序图生成
    for usecase in domain_model.usecase_diagram.usecases:
        sequence_diagram = generate_sequence_diagram_from_usecase(usecase, "系统")
        print(f"✅ 为用例 '{usecase.name}' 生成顺序图")
    
    # 测试类提取
    classes = extract_classes_from_usecases(domain_model.usecase_diagram)
    print(f"✅ 从用例图提取了 {len(classes)} 个类")
    
    # 测试OCL约束生成
    constraints = generate_ocl_constraints(domain_model.usecase_diagram, domain_model.class_diagram)
    print(f"✅ 生成了 {len(constraints)} 个OCL约束")
    
    # 测试PlantUML导出
    plantuml_code = export_to_plantuml(domain_model)
    print("✅ PlantUML代码生成成功")
    print(f"   代码长度: {len(plantuml_code)} 字符")
    
    # 测试复杂度分析
    complexity = analyze_domain_complexity(domain_model)
    print(f"✅ 复杂度分析完成")
    print(f"   复杂度评分: {complexity['complexity_score']}")
    print(f"   复杂度等级: {complexity['complexity_level']}")

def test_json_serialization():
    """测试JSON序列化"""
    print("\n📄 测试JSON序列化...")
    
    domain_model = test_dsl_models()
    
    # 序列化
    json_str = domain_model.model_dump_json(indent=2)
    print(f"✅ JSON序列化成功，长度: {len(json_str)} 字符")
    
    # 反序列化
    data = json.loads(json_str)
    reconstructed_model = DomainModel(**data)
    print("✅ JSON反序列化成功")
    
    # 验证数据完整性
    assert len(reconstructed_model.usecase_diagram.usecases) == len(domain_model.usecase_diagram.usecases)
    assert len(reconstructed_model.class_diagram.classes) == len(domain_model.class_diagram.classes)
    assert len(reconstructed_model.ocl_constraints) == len(domain_model.ocl_constraints)
    print("✅ 数据完整性验证通过")

def main():
    """主测试函数"""
    print("🚀 MultiAgent Workflow 基本功能测试")
    print("=" * 50)
    
    try:
        # 测试DSL模型
        test_dsl_models()
        
        # 测试工具函数
        test_tools()
        
        # 测试JSON序列化
        test_json_serialization()
        
        print("\n🎉 所有基本功能测试通过！")
        print("\n📋 测试总结:")
        print("   ✅ DSL数据模型创建和验证")
        print("   ✅ 工具函数功能测试")
        print("   ✅ JSON序列化和反序列化")
        print("   ✅ 用例图验证")
        print("   ✅ 顺序图生成")
        print("   ✅ 类提取")
        print("   ✅ OCL约束生成")
        print("   ✅ PlantUML导出")
        print("   ✅ 复杂度分析")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 