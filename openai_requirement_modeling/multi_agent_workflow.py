"""
多智能体工作流 - 基于大语言模型的自动化需求建模
"""
from typing import Dict, List, Any, Optional
import json
import logging
from dataclasses import dataclass
from enum import Enum
from openai_client import OpenAIRequirementClient
from requirement_modeler import RequirementModeler
from config import AGENT_CONFIGS

logger = logging.getLogger(__name__)

class AgentRole(Enum):
    """智能体角色枚举"""
    REQUIREMENT_ANALYZER = "requirement_analyzer"
    MODEL_GENERATOR = "model_generator"
    VALIDATOR = "validator"
    COORDINATOR = "coordinator"

@dataclass
class AgentMessage:
    """智能体消息"""
    from_agent: str
    to_agent: str
    content: Any
    message_type: str
    timestamp: float

class Agent:
    """基础智能体类"""
    
    def __init__(self, name: str, role: AgentRole, client: OpenAIRequirementClient):
        """
        初始化智能体
        
        Args:
            name: 智能体名称
            role: 智能体角色
            client: OpenAI客户端
        """
        self.name = name
        self.role = role
        self.client = client
        self.config = AGENT_CONFIGS.get(role.value, {})
        self.conversation_history = []
        
    def process_message(self, message: AgentMessage) -> AgentMessage:
        """
        处理消息
        
        Args:
            message: 输入消息
            
        Returns:
            响应消息
        """
        raise NotImplementedError("子类必须实现process_message方法")
    
    def add_to_history(self, message: AgentMessage):
        """添加到对话历史"""
        self.conversation_history.append(message)

class RequirementAnalyzerAgent(Agent):
    """需求分析智能体"""
    
    def __init__(self, client: OpenAIRequirementClient):
        super().__init__("需求分析智能体", AgentRole.REQUIREMENT_ANALYZER, client)
    
    def process_message(self, message: AgentMessage) -> AgentMessage:
        """处理需求分析消息"""
        if message.message_type == "analyze_requirement":
            requirement_text = message.content
            
            # 创建分析Prompt
            system_prompt = """你是一个专业的需求分析师。你的任务是分析用户提供的需求文本，提取关键信息并识别需求类型。

请输出JSON格式的分析结果：
{
    "identified_requirements": [
        {
            "type": "功能需求/非功能需求/用户故事/用例/业务规则",
            "description": "需求描述",
            "priority": "高/中/低",
            "stakeholders": ["相关利益者"],
            "constraints": ["约束条件"]
        }
    ],
    "missing_information": ["缺失的信息"],
    "ambiguities": ["模糊不清的地方"],
    "recommendations": ["建议"]
}"""

            user_prompt = f"请分析以下需求文本：\n\n{requirement_text}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            completion = self.client.create_chat_completion(
                messages,
                temperature=self.config.get("temperature", 0.3)
            )
            
            analysis_result = self.client.parse_json_response(
                self.client.get_completion_text(completion)
            )
            
            return AgentMessage(
                from_agent=self.name,
                to_agent=message.from_agent,
                content=analysis_result,
                message_type="analysis_result",
                timestamp=message.timestamp
            )
        
        return None

class ModelGeneratorAgent(Agent):
    """模型生成智能体"""
    
    def __init__(self, client: OpenAIRequirementClient):
        super().__init__("模型生成智能体", AgentRole.MODEL_GENERATOR, client)
    
    def process_message(self, message: AgentMessage) -> AgentMessage:
        """处理模型生成消息"""
        if message.message_type == "generate_model":
            analysis_result = message.content
            
            # 创建模型生成Prompt
            system_prompt = """你是一个需求模型生成专家。基于需求分析结果，你需要生成结构化的需求模型。

请按照以下格式输出JSON：
{
    "project_name": "项目名称",
    "stakeholders": ["利益相关者列表"],
    "functional_requirements": [
        {
            "id": "FR001",
            "title": "功能需求标题",
            "description": "详细描述",
            "priority": "高/中/低",
            "acceptance_criteria": ["验收标准列表"]
        }
    ],
    "non_functional_requirements": [
        {
            "id": "NFR001", 
            "title": "非功能需求标题",
            "description": "详细描述",
            "category": "性能/安全/可用性/可维护性",
            "metrics": "具体指标"
        }
    ],
    "user_stories": [
        {
            "id": "US001",
            "as_a": "作为...",
            "i_want": "我想要...",
            "so_that": "以便...",
            "acceptance_criteria": ["验收标准"]
        }
    ],
    "use_cases": [
        {
            "id": "UC001",
            "title": "用例标题",
            "actor": "参与者",
            "preconditions": ["前置条件"],
            "main_flow": ["主要流程步骤"],
            "postconditions": ["后置条件"]
        }
    ],
    "business_rules": [
        {
            "id": "BR001",
            "title": "业务规则标题",
            "description": "规则描述",
            "constraints": ["约束条件"]
        }
    ]
}"""

            user_prompt = f"基于以下需求分析结果生成需求模型：\n\n{json.dumps(analysis_result, ensure_ascii=False, indent=2)}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            completion = self.client.create_chat_completion(
                messages,
                temperature=self.config.get("temperature", 0.5)
            )
            
            model_result = self.client.parse_json_response(
                self.client.get_completion_text(completion)
            )
            
            return AgentMessage(
                from_agent=self.name,
                to_agent=message.from_agent,
                content=model_result,
                message_type="model_result",
                timestamp=message.timestamp
            )
        
        return None

