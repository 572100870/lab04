"""
简单的API测试脚本
"""
import requests
import json


def test_api_key():
    """测试API密钥"""
    print("=" * 50)
    print("测试API密钥")
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
    
    # 简单的测试请求
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Hello, please respond with 'Test successful'"
            }
        ],
        "max_tokens": 50
    }
    
    try:
        print("正在测试API连接...")
        response = requests.post(
            "https://api.chatfire.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            proxies=proxies,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return True
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def test_without_proxy():
    """测试不使用代理"""
    print("\n" + "=" * 50)
    print("测试不使用代理")
    print("=" * 50)
    
    headers = {
        "Authorization": "Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Hello"
            }
        ],
        "max_tokens": 50
    }
    
    try:
        print("正在测试无代理连接...")
        response = requests.post(
            "https://api.chatfire.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            proxies=None,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 无代理连接成功!")
            return True
        else:
            print(f"❌ 无代理连接失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 无代理请求异常: {e}")
        return False


def test_curl_command():
    """提供CURL命令用于手动测试"""
    print("\n" + "=" * 50)
    print("CURL命令测试")
    print("=" * 50)
    
    curl_command = '''curl -X POST "https://api.chatfire.cn/v1/chat/completions" \\
  -H "Authorization: Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON" \\
  -H "Content-Type: application/json" \\
  --proxy http://127.0.0.1:7890 \\
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Hello, this is a test"
      }
    ],
    "max_tokens": 50
  }' '''
    
    print("CURL命令（带代理）:")
    print(curl_command)
    
    print("\nCURL命令（不带代理）:")
    curl_command_no_proxy = '''curl -X POST "https://api.chatfire.cn/v1/chat/completions" \\
  -H "Authorization: Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Hello, this is a test"
      }
    ],
    "max_tokens": 50
  }' '''
    print(curl_command_no_proxy)


def main():
    """主函数"""
    print("API连接测试")
    print("=" * 60)
    
    # 测试带代理的API调用
    proxy_success = test_api_key()
    
    # 测试不带代理的API调用
    no_proxy_success = test_without_proxy()
    
    # 提供CURL命令
    test_curl_command()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"带代理测试: {'✅ 成功' if proxy_success else '❌ 失败'}")
    print(f"无代理测试: {'✅ 成功' if no_proxy_success else '❌ 失败'}")
    
    if proxy_success or no_proxy_success:
        print("\n🎉 API连接正常，可以继续使用系统!")
    else:
        print("\n⚠️ API连接失败，请检查:")
        print("1. VPN是否正常工作")
        print("2. API密钥是否有效")
        print("3. 网络连接是否正常")
        print("4. 尝试使用提供的CURL命令手动测试")


if __name__ == "__main__":
    main() 