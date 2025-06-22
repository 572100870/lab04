"""
OpenAI API客户端 - 用于调用大语言模型进行需求建模
"""
import json
import requests
from typing import Dict, Any, Optional
from config import BASE_URL, API_KEY, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE, REQUIREMENT_MODELING_PROMPT, PROXY_CONFIG, PROXY_CONFIG_ALTERNATIVE


class OpenAIRequirementModelingClient:
    """OpenAI需求建模客户端"""
    
    def __init__(self, base_url: str = BASE_URL, api_key: str = API_KEY, use_proxy: bool = True):
        self.base_url = base_url
        self.api_key = api_key
        self.use_proxy = use_proxy
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 设置代理
        if use_proxy:
            self.proxies = PROXY_CONFIG
        else:
            self.proxies = None
    
    def _make_request(self, url: str, payload: Dict[str, Any], retry_with_alternative_proxy: bool = True) -> Dict[str, Any]:
        """
        发送HTTP请求，支持代理重试
        
        Args:
            url: 请求URL
            payload: 请求数据
            retry_with_alternative_proxy: 是否在失败时尝试备用代理
            
        Returns:
            响应结果
        """
        try:
            # 首先尝试主代理配置
            response = requests.post(
                url, 
                headers=self.headers, 
                json=payload, 
                proxies=self.proxies,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"主代理请求失败: {e}")
            
            # 如果启用了代理且允许重试，尝试备用代理
            if self.use_proxy and retry_with_alternative_proxy:
                print("尝试使用备用代理...")
                try:
                    response = requests.post(
                        url, 
                        headers=self.headers, 
                        json=payload, 
                        proxies=PROXY_CONFIG_ALTERNATIVE,
                        timeout=30
                    )
                    response.raise_for_status()
                    return response.json()
                    
                except requests.exceptions.RequestException as e2:
                    print(f"备用代理也失败: {e2}")
                    
                    # 最后尝试不使用代理
                    print("尝试不使用代理...")
                    try:
                        response = requests.post(
                            url, 
                            headers=self.headers, 
                            json=payload, 
                            proxies=None,
                            timeout=30
                        )
                        response.raise_for_status()
                        return response.json()
                        
                    except requests.exceptions.RequestException as e3:
                        print(f"无代理请求也失败: {e3}")
                        raise e3
    
    def generate_requirement_model(self, requirement_description: str, 
                                 model: str = DEFAULT_MODEL,
                                 max_tokens: int = MAX_TOKENS,
                                 temperature: float = TEMPERATURE) -> Dict[str, Any]:
        """
        生成需求模型
        
        Args:
            requirement_description: 需求描述
            model: 使用的模型名称
            max_tokens: 最大token数
            temperature: 温度参数
            
        Returns:
            结构化的需求模型
        """
        url = f"{self.base_url}/chat/completions"
        
        # 构建完整的prompt
        full_prompt = f"{REQUIREMENT_MODELING_PROMPT}\n\n用户需求描述：\n{requirement_description}\n\n请生成需求模型："
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "developer",
                    "content": "你是一个专业的需求分析师和软件架构师，擅长将自然语言需求转换为结构化的需求模型。"
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }
        
        try:
            result = self._make_request(url, payload)
            content = result["choices"][0]["message"]["content"]
            
            # 解析JSON响应
            try:
                requirement_model = json.loads(content)
                return requirement_model
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                print(f"原始响应: {content}")
                return {"error": "JSON解析失败", "raw_response": content}
                
        except Exception as e:
            print(f"API请求错误: {e}")
            return {"error": f"API请求失败: {str(e)}"}
    
    def validate_requirement_model(self, model: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证需求模型的完整性
        
        Args:
            model: 需求模型
            
        Returns:
            验证结果
        """
        validation_result = {
            "is_valid": True,
            "missing_fields": [],
            "suggestions": []
        }
        
        required_fields = [
            "project_name", "description", "functional_requirements",
            "non_functional_requirements", "use_cases"
        ]
        
        for field in required_fields:
            if field not in model:
                validation_result["missing_fields"].append(field)
                validation_result["is_valid"] = False
        
        # 检查功能需求
        if "functional_requirements" in model:
            for i, fr in enumerate(model["functional_requirements"]):
                if "id" not in fr or "title" not in fr:
                    validation_result["suggestions"].append(
                        f"功能需求 {i+1} 缺少必要字段 (id, title)"
                    )
        
        # 检查用例
        if "use_cases" in model:
            for i, uc in enumerate(model["use_cases"]):
                if "id" not in uc or "title" not in uc or "actor" not in uc:
                    validation_result["suggestions"].append(
                        f"用例 {i+1} 缺少必要字段 (id, title, actor)"
                    )
        
        return validation_result
    
    def enhance_requirement_model(self, base_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        增强需求模型，添加更多细节
        
        Args:
            base_model: 基础需求模型
            
        Returns:
            增强后的需求模型
        """
        enhancement_prompt = f"""
        请对以下需求模型进行增强，添加更多技术细节和实现考虑：
        
        {json.dumps(base_model, ensure_ascii=False, indent=2)}
        
        请重点关注：
        1. 添加更详细的技术架构设计
        2. 补充数据模型的详细设计
        3. 增加系统接口的详细定义
        4. 添加性能指标和约束条件
        5. 考虑安全性和可扩展性要求
        
        请以JSON格式返回增强后的需求模型。
        """
        
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": DEFAULT_MODEL,
            "messages": [
                {
                    "role": "developer",
                    "content": "你是一个高级软件架构师，擅长技术架构设计和系统优化。"
                },
                {
                    "role": "user",
                    "content": enhancement_prompt
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": 0.5,
            "response_format": {"type": "json_object"}
        }
        
        try:
            result = self._make_request(url, payload)
            content = result["choices"][0]["message"]["content"]
            
            enhanced_model = json.loads(content)
            return enhanced_model
            
        except Exception as e:
            print(f"模型增强失败: {e}")
            return base_model 