"""
主程序 - OpenAI需求建模演示
"""
import json
import logging
from typing import Dict, Any
from openai_client import OpenAIRequirementClient
from requirement_modeler import RequirementModeler
from multi_agent_workflow import MultiAgentWorkflow

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_openai_connection():
    """测试OpenAI API连接"""
    print("=" * 50)
    print("测试OpenAI API连接")
    print("=" * 50)
    
    try:
        client = OpenAIRequirementClient()
        if client.test_connection():
            print("✅ API连接成功！")
            return True
        else:
            print("❌ API连接失败！")
            return False
    except Exception as e:
        print(f"❌ 连接测试异常: {str(e)}")
        return False

def demo_basic_openai_call():
    """演示基础OpenAI调用"""
    print("\n" + "=" * 50)
    print("演示基础OpenAI调用")
    print("=" * 50)
    
    try:
        client = OpenAIRequirementClient()
        
        # 基础调用示例
        messages = [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": "请简单介绍一下需求建模的概念。"}
        ]
        
        completion = client.create_chat_completion(messages)
        response = client.get_completion_text(completion)
        
        print("🤖 AI回复:")
        print(response)
        print("\n✅ 基础调用成功！")
        
    except Exception as e:
        print(f"❌ 基础调用失败: {str(e)}")

def demo_requirement_modeling():
    """演示需求建模功能"""
    print("\n" + "=" * 50)
    print("演示需求建模功能")
    print("=" * 50)
    
    # 示例需求文本
    requirement_text = """
    我们需要开发一个在线图书管理系统。系统应该允许用户注册和登录，
    浏览图书目录，搜索图书，借阅和归还图书。管理员可以添加、编辑和删除图书，
    管理用户账户，查看借阅历史。系统需要支持多用户同时访问，
    响应时间应该在3秒以内，数据需要定期备份。
    """
    
    try:
        client = OpenAIRequirementClient()
        modeler = RequirementModeler(client)
        
        print("📝 需求文本:")
        print(requirement_text.strip())
        print("\n🔄 正在生成需求模型...")
        
        result = modeler.generate_requirement_model(requirement_text)
        
        if result["status"] == "success":
            print("✅ 需求模型生成成功！")
            
            # 导出为JSON格式
            json_output = modeler.export_model(result["requirement_model"], "json")
            print("\n📄 需求模型 (JSON格式):")
            print(json_output)
            
            # 导出为Markdown格式
            md_output = modeler.export_model(result["requirement_model"], "markdown")
            print("\n📄 需求模型 (Markdown格式):")
            print(md_output)
            
            # 保存到文件
            with open("requirement_model.json", "w", encoding="utf-8") as f:
                f.write(json_output)
            print("\n💾 需求模型已保存到 requirement_model.json")
            
        else:
            print(f"❌ 需求模型生成失败: {result.get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 需求建模演示失败: {str(e)}")

def demo_multi_agent_workflow():
    """演示多智能体工作流"""
    print("\n" + "=" * 50)
    print("演示多智能体工作流")
    print("=" * 50)
    
    # 示例需求文本
    requirement_text = """
    开发一个智能客服系统，能够自动回答用户常见问题，
    支持多语言对话，集成知识库，提供24/7服务。
    系统需要具备学习能力，能够从对话中不断改进。
    响应时间要求小于2秒，准确率要求达到90%以上。
    """
    
    try:
        client = OpenAIRequirementClient()
        workflow = MultiAgentWorkflow(client)
        
        print("📝 需求文本:")
        print(requirement_text.strip())
        print("\n🤖 开始多智能体工作流...")
        
        result = workflow.execute_workflow(requirement_text, max_iterations=2)
        
        if result["status"] in ["success", "partial_success"]:
            print("✅ 多智能体工作流执行成功！")
            
            print(f"\n📊 工作流统计:")
            print(f"- 迭代次数: {result['iterations']}")
            print(f"- 状态: {result['status']}")
            
            # 显示验证结果
            validation = result["validation_result"]
            print(f"\n🔍 验证结果:")
            print(f"- 验证状态: {validation['validation_status']}")
            print(f"- 总体评分: {validation.get('overall_score', 'N/A')}")
            
            if validation.get('issues'):
                print(f"- 发现 {len(validation['issues'])} 个问题:")
                for issue in validation['issues']:
                    print(f"  • {issue['type']} ({issue['severity']}): {issue['description']}")
            
            # 保存结果
            with open("multi_agent_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print("\n💾 多智能体结果已保存到 multi_agent_result.json")
            
        else:
            print("❌ 多智能体工作流执行失败")
            
    except Exception as e:
        print(f"❌ 多智能体工作流演示失败: {str(e)}")

def interactive_demo():
    """交互式演示"""
    print("\n" + "=" * 50)
    print("交互式需求建模演示")
    print("=" * 50)
    
    try:
        client = OpenAIRequirementClient()
        modeler = RequirementModeler(client)
        
        print("请输入您的需求描述 (输入 'quit' 退出):")
        
        while True:
            requirement_text = input("\n📝 需求描述: ").strip()
            
            if requirement_text.lower() == 'quit':
                break
                
            if not requirement_text:
                print("请输入有效的需求描述")
                continue
            
            print("\n🔄 正在分析需求...")
            
            result = modeler.generate_requirement_model(requirement_text)
            
            if result["status"] == "success":
                print("✅ 需求分析完成！")
                
                # 显示项目名称
                project_name = result["requirement_model"].get("project_name", "未命名项目")
                print(f"\n📋 项目: {project_name}")
                
                # 显示功能需求数量
                func_reqs = result["requirement_model"].get("functional_requirements", [])
                print(f"🔧 功能需求: {len(func_reqs)} 个")
                
                # 显示非功能需求数量
                non_func_reqs = result["requirement_model"].get("non_functional_requirements", [])
                print(f"⚡ 非功能需求: {len(non_func_reqs)} 个")
                
                # 显示用户故事数量
                user_stories = result["requirement_model"].get("user_stories", [])
                print(f"👥 用户故事: {len(user_stories)} 个")
                
                # 显示验证结果
                validation = result["validation_result"]
                print(f"🔍 验证状态: {validation['validation_status']}")
                
                # 询问是否保存
                save_choice = input("\n💾 是否保存结果到文件? (y/n): ").strip().lower()
                if save_choice == 'y':
                    filename = f"requirement_{project_name.replace(' ', '_')}.json"
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    print(f"✅ 结果已保存到 {filename}")
                
            else:
                print(f"❌ 需求分析失败: {result.get('error', '未知错误')}")
                
    except Exception as e:
        print(f"❌ 交互式演示失败: {str(e)}")

def main():
    """主函数"""
    print("🚀 OpenAI需求建模系统")
    print("基于大语言模型的自动化需求建模工具")
    
    # 测试连接
    if not test_openai_connection():
        print("❌ 无法连接到OpenAI API，请检查网络和配置")
        return
    
    # 基础调用演示
    demo_basic_openai_call()
    
    # 需求建模演示
    demo_requirement_modeling()
    
    # 多智能体工作流演示
    demo_multi_agent_workflow()
    
    # 交互式演示
    interactive_demo()
    
    print("\n🎉 演示完成！感谢使用OpenAI需求建模系统")

if __name__ == "__main__":
    main() 