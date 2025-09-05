from typing import Any, Dict
from app.core.base_algorithm import BaseAlgorithm
from app.core.registry import algorithm_register
from app.models.algorithm import AlgorithmMetadata

@algorithm_register(
    name="hello_world",
    display_name="Hello World (1+1)",
    category="basic",
    description="最简单的算法示例：计算1+1并展示步骤",
    complexity_time="O(1)",
    complexity_space="O(1)"
)
class HelloWorldAlgorithm(BaseAlgorithm):
    """Hello World算法：展示1+1的计算过程"""
    
    def get_metadata(self) -> AlgorithmMetadata:
        """返回算法元数据"""
        return AlgorithmMetadata(
            name="hello_world",
            display_name="Hello World (1+1)",
            category="basic",
            description="最简单的算法示例：计算1+1并展示步骤",
            complexity_time="O(1)",
            complexity_space="O(1)"
        )
    
    def get_config_schema(self) -> Dict[str, Any]:
        """配置模式"""
        return {
            "num1": {
                "type": "number",
                "description": "第一个数字",
                "default": 1,
                "min": 0,
                "max": 100
            },
            "num2": {
                "type": "number", 
                "description": "第二个数字",
                "default": 1,
                "min": 0,
                "max": 100
            },
            "show_steps": {
                "type": "boolean",
                "description": "是否显示详细步骤",
                "default": True
            }
        }
    
    def execute(self, data: Dict[str, Any], config: Dict[str, Any]) -> Any:
        """执行算法"""
        # 从配置中获取参数，如果没有则使用默认值
        num1 = config.get("num1", data.get("num1", 1))
        num2 = config.get("num2", data.get("num2", 1))
        show_steps = config.get("show_steps", True)
        
        if show_steps:
            # 步骤1: 显示初始数值
            self.add_step(
                action="initialize",
                data_snapshot={"num1": num1, "num2": num2, "result": None},
                highlight=[0, 1],
                description=f"初始化两个数字: {num1} 和 {num2}"
            )
            
            # 步骤2: 开始计算
            self.add_step(
                action="calculate",
                data_snapshot={"num1": num1, "num2": num2, "result": None, "operation": "+"},
                highlight=[0, 1],
                description=f"开始计算: {num1} + {num2}"
            )
            
            # 步骤3: 计算结果
            result = num1 + num2
            self.add_step(
                action="result",
                data_snapshot={"num1": num1, "num2": num2, "result": result},
                highlight=[2],
                description=f"计算完成: {num1} + {num2} = {result}"
            )
        else:
            # 直接计算
            result = num1 + num2
            self.add_step(
                action="direct_result",
                data_snapshot={"num1": num1, "num2": num2, "result": result},
                highlight=[],
                description=f"直接计算结果: {result}"
            )
        
        return {
            "num1": num1,
            "num2": num2,
            "result": result,
            "operation": "addition"
        }