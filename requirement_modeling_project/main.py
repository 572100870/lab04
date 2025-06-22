"""
主程序 - 演示基于OpenAI API的智能化需求建模
"""
import json
import sys
from openai_client import OpenAIRequirementModelingClient
from requirement_model import validate_requirement_model, requirement_model_to_json


def demo_basic_requirement_modeling():
    """演示基础需求建模功能"""
    print("=" * 60)
    print("基于OpenAI API的智能化需求建模演示")
    print("=" * 60)
    
    # 创建客户端
    client = OpenAIRequirementModelingClient()
    
    # 示例需求描述
    requirement_description = """
    开发一个在线图书管理系统，主要功能包括：
    1. 用户注册和登录功能
    2. 图书信息管理（添加、修改、删除图书）
    3. 图书搜索和查询功能
    4. 图书借阅和归还功能
    5. 借阅历史记录查询
    6. 用户权限管理
    
    系统需要支持多用户同时访问，响应时间要求在3秒内。
    数据需要安全存储，支持备份和恢复。
    界面要简洁易用，支持移动端访问。
    """
    
    print(f"需求描述：\n{requirement_description}")
    print("\n正在生成需求模型...")
    
    # 生成需求模型
    result = client.generate_requirement_model(requirement_description)
    
    if "error" in result:
        print(f"生成失败：{result['error']}")
        return
    
    print("\n生成的需求模型：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 验证模型
    print("\n正在验证需求模型...")
    validation_result = client.validate_requirement_model(result)
    
    print(f"验证结果：")
    print(f"  是否有效：{validation_result['is_valid']}")
    if validation_result['missing_fields']:
        print(f"  缺失字段：{validation_result['missing_fields']}")
    if validation_result['suggestions']:
        print(f"  建议：{validation_result['suggestions']}")
    
    # 尝试使用Pydantic验证
    try:
        validated_model = validate_requirement_model(result)
        print("\nPydantic验证成功！")
        
        # 转换为格式化的JSON
        formatted_json = requirement_model_to_json(validated_model)
        print("\n格式化后的需求模型：")
        print(formatted_json)
        
    except Exception as e:
        print(f"\nPydantic验证失败：{e}")
    
    return result


def demo_enhanced_requirement_modeling():
    """演示增强需求建模功能"""
    print("\n" + "=" * 60)
    print("增强需求建模演示")
    print("=" * 60)
    
    # 创建客户端
    client = OpenAIRequirementModelingClient()
    
    # 基础需求描述
    requirement_description = """
    开发一个智能客服系统，具备以下功能：
    1. 自动回答常见问题
    2. 智能路由用户问题到合适的客服人员
    3. 支持多语言对话
    4. 集成知识库管理
    5. 提供实时聊天功能
    6. 生成客服报告和统计
    
    系统需要高可用性，支持7x24小时运行。
    响应时间要求快速，用户体验要好。
    需要支持大规模并发访问。
    """
    
    print(f"需求描述：\n{requirement_description}")
    print("\n正在生成基础需求模型...")
    
    # 生成基础模型
    base_model = client.generate_requirement_model(requirement_description)
    
    if "error" in base_model:
        print(f"生成失败：{base_model['error']}")
        return
    
    print("\n基础需求模型生成完成")
    
    # 增强模型
    print("\n正在增强需求模型...")
    enhanced_model = client.enhance_requirement_model(base_model)
    
    print("\n增强后的需求模型：")
    print(json.dumps(enhanced_model, ensure_ascii=False, indent=2))
    
    return enhanced_model


def demo_curl_command():
    """演示curl命令调用"""
    print("\n" + "=" * 60)
    print("CURL命令演示")
    print("=" * 60)
    
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
        "content": "请为以下需求生成结构化的需求模型：开发一个简单的待办事项管理系统，支持添加、删除、修改和查看待办事项。系统需要用户登录功能，数据需要持久化存储。请以JSON格式输出需求模型。"
      }
    ],
    "max_tokens": 4000,
    "temperature": 0.7,
    "response_format": {"type": "json_object"}
  }' '''
    
    print("CURL命令：")
    print(curl_command)
    
    print("\n使用说明：")
    print("1. 复制上述curl命令")
    print("2. 在命令行中执行")
    print("3. 查看返回的JSON格式需求模型")


def save_model_to_file(model: dict, filename: str):
    """保存模型到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(model, f, ensure_ascii=False, indent=2)
        print(f"\n需求模型已保存到：{filename}")
    except Exception as e:
        print(f"保存失败：{e}")


def main():
    """主函数"""
    print("基于大语言模型辅助的智能化需求建模系统")
    print("=" * 60)
    
    while True:
        print("\n请选择操作：")
        print("1. 基础需求建模演示")
        print("2. 增强需求建模演示")
        print("3. 显示CURL命令")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            model = demo_basic_requirement_modeling()
            if model and "error" not in model:
                save_choice = input("\n是否保存模型到文件？(y/n): ").strip().lower()
                if save_choice == 'y':
                    save_model_to_file(model, "basic_requirement_model.json")
        
        elif choice == "2":
            model = demo_enhanced_requirement_modeling()
            if model and "error" not in model:
                save_choice = input("\n是否保存模型到文件？(y/n): ").strip().lower()
                if save_choice == 'y':
                    save_model_to_file(model, "enhanced_requirement_model.json")
        
        elif choice == "3":
            demo_curl_command()
        
        elif choice == "4":
            print("感谢使用！")
            break
        
        else:
            print("无效选择，请重新输入。")


if __name__ == "__main__":
    main() 