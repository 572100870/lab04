#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MultiAgent Workflow 启动脚本
提供简单的命令行界面来运行领域建模工作流
"""

import asyncio
import sys
from workflow import MultiAgentWorkflow

def print_banner():
    """打印系统横幅"""
    print("=" * 60)
    print("🚀 MultiAgent Workflow 自动化领域建模系统")
    print("=" * 60)
    print("基于OpenAI Agents SDK的多智能体协同建模系统")
    print("支持用例图、类图、顺序图和OCL约束的自动生成")
    print("=" * 60)

def get_user_requirements():
    """获取用户需求"""
    print("\n📝 请输入您的系统需求描述：")
    print("（输入 'END' 结束输入）")
    print("-" * 40)
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    
    return '\n'.join(lines)

async def run_single_workflow():
    """运行单个工作流"""
    print_banner()
    
    # 获取用户需求
    requirements = get_user_requirements()
    
    if not requirements.strip():
        print("❌ 需求描述不能为空！")
        return
    
    print(f"\n📋 需求描述：")
    print("-" * 40)
    print(requirements)
    print("-" * 40)
    
    # 确认是否继续
    confirm = input("\n🤔 确认开始建模？(y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("❌ 已取消建模")
        return
    
    try:
        # 创建工作流实例
        print("\n🔄 初始化工作流...")
        workflow = MultiAgentWorkflow()
        
        # 运行工作流
        print("🚀 开始自动化领域建模...")
        final_model = await workflow.run_workflow(requirements)
        
        # 保存结果
        from tools import save_domain_model, export_to_plantuml, analyze_domain_complexity
        
        save_result = save_domain_model(final_model, "user_requirements_model.json")
        print(f"\n💾 {save_result}")
        
        # 分析复杂度
        complexity = analyze_domain_complexity(final_model)
        print(f"\n📊 模型复杂度分析:")
        print(f"   - 复杂度评分: {complexity['complexity_score']}")
        print(f"   - 复杂度等级: {complexity['complexity_level']}")
        print(f"   - 用例数量: {complexity['metrics']['usecase_count']}")
        print(f"   - 参与者数量: {complexity['metrics']['actor_count']}")
        print(f"   - 类数量: {complexity['metrics']['class_count']}")
        print(f"   - 关系数量: {complexity['metrics']['relationship_count']}")
        print(f"   - OCL约束数量: {complexity['metrics']['constraint_count']}")
        
        # 导出PlantUML
        plantuml_code = export_to_plantuml(final_model)
        with open("output/user_requirements_usecase.puml", "w", encoding="utf-8") as f:
            f.write(plantuml_code)
        print("📊 PlantUML用例图已导出到 output/user_requirements_usecase.puml")
        
        print("\n🎉 建模完成！")
        print("\n📁 生成的文件:")
        print("   - output/user_requirements_model.json (完整领域模型)")
        print("   - output/user_requirements_usecase.puml (PlantUML用例图)")
        
    except Exception as e:
        print(f"\n❌ 建模过程中出现错误: {e}")
        print("请检查网络连接和API配置")

def show_help():
    """显示帮助信息"""
    print_banner()
    print("\n📖 使用说明:")
    print("1. 运行单个建模任务: python run.py")
    print("2. 运行示例: python example_usage.py")
    print("3. 运行测试: python test_basic.py")
    print("\n🔧 配置说明:")
    print("- 编辑 config.py 文件设置API配置")
    print("- 确保网络连接正常")
    print("- 检查代理设置（如需要）")
    print("\n📋 支持的功能:")
    print("- 用例图自动生成")
    print("- 概念类图设计")
    print("- 系统顺序图创建")
    print("- OCL约束生成")
    print("- 模型验证和改进")
    print("- PlantUML格式导出")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ['help', '-h', '--help']:
            show_help()
        elif command in ['test', '--test']:
            print("🧪 运行基本功能测试...")
            from test_basic import main as test_main
            test_main()
        elif command in ['example', '--example']:
            print("📚 运行示例...")
            asyncio.run(example_usage.main())
        else:
            print(f"❌ 未知命令: {command}")
            print("使用 'python run.py help' 查看帮助")
    else:
        # 运行交互式建模
        asyncio.run(run_single_workflow())

if __name__ == "__main__":
    main() 