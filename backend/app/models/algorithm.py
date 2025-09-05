from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AlgorithmStep(BaseModel):
    """算法执行步骤"""
    step_id: int
    action: str
    data_snapshot: Dict[str, Any]
    highlight: List[int] = Field(default_factory=list)
    description: str
    timestamp: float

class AlgorithmMetadata(BaseModel):
    """算法元数据"""
    name: str
    display_name: str
    category: str
    description: str
    complexity_time: Optional[str] = None
    complexity_space: Optional[str] = None
    author: Optional[str] = None

class AlgorithmConfig(BaseModel):
    """算法配置"""
    name: str
    config_schema: Dict[str, Any]

class AlgorithmResult(BaseModel):
    """算法执行结果"""
    algorithm_name: str
    steps: List[AlgorithmStep]
    final_result: Any
    performance_metrics: Dict[str, Any]
    execution_time: float
    created_at: datetime

class AlgorithmExecuteRequest(BaseModel):
    """算法执行请求"""
    data: Dict[str, Any]
    config: Dict[str, Any] = Field(default_factory=dict)

class AlgorithmListResponse(BaseModel):
    """算法列表响应"""
    algorithms: List[AlgorithmMetadata]
    total: int