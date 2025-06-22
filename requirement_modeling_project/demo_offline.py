"""
离线演示版本 - 展示智能化需求建模系统功能
"""
import json
from requirement_model import validate_requirement_model, requirement_model_to_json


def demo_requirement_model_structure():
    """演示需求模型结构"""
    print("=" * 60)
    print("智能化需求建模系统 - 离线演示")
    print("=" * 60)
    
    # 示例需求模型
    sample_model = {
        "project_name": "在线图书管理系统",
        "description": "一个基于Web的图书管理系统，支持图书借阅、归还、查询等功能",
        "stakeholders": [
            {
                "name": "图书管理员",
                "role": "系统管理员",
                "responsibilities": ["图书管理", "用户管理", "借阅记录管理"]
            },
            {
                "name": "普通用户",
                "role": "读者",
                "responsibilities": ["图书查询", "借阅申请", "个人信息管理"]
            }
        ],
        "functional_requirements": [
            {
                "id": "FR001",
                "title": "用户注册和登录功能",
                "description": "用户可以通过邮箱注册账号，使用用户名和密码登录系统",
                "priority": "高",
                "acceptance_criteria": [
                    "用户可以使用邮箱注册新账号",
                    "用户可以使用用户名和密码登录",
                    "系统验证用户身份并分配相应权限",
                    "支持密码重置功能"
                ]
            },
            {
                "id": "FR002",
                "title": "图书信息管理",
                "description": "管理员可以添加、修改、删除图书信息",
                "priority": "高",
                "acceptance_criteria": [
                    "管理员可以添加新图书信息",
                    "管理员可以修改现有图书信息",
                    "管理员可以删除图书信息",
                    "支持图书分类管理"
                ]
            },
            {
                "id": "FR003",
                "title": "图书搜索和查询",
                "description": "用户可以通过多种方式搜索和查询图书",
                "priority": "高",
                "acceptance_criteria": [
                    "支持按书名搜索",
                    "支持按作者搜索",
                    "支持按ISBN搜索",
                    "支持按分类浏览",
                    "显示图书详细信息"
                ]
            },
            {
                "id": "FR004",
                "title": "图书借阅和归还",
                "description": "用户可以借阅和归还图书，系统记录借阅历史",
                "priority": "高",
                "acceptance_criteria": [
                    "用户可以申请借阅图书",
                    "系统检查图书可用性",
                    "记录借阅时间和归还期限",
                    "用户可以归还图书",
                    "系统更新图书状态"
                ]
            }
        ],
        "non_functional_requirements": [
            {
                "id": "NFR001",
                "category": "性能",
                "title": "响应时间要求",
                "description": "系统响应时间应在3秒内",
                "metrics": "页面加载时间 < 3秒，API响应时间 < 1秒"
            },
            {
                "id": "NFR002",
                "category": "安全性",
                "title": "数据安全要求",
                "description": "用户数据需要加密存储，防止未授权访问",
                "metrics": "使用HTTPS协议，密码加密存储，定期数据备份"
            },
            {
                "id": "NFR003",
                "category": "可用性",
                "title": "系统可用性要求",
                "description": "系统需要高可用性，支持7x24小时运行",
                "metrics": "系统可用性 > 99.5%，故障恢复时间 < 30分钟"
            }
        ],
        "use_cases": [
            {
                "id": "UC001",
                "title": "用户登录",
                "actor": "用户",
                "preconditions": ["用户已注册账号"],
                "main_flow": [
                    "用户访问登录页面",
                    "用户输入用户名和密码",
                    "系统验证用户凭据",
                    "验证成功，用户登录系统",
                    "系统显示用户主页面"
                ],
                "postconditions": ["用户成功登录系统", "系统记录登录日志"]
            },
            {
                "id": "UC002",
                "title": "图书借阅",
                "actor": "用户",
                "preconditions": ["用户已登录", "图书可借阅"],
                "main_flow": [
                    "用户搜索或浏览图书",
                    "用户选择要借阅的图书",
                    "用户点击借阅按钮",
                    "系统检查用户借阅资格",
                    "系统检查图书可用性",
                    "系统创建借阅记录",
                    "系统更新图书状态",
                    "系统发送借阅确认信息"
                ],
                "postconditions": ["图书借阅成功", "借阅记录已创建", "图书状态已更新"]
            }
        ],
        "data_models": [
            {
                "name": "用户模型",
                "description": "用户基本信息",
                "attributes": [
                    {
                        "name": "user_id",
                        "type": "Integer",
                        "description": "用户唯一标识",
                        "constraints": "主键，自增"
                    },
                    {
                        "name": "username",
                        "type": "String",
                        "description": "用户名",
                        "constraints": "唯一，长度3-20字符"
                    },
                    {
                        "name": "email",
                        "type": "String",
                        "description": "邮箱地址",
                        "constraints": "唯一，有效邮箱格式"
                    },
                    {
                        "name": "password_hash",
                        "type": "String",
                        "description": "密码哈希",
                        "constraints": "加密存储"
                    },
                    {
                        "name": "role",
                        "type": "Enum",
                        "description": "用户角色",
                        "constraints": "admin, user"
                    }
                ]
            },
            {
                "name": "图书模型",
                "description": "图书信息",
                "attributes": [
                    {
                        "name": "book_id",
                        "type": "Integer",
                        "description": "图书唯一标识",
                        "constraints": "主键，自增"
                    },
                    {
                        "name": "title",
                        "type": "String",
                        "description": "图书标题",
                        "constraints": "非空，长度1-200字符"
                    },
                    {
                        "name": "author",
                        "type": "String",
                        "description": "作者",
                        "constraints": "非空，长度1-100字符"
                    },
                    {
                        "name": "isbn",
                        "type": "String",
                        "description": "ISBN号",
                        "constraints": "唯一，标准ISBN格式"
                    },
                    {
                        "name": "category",
                        "type": "String",
                        "description": "图书分类",
                        "constraints": "非空"
                    },
                    {
                        "name": "status",
                        "type": "Enum",
                        "description": "图书状态",
                        "constraints": "available, borrowed, reserved"
                    }
                ]
            }
        ],
        "system_architecture": {
            "overview": "采用MVC架构模式，前后端分离设计",
            "components": [
                {
                    "name": "前端界面层",
                    "description": "用户交互界面",
                    "responsibilities": ["用户界面展示", "用户交互处理", "数据展示"]
                },
                {
                    "name": "业务逻辑层",
                    "description": "核心业务处理",
                    "responsibilities": ["业务规则处理", "数据验证", "业务流程控制"]
                },
                {
                    "name": "数据访问层",
                    "description": "数据持久化",
                    "responsibilities": ["数据库操作", "数据查询", "数据存储"]
                },
                {
                    "name": "认证授权模块",
                    "description": "用户认证和权限管理",
                    "responsibilities": ["用户认证", "权限验证", "会话管理"]
                }
            ],
            "interfaces": [
                {
                    "name": "用户认证接口",
                    "description": "用户登录认证",
                    "input": "用户名、密码",
                    "output": "认证结果、用户信息、访问令牌"
                },
                {
                    "name": "图书管理接口",
                    "description": "图书信息管理",
                    "input": "图书信息、操作类型",
                    "output": "操作结果、图书列表"
                },
                {
                    "name": "借阅管理接口",
                    "description": "图书借阅和归还",
                    "input": "用户ID、图书ID、操作类型",
                    "output": "操作结果、借阅记录"
                }
            ]
        }
    }
    
    print("📋 需求模型结构演示")
    print("\n1. 项目基本信息:")
    print(f"   项目名称: {sample_model['project_name']}")
    print(f"   项目描述: {sample_model['description']}")
    
    print(f"\n2. 利益相关者 ({len(sample_model['stakeholders'])}个):")
    for i, stakeholder in enumerate(sample_model['stakeholders'], 1):
        print(f"   {i}. {stakeholder['name']} - {stakeholder['role']}")
        print(f"      职责: {', '.join(stakeholder['responsibilities'])}")
    
    print(f"\n3. 功能需求 ({len(sample_model['functional_requirements'])}个):")
    for req in sample_model['functional_requirements']:
        print(f"   {req['id']}: {req['title']} (优先级: {req['priority']})")
        print(f"      描述: {req['description']}")
        print(f"      验收标准: {len(req['acceptance_criteria'])}项")
    
    print(f"\n4. 非功能需求 ({len(sample_model['non_functional_requirements'])}个):")
    for req in sample_model['non_functional_requirements']:
        print(f"   {req['id']}: {req['title']} (类别: {req['category']})")
        print(f"      指标: {req['metrics']}")
    
    print(f"\n5. 用例 ({len(sample_model['use_cases'])}个):")
    for uc in sample_model['use_cases']:
        print(f"   {uc['id']}: {uc['title']} (参与者: {uc['actor']})")
        print(f"      流程步骤: {len(uc['main_flow'])}步")
    
    print(f"\n6. 数据模型 ({len(sample_model['data_models'])}个):")
    for model in sample_model['data_models']:
        print(f"   {model['name']}: {model['description']}")
        print(f"      属性数量: {len(model['attributes'])}个")
    
    print(f"\n7. 系统架构:")
    print(f"   概述: {sample_model['system_architecture']['overview']}")
    print(f"   组件数量: {len(sample_model['system_architecture']['components'])}个")
    print(f"   接口数量: {len(sample_model['system_architecture']['interfaces'])}个")
    
    return sample_model


