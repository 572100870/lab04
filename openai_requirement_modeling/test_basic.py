"""
基础功能测试脚本
"""
import sys
import traceback

def test_imports():
    """测试模块导入"""
    print("=" * 50)
    print("测试模块导入")
    print("=" * 50)
    
    try:
        from config import BASE_URL, API_KEY, DEFAULT_MODEL
        print(f"✅ 配置模块导入成功")
        print(f"   BASE_URL: {BASE_URL}")
        print(f"   API_KEY: {API_KEY[:10]}...")
        print(f"   DEFAULT_MODEL: {DEFAULT_MODEL}")
    except Exception as e:
        print(f"❌ 配置模块导入失败: {e}")
        return False
    
    try:
        from openai_client import OpenAIRequirementClient
        print("✅ OpenAI客户端模块导入成功")
    except Exception as e:
        print(f"❌ OpenAI客户端模块导入失败: {e}")
        return False
    
    try:
        from requirement_modeler import RequirementModeler
        print("✅ 需求建模器模块导入成功")
    except Exception as e:
        print(f"❌ 需求建模器模块导入失败: {e}")
        return False
    
    try:
        from multi_agent_workflow import MultiAgentWorkflow
        print("✅ 多智能体工作流模块导入成功")
    except Exception as e:
        print(f"❌ 多智能体工作流模块导入失败: {e}")
        return False
    
    return True

def test_client_creation():
    """测试客户端创建"""
    print("\n" + "=" * 50)
    print("测试客户端创建")
    print("=" * 50)
    
    try:
        from openai_client import OpenAIRequirementClient
        client = OpenAIRequirementClient()
        print("✅ OpenAI客户端创建成功")
        print(f"   模型: {client.model}")
        print(f"   温度: {client.temperature}")
        print(f"   最大Token: {client.max_tokens}")
        return True
    except Exception as e:
        print(f"❌ 客户端创建失败: {e}")
        traceback.print_exc()
        return False

def test_modeler_creation():
    """测试建模器创建"""
    print("\n" + "=" * 50)
    print("测试建模器创建")
    print("=" * 50)
    
    try:
        from openai_client import OpenAIRequirementClient
        from requirement_modeler import RequirementModeler
        
        client = OpenAIRequirementClient()
        modeler = RequirementModeler(client)
        print("✅ 需求建模器创建成功")
        return True
    except Exception as e:
        print(f"❌ 建模器创建失败: {e}")
        traceback.print_exc()
        return False

def test_workflow_creation():
    """测试工作流创建"""
    print("\n" + "=" * 50)
    print("测试工作流创建")
    print("=" * 50)
    
    try:
        from openai_client import OpenAIRequirementClient
        from multi_agent_workflow import MultiAgentWorkflow
        
        client = OpenAIRequirementClient()
        workflow = MultiAgentWorkflow(client)
        print("✅ 多智能体工作流创建成功")
        print(f"   智能体数量: {len(workflow.agents)}")
        return True
    except Exception as e:
        print(f"❌ 工作流创建失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🧪 OpenAI需求建模系统 - 基础功能测试")
    
    # 测试导入
    if not test_imports():
        print("\n❌ 模块导入测试失败，请检查依赖安装")
        return
    
    # 测试客户端创建
    if not test_client_creation():
        print("\n❌ 客户端创建测试失败")
        return
    
    # 测试建模器创建
    if not test_modeler_creation():
        print("\n❌ 建模器创建测试失败")
        return
    
    # 测试工作流创建
    if not test_workflow_creation():
        print("\n❌ 工作流创建测试失败")
        return
    
    print("\n🎉 所有基础功能测试通过！")
    print("系统已准备就绪，可以运行 main.py 进行完整演示")

if __name__ == "__main__":
    main() 