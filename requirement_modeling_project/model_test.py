"""
模型测试脚本 - 测试不同的模型
"""
import requests
import json


def test_model(model_name):
    """测试特定模型"""
    print(f"\n测试模型: {model_name}")
    print("-" * 40)
    
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    
    headers = {
        "Authorization": "Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "Hello, please respond with 'Test successful'"
            }
        ],
        "max_tokens": 50
    }
    
    try:
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
            print("✅ 模型可用!")
            print(f"响应: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ 模型不可用: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def test_available_models():
    """测试可用的模型"""
    print("=" * 60)
    print("测试可用模型")
    print("=" * 60)
    
    # 常见的模型列表
    models_to_test = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "claude-3-sonnet",
        "claude-3-haiku",
        "claude-3-opus",
        "qwen-turbo",
        "qwen-plus",
        "qwen-max",
        "gemini-pro",
        "llama-3-8b",
        "llama-3-70b"
    ]
    
    available_models = []
    
    for model in models_to_test:
        if test_model(model):
            available_models.append(model)
    
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    
    if available_models:
        print("✅ 可用的模型:")
        for model in available_models:
            print(f"   - {model}")
        
        print(f"\n建议使用模型: {available_models[0]}")
        print("请更新 config.py 中的 DEFAULT_MODEL 配置")
        
        return available_models[0]
    else:
        print("❌ 没有找到可用的模型")
        print("请检查API密钥的权限或联系服务提供商")
        return None


def test_models_list():
    """获取可用模型列表"""
    print("\n" + "=" * 60)
    print("获取可用模型列表")
    print("=" * 60)
    
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    
    headers = {
        "Authorization": "Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"
    }
    
    try:
        response = requests.get(
            "https://api.chatfire.cn/v1/models",
            headers=headers,
            proxies=proxies,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功获取模型列表!")
            print(f"可用模型数量: {len(result.get('data', []))}")
            
            for model in result.get('data', []):
                model_id = model.get('id', 'Unknown')
                print(f"   - {model_id}")
            
            return result.get('data', [])
        else:
            print(f"❌ 获取模型列表失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return []


def main():
    """主函数"""
    print("模型可用性测试")
    print("=" * 60)
    
    # 首先尝试获取模型列表
    models_list = test_models_list()
    
    # 然后测试常见模型
    working_model = test_available_models()
    
    if working_model:
        print(f"\n🎉 找到可用模型: {working_model}")
        print("现在可以运行完整的需求建模系统了!")
        
        # 更新配置文件
        print(f"\n请将 config.py 中的 DEFAULT_MODEL 更新为: {working_model}")
        
    else:
        print("\n⚠️ 未找到可用模型")
        print("请检查API密钥权限或联系服务提供商")


if __name__ == "__main__":
    main() 