def demo_model_validation():
    """演示模型验证功能"""
    print("\n" + "=" * 60)
    print("需求模型验证演示")
    print("=" * 60)
    
    # 创建一个有问题的模型
    invalid_model = {
        "project_name": "测试项目",
        "description": "这是一个测试项目",
        # 缺少必要的字段
        "functional_requirements": [
            {
                "title": "缺少ID的功能需求",  # 缺少id字段
                "description": "这是一个有问题的需求"
            }
        ]
    }
    
    print("验证有问题的需求模型...")
    
    # 验证模型
    try:
        validated_model = validate_requirement_model(invalid_model)
        print("✅ 模型验证通过")
    except Exception as e:
        print(f"❌ 模型验证失败: {e}")
        print("这是预期的结果，因为模型缺少必要字段")
    
    # 验证完整模型
    print("\n验证完整的需求模型...")
    complete_model = demo_requirement_model_structure()
    
    try:
        validated_model = validate_requirement_model(complete_model)
        print("✅ 完整模型验证通过")
        
        # 转换为JSON
        json_output = requirement_model_to_json(validated_model)
        print(f"\nJSON输出长度: {len(json_output)} 字符")
        print("JSON格式正确，可以用于API响应")
        
    except Exception as e:
        print(f"❌ 完整模型验证失败: {e}")


