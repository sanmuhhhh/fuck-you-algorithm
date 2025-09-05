from typing import Dict, List, Type
import importlib
import pkgutil
from app.core.base_algorithm import BaseAlgorithm
from app.models.algorithm import AlgorithmMetadata

class AlgorithmRegistry:
    """算法注册器"""
    
    def __init__(self):
        self._algorithms: Dict[str, Type[BaseAlgorithm]] = {}
        
    def register(self, name: str, algorithm_class: Type[BaseAlgorithm]):
        """注册算法"""
        if not issubclass(algorithm_class, BaseAlgorithm):
            raise ValueError(f"Algorithm {name} must inherit from BaseAlgorithm")
        self._algorithms[name] = algorithm_class
        
    def get_algorithm(self, name: str) -> Type[BaseAlgorithm]:
        """获取算法类"""
        if name not in self._algorithms:
            raise ValueError(f"Algorithm {name} not found")
        return self._algorithms[name]
        
    def get_algorithm_instance(self, name: str) -> BaseAlgorithm:
        """获取算法实例"""
        algorithm_class = self.get_algorithm(name)
        return algorithm_class()
        
    def list_algorithms(self) -> List[AlgorithmMetadata]:
        """获取所有算法的元数据"""
        metadata_list = []
        for name, algorithm_class in self._algorithms.items():
            instance = algorithm_class()
            metadata_list.append(instance.get_metadata())
        return metadata_list
        
    def discover_algorithms(self):
        """自动发现并注册算法"""
        try:
            # 导入算法模块
            import app.algorithms
            
            # 递归导入所有子模块
            def import_submodules(package):
                for _, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
                    try:
                        importlib.import_module(name)
                        if ispkg:
                            submodule = importlib.import_module(name)
                            import_submodules(submodule)
                    except Exception as e:
                        print(f"Failed to import {name}: {e}")
            
            import_submodules(app.algorithms)
            print(f"Discovered {len(self._algorithms)} algorithms")
            
        except ImportError:
            print("No algorithms package found")

# 全局注册器实例
algorithm_registry = AlgorithmRegistry()

def algorithm_register(name: str, display_name: str, category: str, description: str, 
                      complexity_time: str = None, complexity_space: str = None):
    """算法注册装饰器"""
    def decorator(cls: Type[BaseAlgorithm]):
        # 注册到全局注册器
        algorithm_registry.register(name, cls)
        return cls
    
    return decorator