class ValidatorAgent(Agent):
    """验证智能体"""
    
    def __init__(self, client: OpenAIRequirementClient):
        super().__init__("验证智能体", AgentRole.VALIDATOR, client)
    
    def process_message(self, message: AgentMessage) -> AgentMessage:
        """处理验证消息"""
        if message.message_type == "validate_model":
            requirement_model = message.content
            
            # 创建验证Prompt
            system_prompt = """你是一个需求模型验证专家。你的任务是验证需求模型的完整性、一致性和质量。

请输出验证结果JSON：
{
    "validation_status": "通过/需要改进/失败",
    "issues": [
        {
            "type": "完整性/一致性/可测试性/可追溯性/优先级",
            "severity": "高/中/低",
            "description": "问题描述",
            "suggestion": "改进建议"
        }
    ],
    "overall_score": 0-100,
    "recommendations": ["改进建议列表"]
}"""

            user_prompt = f"请验证以下需求模型：\n\n{json.dumps(requirement_model, ensure_ascii=False, indent=2)}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            completion = self.client.create_chat_completion(
                messages,
                temperature=self.config.get("temperature", 0.2)
            )
            
            validation_result = self.client.parse_json_response(
                self.client.get_completion_text(completion)
            )
            
            return AgentMessage(
                from_agent=self.name,
                to_agent=message.from_agent,
                content=validation_result,
                message_type="validation_result",
                timestamp=message.timestamp
            )
        
        return None

class MultiAgentWorkflow:
    """多智能体工作流"""
    
    def __init__(self, client: OpenAIRequirementClient):
        """
        初始化多智能体工作流
        
        Args:
            client: OpenAI客户端
        """
        self.client = client
        self.agents = {
            AgentRole.REQUIREMENT_ANALYZER: RequirementAnalyzerAgent(client),
            AgentRole.MODEL_GENERATOR: ModelGeneratorAgent(client),
            AgentRole.VALIDATOR: ValidatorAgent(client)
        }
        self.workflow_history = []
        
    def execute_workflow(self, requirement_text: str, max_iterations: int = 3) -> Dict[str, Any]:
        """
        执行多智能体工作流
        
        Args:
            requirement_text: 需求文本
            max_iterations: 最大迭代次数
            
        Returns:
            工作流执行结果
        """
        logger.info("开始执行多智能体工作流...")
        
        # 第一步：需求分析
        logger.info("步骤1: 需求分析")
        analysis_message = AgentMessage(
            from_agent="coordinator",
            to_agent="requirement_analyzer",
            content=requirement_text,
            message_type="analyze_requirement",
            timestamp=0.0
        )
        
        analysis_result = self.agents[AgentRole.REQUIREMENT_ANALYZER].process_message(analysis_message)
        self.workflow_history.append(analysis_result)
        
        # 第二步：模型生成
        logger.info("步骤2: 模型生成")
        model_message = AgentMessage(
            from_agent="coordinator",
            to_agent="model_generator",
            content=analysis_result.content,
            message_type="generate_model",
            timestamp=1.0
        )
        
        model_result = self.agents[AgentRole.MODEL_GENERATOR].process_message(model_message)
        self.workflow_history.append(model_result)
        
        # 第三步：模型验证和改进
        iteration = 0
        while iteration < max_iterations:
            logger.info(f"步骤3.{iteration + 1}: 模型验证 (迭代 {iteration + 1})")
            
            validation_message = AgentMessage(
                from_agent="coordinator",
                to_agent="validator",
                content=model_result.content,
                message_type="validate_model",
                timestamp=2.0 + iteration
            )
            
            validation_result = self.agents[AgentRole.VALIDATOR].process_message(validation_message)
            self.workflow_history.append(validation_result)
            
            # 检查验证结果
            if validation_result.content["validation_status"] == "通过":
                logger.info("模型验证通过，工作流完成")
                break
            
            # 如果验证失败，进行改进
            logger.info("模型需要改进，重新生成...")
            improvement_message = AgentMessage(
                from_agent="coordinator",
                to_agent="model_generator",
                content={
                    "original_model": model_result.content,
                    "validation_result": validation_result.content
                },
                message_type="improve_model",
                timestamp=3.0 + iteration
            )
            
            model_result = self.agents[AgentRole.MODEL_GENERATOR].process_message(improvement_message)
            self.workflow_history.append(model_result)
            
            iteration += 1
        
        # 返回最终结果
        return {
            "requirement_model": model_result.content,
            "validation_result": validation_result.content,
            "workflow_history": self.workflow_history,
            "iterations": iteration + 1,
            "status": "success" if validation_result.content["validation_status"] == "通过" else "partial_success"
        }
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """获取工作流摘要"""
        return {
            "total_messages": len(self.workflow_history),
            "agents_involved": list(self.agents.keys()),
            "workflow_status": "completed"
        } 