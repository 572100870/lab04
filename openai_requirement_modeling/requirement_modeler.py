"""
需求建模核心类
"""
from typing import Dict, List, Any, Optional
import json
import logging
from openai_client import OpenAIRequirementClient
from config import AGENT_CONFIGS, REQUIREMENT_TEMPLATES, OUTPUT_FORMATS

logger = logging.getLogger(__name__)

class RequirementModeler:
    """需求建模器"""
    
    def __init__(self, client: OpenAIRequirementClient):
        """
        初始化需求建模器
        
        Args:
            client: OpenAI客户端
        """
        self.client = client
        self.requirement_templates = REQUIREMENT_TEMPLATES
        self.output_formats = OUTPUT_FORMATS
        
    def create_requirement_analysis_prompt(self, requirement_text: str) -> List[Dict[str, str]]:
        """
        创建需求分析Prompt
        
        Args:
            requirement_text: 需求文本
            
        Returns:
            消息列表
        """
        system_prompt = """你是一个专业的需求分析师。你的任务是分析用户提供的需求文本，提取关键信息并生成结构化的需求模型。

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

        user_prompt = f"""请分析以下需求文本并生成结构化的需求模型：

{requirement_text}

请确保：
1. 所有ID都是唯一的
2. 需求描述清晰明确
3. 优先级合理分配
4. 验收标准可测试
5. 业务规则逻辑正确"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def create_model_validation_prompt(self, requirement_model: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        创建模型验证Prompt
        
        Args:
            requirement_model: 需求模型
            
        Returns:
            消息列表
        """
        system_prompt = """你是一个需求模型验证专家。你的任务是验证需求模型的完整性、一致性和质量。

请检查以下方面：
1. 需求完整性：是否覆盖了所有必要的需求类型
2. 需求一致性：需求之间是否存在冲突
3. 需求可测试性：验收标准是否可测试
4. 需求可追溯性：需求ID是否唯一且有意义
5. 需求优先级：优先级分配是否合理

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

        user_prompt = f"""请验证以下需求模型：

{json.dumps(requirement_model, ensure_ascii=False, indent=2)}"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def generate_requirement_model(self, requirement_text: str) -> Dict[str, Any]:
        """
        生成需求模型
        
        Args:
            requirement_text: 需求文本
            
        Returns:
            需求模型字典
        """
        try:
            # 第一步：需求分析
            logger.info("开始需求分析...")
            analysis_prompt = self.create_requirement_analysis_prompt(requirement_text)
            analysis_completion = self.client.create_chat_completion(
                analysis_prompt,
                temperature=AGENT_CONFIGS["requirement_analyzer"]["temperature"]
            )
            analysis_response = self.client.get_completion_text(analysis_completion)
            requirement_model = self.client.parse_json_response(analysis_response)
            
            # 第二步：模型验证
            logger.info("开始模型验证...")
            validation_prompt = self.create_model_validation_prompt(requirement_model)
            validation_completion = self.client.create_chat_completion(
                validation_prompt,
                temperature=AGENT_CONFIGS["validator"]["temperature"]
            )
            validation_response = self.client.get_completion_text(validation_completion)
            validation_result = self.client.parse_json_response(validation_response)
            
            # 第三步：如果验证失败，进行改进
            if validation_result["validation_status"] != "通过":
                logger.info("模型需要改进，开始优化...")
                improvement_prompt = self.create_improvement_prompt(requirement_model, validation_result)
                improvement_completion = self.client.create_chat_completion(
                    improvement_prompt,
                    temperature=AGENT_CONFIGS["model_generator"]["temperature"]
                )
                improvement_response = self.client.get_completion_text(improvement_completion)
                requirement_model = self.client.parse_json_response(improvement_response)
            
            return {
                "requirement_model": requirement_model,
                "validation_result": validation_result,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"生成需求模型失败: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    def create_improvement_prompt(self, requirement_model: Dict[str, Any], validation_result: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        创建模型改进Prompt
        
        Args:
            requirement_model: 原始需求模型
            validation_result: 验证结果
            
        Returns:
            消息列表
        """
        system_prompt = """你是一个需求模型优化专家。基于验证结果，你需要改进需求模型以解决发现的问题。

请根据验证结果中的问题和建议，对需求模型进行相应的改进。"""

        user_prompt = f"""原始需求模型：
{json.dumps(requirement_model, ensure_ascii=False, indent=2)}

验证结果：
{json.dumps(validation_result, ensure_ascii=False, indent=2)}

请根据验证结果中的问题和建议，生成改进后的需求模型。"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def export_model(self, requirement_model: Dict[str, Any], format_type: str = "json") -> str:
        """
        导出需求模型
        
        Args:
            requirement_model: 需求模型
            format_type: 导出格式
            
        Returns:
            导出的字符串
        """
        if format_type == "json":
            return json.dumps(requirement_model, ensure_ascii=False, indent=2)
        elif format_type == "yaml":
            import yaml
            return yaml.dump(requirement_model, allow_unicode=True, default_flow_style=False)
        elif format_type == "markdown":
            return self._convert_to_markdown(requirement_model)
        else:
            raise ValueError(f"不支持的导出格式: {format_type}")
    
    def _convert_to_markdown(self, requirement_model: Dict[str, Any]) -> str:
        """
        转换为Markdown格式
        
        Args:
            requirement_model: 需求模型
            
        Returns:
            Markdown字符串
        """
        md_content = f"# {requirement_model.get('project_name', '需求模型')}\n\n"
        
        # 利益相关者
        if "stakeholders" in requirement_model:
            md_content += "## 利益相关者\n\n"
            for stakeholder in requirement_model["stakeholders"]:
                md_content += f"- {stakeholder}\n"
            md_content += "\n"
        
        # 功能需求
        if "functional_requirements" in requirement_model:
            md_content += "## 功能需求\n\n"
            for req in requirement_model["functional_requirements"]:
                md_content += f"### {req['id']}: {req['title']}\n\n"
                md_content += f"**描述**: {req['description']}\n\n"
                md_content += f"**优先级**: {req['priority']}\n\n"
                md_content += "**验收标准**:\n"
                for criterion in req['acceptance_criteria']:
                    md_content += f"- {criterion}\n"
                md_content += "\n"
        
        # 非功能需求
        if "non_functional_requirements" in requirement_model:
            md_content += "## 非功能需求\n\n"
            for req in requirement_model["non_functional_requirements"]:
                md_content += f"### {req['id']}: {req['title']}\n\n"
                md_content += f"**描述**: {req['description']}\n\n"
                md_content += f"**类别**: {req['category']}\n\n"
                md_content += f"**指标**: {req['metrics']}\n\n"
        
        return md_content 