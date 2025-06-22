"""
OpenAI API 客户端封装
"""
from openai import OpenAI
from openai.types.chat import ChatCompletion
from typing import List, Dict, Any, Optional
import json
import logging
from config import BASE_URL, API_KEY, DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIRequirementClient:
    """OpenAI需求建模客户端"""
    
    def __init__(self, base_url: str = BASE_URL, api_key: str = API_KEY):
        """
        初始化OpenAI客户端
        
        Args:
            base_url: API基础URL
            api_key: API密钥
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = DEFAULT_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        
    def create_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> ChatCompletion:
        """
        创建聊天完成请求
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            ChatCompletion对象
        """
        try:
            completion = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            logger.info(f"成功调用OpenAI API，模型: {model or self.model}")
            return completion
        except Exception as e:
            logger.error(f"调用OpenAI API失败: {str(e)}")
            raise
    
    def get_completion_text(self, completion: ChatCompletion) -> str:
        """
        从完成对象中提取文本内容
        
        Args:
            completion: ChatCompletion对象
            
        Returns:
            文本内容
        """
        return completion.choices[0].message.content
    
    def parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        解析JSON格式的响应
        
        Args:
            text: 响应文本
            
        Returns:
            解析后的字典
        """
        try:
            # 尝试直接解析JSON
            return json.loads(text)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("无法解析JSON响应")
    
    def test_connection(self) -> bool:
        """
        测试API连接
        
        Returns:
            连接是否成功
        """
        try:
            messages = [
                {"role": "system", "content": "你是一个有用的助手。"},
                {"role": "user", "content": "请回复'连接成功'"}
            ]
            completion = self.create_chat_completion(messages)
            response = self.get_completion_text(completion)
            logger.info(f"API连接测试成功: {response}")
            return True
        except Exception as e:
            logger.error(f"API连接测试失败: {str(e)}")
            return False 