def demo_api_format():
    """演示API格式"""
    print("\n" + "=" * 60)
    print("API格式演示")
    print("=" * 60)
    
    # 模拟API请求
    api_request = {
        "description": "开发一个在线图书管理系统",
        "model": "gpt-3.5-turbo",
        "max_tokens": 4000,
        "temperature": 0.7,
        "enhance": True
    }
    
    print("API请求格式:")
    print(json.dumps(api_request, ensure_ascii=False, indent=2))
    
    # 模拟API响应
    api_response = {
        "success": True,
        "data": {
            "project_name": "在线图书管理系统",
            "description": "一个基于Web的图书管理系统",
            "functional_requirements": [
                {
                    "id": "FR001",
                    "title": "用户登录功能",
                    "description": "用户可以通过用户名和密码登录系统",
                    "priority": "高",
                    "acceptance_criteria": ["支持用户名密码登录", "验证用户身份"]
                }
            ]
        },
        "validation_result": {
            "is_valid": True,
            "missing_fields": [],
            "suggestions": []
        }
    }
    
    print("\nAPI响应格式:")
    print(json.dumps(api_response, ensure_ascii=False, indent=2))


def demo_curl_command():
    """演示CURL命令"""
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
    
    print("CURL命令示例:")
    print(curl_command)
    
    print("\n使用说明:")
    print("1. 复制上述curl命令")
    print("2. 在命令行中执行")
    print("3. 查看返回的JSON格式需求模型")
    print("4. 如果使用代理，可能需要添加代理参数")


def main():
    """主函数"""
    print("基于大语言模型的智能化需求建模系统 - 离线演示")
    print("=" * 80)
    
    # 演示需求模型结构
    demo_requirement_model_structure()
    
    # 演示模型验证
    demo_model_validation()
    
    # 演示API格式
    demo_api_format()
    
    # 演示CURL命令
    demo_curl_command()
    
    print("\n" + "=" * 80)
    print("演示总结")
    print("=" * 80)
    print("✅ 系统功能演示完成")
    print("\n主要功能:")
    print("1. 📋 结构化需求模型生成")
    print("2. 🔍 需求模型验证")
    print("3. 🌐 RESTful API接口")
    print("4. 📝 JSON格式输出")
    print("5. 🔧 CURL命令支持")
    
    print("\n下一步:")
    print("1. 配置正确的代理设置")
    print("2. 运行 python test_system.py 进行在线测试")
    print("3. 运行 python main.py 进行交互式演示")
    print("4. 运行 python api_server.py 启动API服务器")


if __name__ == "__main__":
    main() 