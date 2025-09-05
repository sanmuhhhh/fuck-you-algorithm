from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.registry import algorithm_registry
from app.models.algorithm import (
    AlgorithmListResponse, 
    AlgorithmExecuteRequest, 
    AlgorithmResult,
    AlgorithmConfig
)

router = APIRouter()

@router.get("/algorithms", response_model=AlgorithmListResponse)
async def list_algorithms():
    """获取所有可用算法列表"""
    try:
        algorithms = algorithm_registry.list_algorithms()
        return AlgorithmListResponse(
            algorithms=algorithms,
            total=len(algorithms)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/algorithms/{algorithm_name}/config", response_model=AlgorithmConfig)
async def get_algorithm_config(algorithm_name: str):
    """获取指定算法的配置模式"""
    try:
        algorithm = algorithm_registry.get_algorithm_instance(algorithm_name)
        return AlgorithmConfig(
            name=algorithm_name,
            config_schema=algorithm.get_config_schema()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/algorithms/{algorithm_name}/execute", response_model=AlgorithmResult)
async def execute_algorithm(algorithm_name: str, request: AlgorithmExecuteRequest):
    """执行指定算法"""
    try:
        algorithm = algorithm_registry.get_algorithm_instance(algorithm_name)
        algorithm.reset_steps()
        
        # 执行算法
        final_result = algorithm.execute(request.data, request.config)
        
        # 返回结果
        return algorithm.create_result(final_result)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Algorithm execution failed: {str(e)}")

@router.get("/algorithms/{algorithm_name}/metadata")
async def get_algorithm_metadata(algorithm_name: str):
    """获取算法元数据"""
    try:
        algorithm = algorithm_registry.get_algorithm_instance(algorithm_name)
        return algorithm.get_metadata()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))