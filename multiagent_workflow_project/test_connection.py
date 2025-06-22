#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络连接和API配置测试脚本
"""

import asyncio
import httpx
from openai import AsyncOpenAI
from config import config, PROXIES

async def test_network_connection():
    """测试网络连接"""
    print("🌐 测试网络连接...")
    
    try:
        async with httpx.AsyncClient(proxy=PROXIES, timeout=10.0) as client:
            response = await client.get("https://httpbin.org/ip")
            print(f"✅ 网络连接成功")
            print(f"   代理IP: {response.json()}")
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return False
    
    return True

async def test_openai_connection():
    """测试OpenAI API连接"""
    print("\n🔗 测试OpenAI API连接...")
    
    try:
        client = AsyncOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            http_client=httpx.AsyncClient(proxy=PROXIES, timeout=30.0)
        )
        
        # 测试简单的API调用
        response = await client.chat.completions.create(
            model=config.model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print(f"✅ OpenAI API连接成功")
        print(f"   模型: {config.model}")
        print(f"   响应: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API连接失败: {e}")
        return False

async def test_agents_import():
    """测试agents包导入"""
    print("\n📦 测试agents包导入...")
    
    try:
        from agents import Runner, RunConfig, OpenAIProvider
        print("✅ agents包导入成功")
        
        # 测试Agent创建
        from my_agents import requirements_analyst
        print("✅ 本地Agent导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ agents包导入失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🔧 MultiAgent Workflow 连接测试")
    print("=" * 50)
    
    # 显示配置信息
    print(f"📋 配置信息:")
    print(f"   Base URL: {config.base_url}")
    print(f"   API Key: {config.api_key[:10]}...")
    print(f"   代理: {config.proxy_host}:{config.proxy_port}")
    print(f"   模型: {config.model}")
    
    # 运行测试
    network_ok = await test_network_connection()
    agents_ok = await test_agents_import()
    openai_ok = await test_openai_connection()
    
    print("\n📊 测试结果:")
    print(f"   网络连接: {'✅ 通过' if network_ok else '❌ 失败'}")
    print(f"   Agents包: {'✅ 通过' if agents_ok else '❌ 失败'}")
    print(f"   OpenAI API: {'✅ 通过' if openai_ok else '❌ 失败'}")
    
    if all([network_ok, agents_ok, openai_ok]):
        print("\n🎉 所有测试通过！可以运行完整演示。")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查配置。")
        return False

if __name__ == "__main__":
    asyncio.run(main()) 