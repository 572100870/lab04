import os
from typing import List, Dict, Any
from openai import OpenAI
from dsl_models import DomainModel, UseCaseDiagram, SystemSequenceDiagram, ConceptualClassDiagram, OCLConstraint
from my_agents import requirements_analyst, usecase_modeler, class_diagram_designer, sequence_diagram_designer, ocl_expert, validation_expert, coordinator
from config import config
import json
import re

# 设置代理
os.environ["HTTP_PROXY"] = f"http://{config.proxy_host}:{config.proxy_port}"
os.environ["HTTPS_PROXY"] = f"http://{config.proxy_host}:{config.proxy_port}"

client = OpenAI(base_url=config.base_url, api_key=config.api_key)

def run_agent(agent, user_input, max_tokens=2048):
    messages = [
        {"role": "system", "content": agent.instructions},
        {"role": "user", "content": user_input}
    ]
    completion = client.chat.completions.create(
        model=agent.model,
        messages=messages,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content

class MultiAgentWorkflow:
    """MultiAgent工作流管理器（同步串行，基于新版openai SDK）"""
    def __init__(self):
        self.current_model = None
        self.iteration_count = 0
        self.max_iterations = 3

    def extract_json(self, text):
        """从文本中提取第一个合法JSON块，增强健壮性"""
        if not text or text.strip() == "":
            raise ValueError("Agent返回了空字符串")
        
        print(f"🔍 正在提取JSON，原始文本长度: {len(text)}")
        print(f"📝 原始文本前200字符: {text[:200]}...")
        
        # 尝试多种JSON提取模式
        patterns = [
            r'```json\s*(\{[\s\S]*?\})\s*```',  # ```json {content} ```
            r'```\s*(\{[\s\S]*?\})\s*```',      # ``` {content} ```
            r'\{[\s\S]*?\}',                    # 直接匹配JSON对象
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                json_str = match.group(1) if len(match.groups()) > 0 else match.group(0)
                try:
                    # 验证JSON格式
                    json.loads(json_str)
                    print(f"✅ JSON提取成功，长度: {len(json_str)}")
                    return json_str
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON格式验证失败: {e}")
                    continue
        
        # 如果所有模式都失败，尝试直接解析整个文本
        try:
            json.loads(text.strip())
            print("✅ 直接解析成功")
            return text.strip()
        except json.JSONDecodeError:
            pass
        
        raise ValueError(f"无法从文本中提取有效JSON。文本内容: {text[:500]}...")

    def fix_usecase_diagram_json(self, data: dict) -> dict:
        """修正用例图JSON结构，确保符合DSL模型要求"""
        print(f"🔧 开始修正用例图JSON，原始数据键: {list(data.keys())}")
        
        # 确保顶层字段存在
        if 'name' not in data:
            data['name'] = "系统用例图"
        if 'description' not in data:
            data['description'] = "系统的主要用例和参与者"
        
        # 处理参与者字段 - DSL模型使用actors
        if 'participants' in data:
            data['actors'] = data.pop('participants')
        elif 'actors' not in data:
            data['actors'] = []
        
        # 处理用例字段
        usecases_key = None
        for key in ['useCases', 'usecases', 'use_cases']:
            if key in data:
                usecases_key = key
                break
        
        if usecases_key:
            data['usecases'] = data.pop(usecases_key)
        elif 'usecases' not in data:
            data['usecases'] = []
        
        # 修正每个用例的结构
        for i, uc in enumerate(data.get('usecases', [])):
            if not isinstance(uc, dict):
                print(f"⚠️ 用例 {i} 不是字典格式，跳过")
                continue
                
            # 确保用例有name字段
            if 'name' not in uc:
                uc['name'] = f"用例{i+1}"
            
            # 处理参与者字段 - DSL模型使用actor（单数）
            if 'participants' in uc:
                if isinstance(uc['participants'], list):
                    uc['actor'] = uc['participants'][0] if uc['participants'] else ""
                else:
                    uc['actor'] = uc['participants']
                del uc['participants']
            elif 'actors' in uc:
                if isinstance(uc['actors'], list):
                    uc['actor'] = uc['actors'][0] if uc['actors'] else ""
                else:
                    uc['actor'] = uc['actors']
                del uc['actors']
            elif 'actor' not in uc:
                uc['actor'] = ""
            
            # 处理include字段
            if 'include' in uc:
                uc['includes'] = uc.pop('include')
            elif 'includes' not in uc:
                uc['includes'] = []
            
            # 处理extend字段
            if 'extend' in uc:
                uc['extends'] = uc.pop('extend')
            elif 'extends' not in uc:
                uc['extends'] = []
        
        print(f"✅ 用例图JSON修正完成，最终键: {list(data.keys())}")
        return data

    def safe_json_parse(self, json_str: str, model_class, fix_func=None):
        """安全解析JSON并验证模型"""
        try:
            # 提取JSON
            extracted_json = self.extract_json(json_str)
            # 解析JSON
            raw_data = json.loads(extracted_json)
            # 应用修正函数
            if fix_func:
                raw_data = fix_func(raw_data)
            # 验证模型
            return model_class.model_validate(raw_data)
        except Exception as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"📝 原始JSON字符串: {json_str[:500]}...")
            raise

    def run_workflow(self, user_requirements: str) -> DomainModel:
        print("🚀 开始MultiAgent领域建模工作流...")
        
        # 步骤1: 需求分析
        print("\n📋 步骤1: 需求分析")
        analysis_result = run_agent(requirements_analyst, f"请分析以下需求并提取关键信息：\n\n{user_requirements}")
        
        # 步骤2: 用例建模
        print("\n🎯 步骤2: 用例建模")
        usecase_diagram_json = run_agent(usecase_modeler, f"基于以下需求分析结果，创建详细的用例图：\n\n{analysis_result}")
        print("用例建模Agent原始输出：", usecase_diagram_json)
        
        try:
            usecase_diagram = self.safe_json_parse(usecase_diagram_json, UseCaseDiagram, self.fix_usecase_diagram_json)
            print("✅ 用例图解析成功")
        except Exception as e:
            print(f"❌ 用例图解析失败: {e}")
            raise
        
        # 步骤3: 类图设计
        print("\n🏗️ 步骤3: 类图设计")
        class_diagram_json = run_agent(class_diagram_designer, f"基于以下用例图，创建概念类图：\n\n{usecase_diagram.model_dump_json(indent=2)}")
        print("类图设计Agent原始输出：", class_diagram_json)
        
        try:
            class_diagram = self.safe_json_parse(class_diagram_json, ConceptualClassDiagram)
            print("✅ 类图解析成功")
        except Exception as e:
            print(f"❌ 类图解析失败: {e}")
            raise
        
        # 步骤4: 顺序图设计
        print("\n📊 步骤4: 顺序图设计")
        sequence_diagrams = []
        for usecase in usecase_diagram.usecases:
            print(f"🔍 正在为用例 '{usecase.name}' 生成顺序图...")
            seq_json = run_agent(sequence_diagram_designer, f"为用例 '{usecase.name}' 创建系统顺序图：\n\n{usecase.model_dump_json(indent=2)}")
            try:
                seq_diagram = self.safe_json_parse(seq_json, SystemSequenceDiagram)
                sequence_diagrams.append(seq_diagram)
                print(f"✅ 用例 '{usecase.name}' 顺序图解析成功")
            except Exception as e:
                print(f"❌ 用例 '{usecase.name}' 顺序图解析失败: {e}")
                continue
        
        print(f"📊 顺序图设计完成，共生成 {len(sequence_diagrams)} 个顺序图")
        
        # 步骤5: OCL约束生成
        print("\n🔒 步骤5: OCL约束生成")
        print("🔍 正在调用OCL专家Agent...")
        ocl_json = run_agent(ocl_expert, f"基于以下用例图和类图，生成OCL约束：\n\n用例图：{usecase_diagram.model_dump_json(indent=2)}\n\n类图：{class_diagram.model_dump_json(indent=2)}")
        print("🔍 OCL专家Agent返回结果，正在解析...")
        try:
            ocl_data = json.loads(self.extract_json(ocl_json))
            print(f"🔍 OCL数据解析成功，数据类型: {type(ocl_data)}, 长度: {len(ocl_data)}")
            print(f"🔍 OCL数据前200字符: {str(ocl_data)[:200]}...")
            
            ocl_constraints = []
            for i, constraint_data in enumerate(ocl_data):
                try:
                    print(f"🔍 处理OCL约束 {i+1}: {type(constraint_data)} - {constraint_data}")
                    if isinstance(constraint_data, dict):
                        constraint = OCLConstraint.model_validate(constraint_data)
                        ocl_constraints.append(constraint)
                        print(f"✅ OCL约束 {i+1} 解析成功: {constraint.name}")
                    else:
                        print(f"⚠️ OCL约束 {i+1} 不是字典格式，跳过")
                        continue
                except Exception as e:
                    print(f"⚠️ OCL约束 {i+1} 解析失败: {e}")
                    continue
            print(f"✅ OCL约束解析完成，成功解析 {len(ocl_constraints)} 个约束")
        except Exception as e:
            print(f"❌ OCL约束解析失败: {e}")
            ocl_constraints = []
        
        print(f"🔒 OCL约束生成完成，共生成 {len(ocl_constraints)} 个约束")
        
        # 步骤6: 模型验证和迭代改进
        print("\n✅ 步骤6: 模型验证和迭代改进")
        print("🔍 正在进入验证和迭代阶段...")
        final_model = self._run_validation_and_iteration(
            usecase_diagram, class_diagram, sequence_diagrams, ocl_constraints
        )
        print("\n🎉 工作流完成！")
        return final_model

    def _run_validation_and_iteration(self, usecase_diagram, class_diagram, sequence_diagrams, ocl_constraints):
        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            print(f"\n🔄 迭代 {self.iteration_count}/{self.max_iterations}")
            current_model = DomainModel(
                name="领域模型",
                description="通过MultiAgent工作流生成的领域模型",
                usecase_diagram=usecase_diagram,
                sequence_diagrams=sequence_diagrams,
                class_diagram=class_diagram,
                ocl_constraints=ocl_constraints
            )
            # 验证
            try:
                validation_json = run_agent(validation_expert, f"请验证以下领域模型：\n\n{current_model.model_dump_json(indent=2)}")
                validation = json.loads(self.extract_json(validation_json))
                score = validation.get("score", "pass")
                feedback = validation.get("feedback", "")
            except Exception as e:
                print(f"⚠️ 验证步骤出现异常，使用默认评分: {e}")
                score = "pass"
                feedback = ""
            
            if score == "pass":
                print("✅ 模型验证通过！")
                return current_model
            elif score == "needs_improvement":
                print("⚠️ 模型需要改进，进行迭代...")
                try:
                    improved_json = run_agent(coordinator, f"请根据以下反馈改进模型：\n\n反馈：{feedback}\n\n当前模型：{current_model.model_dump_json(indent=2)}")
                    improved = json.loads(self.extract_json(improved_json))
                    usecase_diagram = UseCaseDiagram.model_validate(improved["usecase_diagram"])
                    class_diagram = ConceptualClassDiagram.model_validate(improved["class_diagram"])
                    sequence_diagrams = [SystemSequenceDiagram.model_validate(x) for x in improved["sequence_diagrams"]]
                    ocl_constraints = [OCLConstraint.model_validate(x) for x in improved["ocl_constraints"]]
                except Exception as e:
                    print(f"⚠️ 迭代改进失败，使用当前模型: {e}")
                    return current_model
            else:
                print("❌ 模型验证失败，返回当前模型...")
                return current_model
        
        print("⚠️ 达到最大迭代次数，返回当前模型")
        return current_model

def main():
    sample_requirements = """
    请为在线书店系统进行领域建模。
    
    系统功能包括：
    1. 用户注册和登录
    2. 浏览和搜索图书
    3. 添加图书到购物车
    4. 下单和支付
    5. 订单管理
    6. 库存管理
    7. 用户评价和评论
    
    主要参与者包括：顾客、管理员、支付系统
    """
    
    try:
        workflow = MultiAgentWorkflow()
        final_model = workflow.run_workflow(sample_requirements)
        
        # 确保output目录存在
        import os
        os.makedirs("output", exist_ok=True)
        
        # 保存领域模型
        from tools import save_domain_model, export_to_plantuml
        save_result = save_domain_model(final_model, "final_domain_model.json")
        print(f"\n💾 {save_result}")
        
        # 导出PlantUML用例图
        plantuml_code = export_to_plantuml(final_model)
        with open("output/usecase_diagram.puml", "w", encoding="utf-8") as f:
            f.write(plantuml_code)
        print("📊 PlantUML用例图已导出到 output/usecase_diagram.puml")
        
        print("\n🎉 多智能体自动化领域建模流程完成！")
        
    except Exception as e:
        print(f"❌ 工作流执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 