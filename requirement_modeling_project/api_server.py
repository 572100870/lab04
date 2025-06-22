"""
FastAPI服务器 - 提供RESTful API接口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uvicorn

from openai_client import OpenAIRequirementModelingClient
from requirement_model import validate_requirement_model, requirement_model_to_json


# 创建FastAPI应用
app = FastAPI(
    title="智能化需求建模API",
    description="基于大语言模型的智能化需求建模系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建客户端实例
client = OpenAIRequirementModelingClient()


class RequirementRequest(BaseModel):
    """需求请求模型"""
    description: str = Field(..., description="需求描述")
    model: Optional[str] = Field("gpt-3.5-turbo", description="使用的模型")
    max_tokens: Optional[int] = Field(4000, description="最大token数")
    temperature: Optional[float] = Field(0.7, description="温度参数")
    enhance: Optional[bool] = Field(False, description="是否增强模型")


class RequirementResponse(BaseModel):
    """需求响应模型"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    validation_result: Optional[Dict[str, Any]] = None


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能化需求建模API服务",
        "version": "1.0.0",
        "endpoints": {
            "/generate": "生成需求模型",
            "/validate": "验证需求模型",
            "/enhance": "增强需求模型"
        }
    }


@app.post("/generate", response_model=RequirementResponse)
async def generate_requirement_model(request: RequirementRequest):
    """生成需求模型"""
    try:
        # 生成基础模型
        result = client.generate_requirement_model(
            requirement_description=request.description,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        if "error" in result:
            return RequirementResponse(
                success=False,
                error=result["error"]
            )
        
        # 验证模型
        validation_result = client.validate_requirement_model(result)
        
        # 如果需要增强
        if request.enhance:
            enhanced_result = client.enhance_requirement_model(result)
            if "error" not in enhanced_result:
                result = enhanced_result
        
        return RequirementResponse(
            success=True,
            data=result,
            validation_result=validation_result
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


@app.post("/validate")
async def validate_model(model_data: Dict[str, Any]):
    """验证需求模型"""
    try:
        validation_result = client.validate_requirement_model(model_data)
        
        # 尝试Pydantic验证
        pydantic_valid = False
        pydantic_error = None
        try:
            validated_model = validate_requirement_model(model_data)
            pydantic_valid = True
        except Exception as e:
            pydantic_error = str(e)
        
        return {
            "success": True,
            "validation_result": validation_result,
            "pydantic_valid": pydantic_valid,
            "pydantic_error": pydantic_error
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"验证失败: {str(e)}")


@app.post("/enhance")
async def enhance_model(model_data: Dict[str, Any]):
    """增强需求模型"""
    try:
        enhanced_result = client.enhance_requirement_model(model_data)
        
        if "error" in enhanced_result:
            return {
                "success": False,
                "error": enhanced_result["error"]
            }
        
        return {
            "success": True,
            "data": enhanced_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"增强失败: {str(e)}")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "requirement-modeling-api"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 