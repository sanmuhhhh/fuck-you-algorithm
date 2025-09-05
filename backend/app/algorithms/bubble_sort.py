"""
冒泡排序算法实现
具有详细的步骤记录和可视化数据
"""
import time
from typing import List, Dict, Any
from app.core.base_algorithm import BaseAlgorithm
from app.core.registry import algorithm_register


@algorithm_register(
    name="bubble_sort",
    display_name="冒泡排序",
    category="排序算法", 
    description="通过重复遍历列表，比较相邻元素并交换它们来排序数组的简单排序算法",
    complexity_time="O(n²)",
    complexity_space="O(1)"
)
class BubbleSortAlgorithm(BaseAlgorithm):
    """冒泡排序算法类"""
    
    def get_metadata(self):
        """获取算法元数据"""
        from app.models.algorithm import AlgorithmMetadata
        return AlgorithmMetadata(
            name="bubble_sort",
            display_name="冒泡排序",
            category="排序算法",
            description="通过重复遍历列表，比较相邻元素并交换它们来排序数组的简单排序算法",
            complexity_time="O(n²)",
            complexity_space="O(1)",
            author="Claude"
        )
    
    def get_config_schema(self) -> Dict[str, Any]:
        """获取算法配置模式"""
        return {
            "type": "object",
            "properties": {
                "array": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 5,
                    "maxItems": 50,
                    "default": [89, 34, 67, 23, 78, 45, 12, 56, 91, 38, 72, 15, 84, 29, 63]
                },
                "animation_speed": {
                    "type": "number",
                    "minimum": 100,
                    "maximum": 2000,
                    "default": 500,
                    "description": "动画速度（毫秒）"
                },
                "show_comparisons": {
                    "type": "boolean",
                    "default": True,
                    "description": "显示比较过程"
                },
                "show_swaps": {
                    "type": "boolean", 
                    "default": True,
                    "description": "显示交换过程"
                }
            },
            "required": ["array"]
        }
    
    def execute(self, data: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行冒泡排序算法"""
        # 获取输入数据和配置
        array = data.get("array", [89, 34, 67, 23, 78, 45, 12, 56, 91, 38, 72, 15, 84, 29, 63])
        if config is None:
            config = {}
        
        animation_speed = config.get("animation_speed", 500)
        show_comparisons = config.get("show_comparisons", True)
        show_swaps = config.get("show_swaps", True)
        
        # 验证输入
        if not isinstance(array, list) or len(array) < 2:
            raise ValueError("数组必须是包含至少2个元素的列表")
        
        if not all(isinstance(x, (int, float)) for x in array):
            raise ValueError("数组元素必须是数字")
        
        # 复制数组以避免修改原数组
        arr = array.copy()
        n = len(arr)
        
        # 性能指标
        performance_metrics = {
            "comparisons": 0,
            "swaps": 0,
            "iterations": 0,
            "array_length": n
        }
        
        # 初始状态
        self.add_step(
            action="initialize",
            data_snapshot={
                "array": arr.copy(),
                "comparing": [],
                "swapping": [],
                "sorted": [],
                "current_pass": 0,
                "total_passes": n - 1,
                "performance": performance_metrics.copy()
            },
            highlight=[],
            description=f"初始化数组：{arr}"
        )
        
        # 冒泡排序主循环
        for i in range(n):
            performance_metrics["iterations"] += 1
            
            # 本轮开始
            self.add_step(
                action="pass_start",
                data_snapshot={
                    "array": arr.copy(),
                    "comparing": [],
                    "swapping": [],
                    "sorted": list(range(n - i, n)),
                    "current_pass": i + 1,
                    "total_passes": n - 1,
                    "performance": performance_metrics.copy()
                },
                highlight=[],
                description=f"开始第 {i + 1} 轮冒泡，目标：将最大值移到位置 {n - 1 - i}"
            )
            
            swapped = False
            
            # 内层循环：比较相邻元素
            for j in range(0, n - i - 1):
                performance_metrics["comparisons"] += 1
                
                # 比较步骤
                if show_comparisons:
                    self.add_step(
                        action="compare",
                        data_snapshot={
                            "array": arr.copy(),
                            "comparing": [j, j + 1],
                            "swapping": [],
                            "sorted": list(range(n - i, n)),
                            "current_pass": i + 1,
                            "total_passes": n - 1,
                            "comparison_result": ">" if arr[j] > arr[j + 1] else "<=",
                            "performance": performance_metrics.copy()
                        },
                        highlight=[j, j + 1],
                        description=f"比较 {arr[j]} 和 {arr[j + 1]}：{arr[j]} {'>' if arr[j] > arr[j + 1] else '<='} {arr[j + 1]}"
                    )
                
                # 如果需要交换
                if arr[j] > arr[j + 1]:
                    # 交换前的状态
                    if show_swaps:
                        self.add_step(
                            action="swap_start",
                            data_snapshot={
                                "array": arr.copy(),
                                "comparing": [],
                                "swapping": [j, j + 1],
                                "sorted": list(range(n - i, n)),
                                "current_pass": i + 1,
                                "total_passes": n - 1,
                                "swap_values": [arr[j], arr[j + 1]],
                                "performance": performance_metrics.copy()
                            },
                            highlight=[j, j + 1],
                            description=f"需要交换：{arr[j]} 和 {arr[j + 1]}"
                        )
                    
                    # 执行交换
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    performance_metrics["swaps"] += 1
                    
                    # 交换后的状态
                    if show_swaps:
                        self.add_step(
                            action="swap_complete",
                            data_snapshot={
                                "array": arr.copy(),
                                "comparing": [],
                                "swapping": [j, j + 1],
                                "sorted": list(range(n - i, n)),
                                "current_pass": i + 1,
                                "total_passes": n - 1,
                                "swap_values": [arr[j], arr[j + 1]],
                                "performance": performance_metrics.copy()
                            },
                            highlight=[j, j + 1],
                            description=f"交换完成：位置 {j} 和 {j + 1}"
                        )
            
            # 本轮结束，确定一个元素的最终位置
            self.add_step(
                action="pass_complete",
                data_snapshot={
                    "array": arr.copy(),
                    "comparing": [],
                    "swapping": [],
                    "sorted": list(range(n - i - 1, n)),
                    "current_pass": i + 1,
                    "total_passes": n - 1,
                    "fixed_element": n - i - 1,
                    "performance": performance_metrics.copy()
                },
                highlight=[n - i - 1],
                description=f"第 {i + 1} 轮完成，元素 {arr[n - i - 1]} 已就位"
            )
            
            # 如果没有交换发生，说明已经排序完成
            if not swapped:
                break
        
        # 排序完成
        self.add_step(
            action="complete",
            data_snapshot={
                "array": arr.copy(),
                "comparing": [],
                "swapping": [],
                "sorted": list(range(n)),
                "current_pass": performance_metrics["iterations"],
                "total_passes": n - 1,
                "performance": performance_metrics.copy()
            },
            highlight=list(range(n)),
            description=f"排序完成！结果：{arr}"
        )
        
        # 返回最终结果数据（会被create_result包装）
        return {
            "sorted_array": arr,
            "original_array": array,
            "comparisons": performance_metrics["comparisons"],
            "swaps": performance_metrics["swaps"],
            "iterations": performance_metrics["iterations"]
        }


# 注册算法
def get_algorithm():
    """获取算法实例"""
    return BubbleSortAlgorithm()