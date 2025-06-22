"""
测试gpt-4o模型
"""
import requests
import json


def test_gpt4o_model():
    """测试gpt-4o模型"""
    print("=" * 50)
    print("测试gpt-4o模型")
    print("=" * 50)
    
    # 代理配置
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    
    headers = {
        "Authorization": "Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON",
        "Content-Type": "application/json"
    }
    
    # 使用您提供的格式
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "developer",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello! Please respond with 'Test successful'"
            }
        ]
    }
    
    try:
        print("正在测试gpt-4o模型...")
        response = requests.post(
            "https://api.chatfire.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            proxies=proxies,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ gpt-4o模型测试成功!")
            print(f"响应内容: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ gpt-4o模型测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def test_requirement_modeling():
    """测试需求建模功能"""
    print("\n" + "=" * 50)
    print("测试需求建模功能")
    print("=" * 50)
    
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    
    headers = {
        "Authorization": "Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON",
        "Content-Type": "application/json"
    }
    
    # 需求建模请求
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "developer",
                "content": "你是一个专业的需求分析师和软件架构师，擅长将自然语言需求转换为结构化的需求模型。"
            },
            {
                "role": "user",
                "content": "请为以下需求生成结构化的需求模型：开发一个简单的待办事项管理系统，支持添加、删除、修改和查看待办事项。系统需要用户登录功能，数据需要持久化存储。请以JSON格式输出需求模型。"
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }
    
    try:
        print("正在测试需求建模...")
        response = requests.post(
            "https://api.chatfire.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            proxies=proxies,
            timeout=60
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print("✅ 需求建模测试成功!")
            
            # 尝试解析JSON
            try:
                requirement_model = json.loads(content)
                print("✅ JSON解析成功!")
                print(f"项目名称: {requirement_model.get('project_name', 'N/A')}")
                print(f"功能需求数量: {len(requirement_model.get('functional_requirements', []))}")
                print(f"用例数量: {len(requirement_model.get('use_cases', []))}")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应: {content}")
                return False
        else:
            print(f"❌ 需求建模测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def main():
    """主函数"""
    print("gpt-4o模型和需求建模功能测试")
    print("=" * 60)
    
    # 测试基本模型功能
    basic_success = test_gpt4o_model()
    
    # 测试需求建模功能
    if basic_success:
        modeling_success = test_requirement_modeling()
    else:
        print("\n跳过需求建模测试（因为基本模型测试失败）")
        modeling_success = False
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"基本模型测试: {'✅ 成功' if basic_success else '❌ 失败'}")
    print(f"需求建模测试: {'✅ 成功' if modeling_success else '❌ 失败'}")
    
    if basic_success and modeling_success:
        print("\n🎉 所有测试通过！系统可以正常工作了!")
        print("现在可以运行完整的需求建模系统:")
        print("1. python main.py - 交互式演示")
        print("2. python api_server.py - 启动API服务器")
        print("3. python test_system.py - 完整系统测试")
    else:
        print("\n⚠️ 部分测试失败，请检查配置")


if __name__ == "__main__":
    main() 