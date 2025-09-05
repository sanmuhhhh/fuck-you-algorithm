from abc import ABC, abstractmethod
from typing import Any, Dict, List
import time
from datetime import datetime
from app.models.algorithm import AlgorithmStep, AlgorithmResult, AlgorithmMetadata

class BaseAlgorithm(ABC):
    """算法基类，所有算法实现都需要继承此类"""
    
    def __init__(self):
        self.steps: List[AlgorithmStep] = []
        self.step_counter = 0
        self.start_time = 0.0
        
    @abstractmethod
    def get_metadata(self) -> AlgorithmMetadata:
        """返回算法元数据"""
        pass
    
    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """返回算法配置模式"""
        pass
    
    @abstractmethod
    def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Any:
        """执行算法主逻辑，返回最终结果"""
        pass
    
    def reset_steps(self):
        """重置步骤记录"""
        self.steps = []
        self.step_counter = 0
        self.start_time = time.time()
        
    def add_step(self, action: str, data_snapshot: Dict[str, Any], 
                 highlight: List[int] = None, description: str = ""):
        """添加算法执行步骤"""
        if highlight is None:
            highlight = []
            
        step = AlgorithmStep(
            step_id=self.step_counter,
            action=action,
            data_snapshot=data_snapshot,
            highlight=highlight,
            description=description,
            timestamp=time.time() - self.start_time
        )
        self.steps.append(step)
        self.step_counter += 1
        
    def create_result(self, final_result: Any) -> AlgorithmResult:
        """创建算法执行结果"""
        execution_time = time.time() - self.start_time
        
        return AlgorithmResult(
            algorithm_name=self.get_metadata().name,
            steps=self.steps,
            final_result=final_result,
            performance_metrics={
                "execution_time": execution_time,
                "step_count": len(self.steps),
                "memory_usage": "N/A"  # 可以后续扩展
            },
            execution_time=execution_time,
            created_at=datetime.now()
        )