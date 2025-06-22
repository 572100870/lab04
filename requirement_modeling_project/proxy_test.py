"""
代理配置测试脚本 - 帮助找到正确的代理端口
"""
import requests
import json
from config import PROXY_CONFIG, PROXY_CONFIG_ALTERNATIVE


def test_proxy_connection(proxy_config, name):
    """测试代理连接"""
    print(f"\n测试 {name}...")
    print(f"代理配置: {proxy_config}")
    
    try:
        # 测试基本连接
        response = requests.get(
            "https://httpbin.org/ip", 
            proxies=proxy_config, 
            timeout=10
        )
        if response.status_code == 200:
            ip_info = response.json()
            print(f"✅ {name} 连接成功!")
            print(f"   当前IP: {ip_info.get('origin', 'Unknown')}")
            return True
        else:
            print(f"❌ {name} 连接失败: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} 连接失败: {e}")
        return False


def test_openai_api_with_proxy(proxy_config, name):
    """测试使用代理访问OpenAI API"""
    print(f"\n测试使用 {name} 访问OpenAI API...")
    
    headers = {
        "Authorization": "Bearer sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Hello, this is a test message."
            }
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://api.chatfire.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            proxies=proxy_config,
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ {name} OpenAI API 访问成功!")
            return True
        else:
            print(f"❌ {name} OpenAI API 访问失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} OpenAI API 访问失败: {e}")
        return False


def test_common_proxy_ports():
    """测试常见的代理端口"""
    print("=" * 60)
    print("测试常见代理端口")
    print("=" * 60)
    
    common_ports = [7890, 1080, 8080, 8118, 3128, 8888, 10809, 10808]
    
    for port in common_ports:
        proxy_config = {
            "http": f"http://127.0.0.1:{port}",
            "https": f"http://127.0.0.1:{port}"
        }
        
        print(f"\n测试端口 {port}...")
        if test_proxy_connection(proxy_config, f"端口 {port}"):
            print(f"✅ 端口 {port} 可用!")
            
            # 如果基本连接成功，测试OpenAI API
            if test_openai_api_with_proxy(proxy_config, f"端口 {port}"):
                print(f"🎉 端口 {port} 完全可用，可以用于OpenAI API!")
                return port
    
    return None


def main():
    """主函数"""
    print("代理配置测试工具")
    print("=" * 60)
    
    # 测试预配置的代理
    print("1. 测试预配置的代理...")
    
    # 测试主代理配置
    main_proxy_works = test_proxy_connection(PROXY_CONFIG, "主代理配置 (7890)")
    if main_proxy_works:
        test_openai_api_with_proxy(PROXY_CONFIG, "主代理配置 (7890)")
    
    # 测试备用代理配置
    alt_proxy_works = test_proxy_connection(PROXY_CONFIG_ALTERNATIVE, "备用代理配置 (1080)")
    if alt_proxy_works:
        test_openai_api_with_proxy(PROXY_CONFIG_ALTERNATIVE, "备用代理配置 (1080)")
    
    # 测试无代理
    print("\n2. 测试无代理连接...")
    try:
        response = requests.get("https://httpbin.org/ip", timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            print(f"✅ 无代理连接成功! IP: {ip_info.get('origin', 'Unknown')}")
        else:
            print("❌ 无代理连接失败")
    except Exception as e:
        print(f"❌ 无代理连接失败: {e}")
    
    # 测试常见端口
    print("\n3. 测试常见代理端口...")
    working_port = test_common_proxy_ports()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if main_proxy_works:
        print("✅ 主代理配置 (7890) 可用")
    else:
        print("❌ 主代理配置 (7890) 不可用")
    
    if alt_proxy_works:
        print("✅ 备用代理配置 (1080) 可用")
    else:
        print("❌ 备用代理配置 (1080) 不可用")
    
    if working_port:
        print(f"✅ 找到可用端口: {working_port}")
        print(f"建议更新 config.py 中的代理配置为端口 {working_port}")
    else:
        print("❌ 未找到可用的代理端口")
    
    print("\n如果所有代理都不可用，请检查：")
    print("1. VPN是否已正确启动")
    print("2. 代理端口是否正确")
    print("3. 防火墙是否阻止了连接")


if __name__ == "__main__":
    main() 