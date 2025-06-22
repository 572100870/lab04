"""
简单演示脚本 - 展示OpenAI SDK调用和需求建模功能
"""
import json
from openai_client import OpenAIRequirementClient
from requirement_modeler import RequirementModeler

def simple_openai_demo():
    """简单的OpenAI调用演示"""
    print("=" * 60)
    print("🚀 OpenAI SDK 调用演示")
    print("=" * 60)
    
    try:
        # 创建客户端
        client = OpenAIRequirementClient()
        
        # 基础调用示例（参考9.2）
        messages = [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": "请简单介绍一下需求建模的重要性。"}
        ]
        
        print("📡 正在调用OpenAI API...")
        completion = client.create_chat_completion(messages)
        response = client.get_completion_text(completion)
        
        print("🤖 AI回复:")
        print(response)
        print("\n✅ 基础调用成功！")
        
    except Exception as e:
        print(f"❌ 调用失败: {e}")

def requirement_modeling_demo():
    """需求建模演示"""
    print("\n" + "=" * 60)
    print("📋 需求建模演示")
    print("=" * 60)
    
    # 示例需求
    requirement_text = """
    开发一个在线学习平台，支持视频课程播放、在线测验、学习进度跟踪。
    用户可以注册登录，选择课程，观看视频，完成作业，查看成绩。
    教师可以上传课程内容，创建测验，查看学生学习情况。
    系统需要支持移动端访问，响应时间小于2秒。
    """
    
    try:
        client = OpenAIRequirementClient()
        modeler = RequirementModeler(client)
        
        print("📝 需求描述:")
        print(requirement_text.strip())
        print("\n🔄 正在生成需求模型...")
        
        # 生成需求模型
        result = modeler.generate_requirement_model(requirement_text)
        
        if result["status"] == "success":
            print("✅ 需求模型生成成功！")
            
            # 显示项目信息
            model = result["requirement_model"]
            print(f"\n📊 项目统计:")
            print(f"   项目名称: {model.get('project_name', '未命名')}")
            print(f"   功能需求: {len(model.get('functional_requirements', []))} 个")
            print(f"   非功能需求: {len(model.get('non_functional_requirements', []))} 个")
            print(f"   用户故事: {len(model.get('user_stories', []))} 个")
            print(f"   用例: {len(model.get('use_cases', []))} 个")
            
            # 显示验证结果
            validation = result["validation_result"]
            print(f"\n🔍 验证结果:")
            print(f"   验证状态: {validation['validation_status']}")
            print(f"   总体评分: {validation.get('overall_score', 'N/A')}")
            
            # 保存结果
            with open("demo_requirement_model.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print("\n💾 结果已保存到 demo_requirement_model.json")
            
        else:
            print(f"❌ 需求建模失败: {result.get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 需求建模演示失败: {e}")

def main():
    """主函数"""
    print("🎯 OpenAI需求建模系统 - 简单演示")
    print("基于大语言模型的自动化需求建模工具")
    
    # 基础OpenAI调用演示
    simple_openai_demo()
    
    # 需求建模演示
    requirement_modeling_demo()
    
    print("\n🎉 演示完成！")
    print("💡 提示: 运行 main.py 可以体验完整的多智能体工作流")

if __name__ == "__main__":
    main() 