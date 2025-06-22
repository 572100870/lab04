# MultiAgent 自动化领域建模系统 实验报告

## 一、项目简介

本项目旨在构建一个基于多智能体（MultiAgent）协同的自动化领域建模系统，利用OpenAI GPT-4o模型和新版OpenAI SDK，实现从需求分析到用例建模、类图设计、顺序图设计、OCL约束生成、模型验证与迭代的全流程自动化。系统具备极强的健壮性，能够自动修正和兼容Agent输出的JSON格式差异，确保多智能体工作流顺利运行。

---

## 二、输入Prompt示例

用户只需输入自然语言需求描述，例如：

```text
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
```

---

## 三、输出格式定义（DSL）

### 1. 用例图（UseCaseDiagram）

```json
{
  "name": "系统名称",
  "description": "系统描述",
  "actors": [
    {
      "name": "参与者名称",
      "description": "参与者描述",
      "type": "primary"
    }
  ],
  "usecases": [
    {
      "name": "用例名称",
      "description": "用例描述",
      "actor": "主要参与者名称",
      "includes": ["包含的用例名称"],
      "extends": ["扩展的用例名称"]
    }
  ]
}
```

### 2. 概念类图（ConceptualClassDiagram）

```json
{
  "name": "类图名称",
  "description": "类图描述",
  "classes": [
    {
      "name": "类名称",
      "description": "类描述",
      "attributes": [
        {
          "name": "属性名称",
          "type": "属性类型",
          "visibility": "private",
          "multiplicity": "1",
          "description": "属性描述"
        }
      ],
      "methods": [
        {
          "name": "方法名称",
          "parameters": ["参数列表"],
          "return_type": "返回类型",
          "visibility": "public",
          "description": "方法描述"
        }
      ],
      "stereotypes": ["构造型列表"]
    }
  ],
  "relationships": [
    {
      "name": "关系名称",
      "source": "源类名称",
      "target": "目标类名称",
      "type": "association",
      "source_multiplicity": "1",
      "target_multiplicity": "1",
      "description": "关系描述"
    }
  ]
}
```

### 3. 系统顺序图（SystemSequenceDiagram）

```json
{
  "name": "顺序图名称",
  "description": "顺序图描述",
  "actors": ["参与者列表"],
  "systems": ["系统列表"],
  "messages": [
    {
      "name": "消息名称",
      "sender": "发送方",
      "receiver": "接收方",
      "message_type": "synchronous",
      "parameters": ["参数列表"],
      "return_value": "返回值"
    }
  ]
}
```

### 4. OCL约束（OCLConstraint）

```json
[
  {
    "name": "约束名称",
    "context": "约束上下文",
    "type": "inv",
    "expression": "OCL表达式",
    "description": "约束描述"
  }
]
```

### 5. 验证结果（ValidationResult）

```json
{
  "score": "pass",
  "feedback": "验证反馈信息",
  "details": {
    "usecase_score": "用例图评分",
    "class_score": "类图评分",
    "sequence_score": "顺序图评分",
    "ocl_score": "OCL约束评分",
    "overall_score": "整体评分"
  }
}
```

---

## 四、MultiAgent Workflow 简要说明

### 1. 工作流结构

- **需求分析Agent**：分析用户输入的需求文本，提取关键业务要素。
- **用例建模Agent**：根据分析结果，生成标准用例图JSON。
- **类图设计Agent**：根据用例图，生成概念类图JSON。
- **顺序图设计Agent**：为每个用例生成系统顺序图JSON。
- **OCL专家Agent**：根据用例图和类图生成OCL约束。
- **验证专家Agent**：对整体模型进行一致性、完整性、正确性验证，输出评分和改进建议。
- **协调者Agent**：负责多Agent之间的流程协调和模型迭代。

### 2. 自动化与健壮性

- **自动JSON提取与修正**：系统会自动从Agent输出中提取JSON，并修正字段名、结构、大小写等差异，确保Pydantic模型校验通过。
- **串行自动执行**：所有步骤自动串行执行，无需人工干预。
- **错误调试信息**：每一步均有详细的调试输出，便于定位和修复问题。

### 3. 运行方式

在命令行中运行：

```shell
cd D:\conda\ruanjian\multiagent_workflow_project
python example_usage.py
```

---

## 五、生成的需求模型说明（以在线书店为例）

### 1. 用例图（部分）

```json
{
  "name": "在线书店系统",
  "description": "一个用于用户注册、浏览、购买图书以及进行订单管理和图书评价的在线书店系统。",
  "actors": [
    {"name": "顾客", "description": "...", "type": "primary"},
    {"name": "管理员", "description": "...", "type": "primary"},
    {"name": "支付系统", "description": "...", "type": "primary"}
  ],
  "usecases": [
    {
      "name": "用户注册和登录",
      "description": "用户创建账户并登录系统以访问更多服务。",
      "actor": "顾客",
      "includes": [],
      "extends": []
    },
    ...
  ]
}
```

### 2. 概念类图（部分）

```json
{
  "name": "在线书店系统类图",
  "description": "该类图展示了在线书店系统中的概念类以及类之间的关系。",
  "classes": [
    {
      "name": "用户",
      "description": "表示注册和登录到系统的用户。",
      "attributes": [
        {"name": "用户名", "type": "String", ...}
      ],
      "methods": [
        {"name": "注册", "parameters": ["用户名", "密码", "电子邮件"], ...}
      ],
      "stereotypes": []
    },
    ...
  ],
  "relationships": [
    {
      "name": "用户-顾客继承关系",
      "source": "顾客",
      "target": "用户",
      "type": "generalization",
      ...
    }
  ]
}
```

### 3. 顺序图、OCL约束、验证结果

- 顺序图和OCL约束均为标准JSON结构，内容详见output文件夹。
- 验证结果会输出模型评分和改进建议，便于后续迭代。

---

## 六、结论与亮点

- **全流程自动化**：用户只需输入需求，系统自动完成全部领域建模任务。
- **极强健壮性**：自动修正Agent输出，兼容各种JSON格式差异。
- **可扩展性强**：支持自定义Agent、插入人工环节、扩展输出格式。
- **结果可视化**：自动导出PlantUML用例图，便于后续文档和设计交流。

---

如需进一步定制或遇到特殊格式问题，欢迎随时反馈！ 