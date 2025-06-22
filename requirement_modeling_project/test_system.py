"""
测试脚本 - 验证系统功能
"""
import json
import requests
from openai_client import OpenAIRequirementModelingClient


def test_openai_client():
    """测试OpenAI客户端"""
    print("=" * 50)
    print("测试OpenAI客户端")
    print("=" * 50)
    
    client = OpenAIRequirementModelingClient()
    
    # 测试需求描述
    test_requirement = """
    开发一个简单的待办事项管理系统，功能包括：
    1. 用户注册和登录
    2. 添加、删除、修改待办事项
    3. 标记待办事项为完成
    4. 查看待办事项列表
    5. 按优先级和状态筛选
    
    系统需要响应快速，界面简洁易用。
    """
    
    print(f"测试需求：{test_requirement}")
    print("\n正在调用OpenAI API...")
    
    try:
        result = client.generate_requirement_model(test_requirement)
        
        if "error" in result:
            print(f"❌ 生成失败：{result['error']}")
            return False
        
        print("✅ 需求模型生成成功！")
        print("\n生成的需求模型：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 验证模型
        validation_result = client.validate_requirement_model(result)
        print(f"\n验证结果：{validation_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_api_server():
    """测试API服务器"""
    print("\n" + "=" * 50)
    print("测试API服务器")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ API服务器运行正常")
        else:
            print(f"❌ API服务器异常：{response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器，请确保服务器已启动")
        return False
    
    # 测试生成需求模型
    test_data = {
        "description": "开发一个简单的笔记应用，支持创建、编辑、删除笔记",
        "enhance": False
    }
    
    try:
        response = requests.post(f"{base_url}/generate", json=test_data)
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("✅ API生成需求模型成功")
                print(f"验证结果：{result['validation_result']}")
                return True
            else:
                print(f"❌ API生成失败：{result['error']}")
                return False
        else:
            print(f"❌ API请求失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API测试失败：{e}")
        return False


def test_curl_command():
    """测试CURL命令"""
    print("\n" + "=" * 50)
    print("测试CURL命令")
    print("=" * 50)
    
    curl_command = '''curl -X POST "https://api.chatfire.cn/v1/chat/completions" \\
  -H "Authorization: Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "你是一个专业的需求分析师和软件架构师，擅长将自然语言需求转换为结构化的需求模型。"
      },
      {
        "role": "user",
        "content": "请为以下需求生成结构化的需求模型：开发一个简单的计算器应用，支持基本的加减乘除运算。请以JSON格式输出需求模型。"
      }
    ],
    "max_tokens": 2000,
    "temperature": 0.7,
    "response_format": {"type": "json_object"}
  }' '''
    
    print("CURL命令：")
    print(curl_command)
    print("\n请复制上述命令并在命令行中执行，验证API调用是否正常。")


def main():
    """主测试函数"""
    print("智能化需求建模系统测试")
    print("=" * 60)
    
    # 测试OpenAI客户端
    client_success = test_openai_client()
    
    # 测试API服务器（如果客户端测试成功）
    if client_success:
        api_success = test_api_server()
    else:
        print("\n跳过API服务器测试（因为客户端测试失败）")
        api_success = False
    
    # 显示CURL命令
    test_curl_command()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"OpenAI客户端测试：{'✅ 通过' if client_success else '❌ 失败'}")
    print(f"API服务器测试：{'✅ 通过' if api_success else '❌ 失败'}")
    
    if client_success:
        print("\n🎉 系统基本功能正常！")
        print("您可以：")
        print("1. 运行 python main.py 进行交互式演示")
        print("2. 运行 python api_server.py 启动API服务器")
        print("3. 使用CURL命令直接调用OpenAI API")
    else:
        print("\n⚠️ 系统存在问题，请检查：")
        print("1. 网络连接是否正常")
        print("2. API密钥是否有效")
        print("3. 依赖包是否正确安装")


if __name__ == "__main__":
    main() 