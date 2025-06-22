#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MultiAgent Workflow 示例使用脚本
演示如何使用自动化领域建模系统
"""

import json
import os
from workflow import MultiAgentWorkflow
from tools import save_domain_model, export_to_plantuml, analyze_domain_complexity

def example_online_bookstore():
    """在线书店系统建模示例"""
    print("📚 在线书店系统领域建模示例")
    print("=" * 50)
    
    requirements = """
    请为在线书店系统进行领域建模。
    
    系统功能包括：
    1. 用户注册和登录
    2. 浏览和搜索图书
    3. 添加图书到购物车
    4. 下单和支付
    5. 订单管理
    6. 库存管理
    7. 用户评价和评论
    
    主要参与者包括：顾客、管理员、支付系统
    
    业务规则：
    - 用户必须注册才能购买图书
    - 图书库存不足时不能下单
    - 订单支付成功后库存自动减少
    - 用户可以对已购买的图书进行评价
    """
    
    # 创建工作流实例
    workflow = MultiAgentWorkflow()
    
    # 运行工作流
    final_model = workflow.run_workflow(requirements)
    
    # 确保output目录存在
    os.makedirs("output", exist_ok=True)
    
    # 保存结果
    save_result = save_domain_model(final_model, "online_bookstore_model.json")
    print(f"\n💾 {save_result}")
    
    # 分析复杂度
    complexity = analyze_domain_complexity(final_model)
    print(f"\n📊 模型复杂度分析:")
    print(f"   - 复杂度评分: {complexity['complexity_score']}")
    print(f"   - 复杂度等级: {complexity['complexity_level']}")
    print(f"   - 用例数量: {complexity['metrics']['usecase_count']}")
    print(f"   - 参与者数量: {complexity['metrics']['actor_count']}")
    print(f"   - 类数量: {complexity['metrics']['class_count']}")
    
    # 导出PlantUML
    plantuml_code = export_to_plantuml(final_model)
    with open("output/online_bookstore_usecase.puml", "w", encoding="utf-8") as f:
        f.write(plantuml_code)
    print("📊 PlantUML用例图已导出到 output/online_bookstore_usecase.puml")
    
    return final_model

def main():
    """主函数 - 运行在线书店示例"""
    print("🚀 MultiAgent Workflow 自动化领域建模系统")
    print("=" * 60)
    
    try:
        # 运行在线书店示例
        bookstore_model = example_online_bookstore()
        
        print("\n🎉 示例运行完成！")
        print("\n📁 生成的文件:")
        print("   - output/online_bookstore_model.json")
        print("   - output/online_bookstore_usecase.puml")
        
        # 显示模型统计信息
        print("\n📊 模型统计信息:")
        print(f"   - 用例图: {len(bookstore_model.usecase_diagram.usecases)} 个用例")
        print(f"   - 类图: {len(bookstore_model.class_diagram.classes)} 个类")
        print(f"   - 顺序图: {len(bookstore_model.sequence_diagrams)} 个顺序图")
        print(f"   - OCL约束: {len(bookstore_model.ocl_constraints)} 个约束")
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 