"""
石头分配算法实现
通过BFS找到将石头P等分到指定格子的最少步数
"""
import time
from typing import List, Dict, Any, Tuple, Set
from collections import deque
from app.core.base_algorithm import BaseAlgorithm
from app.core.registry import algorithm_register
from app.models.algorithm import AlgorithmMetadata


@algorithm_register(
    name="stone_distribution",
    display_name="石头分配问题",
    category="数学优化",
    description="通过最少步数将K个格子中的N个石头P等分到指定格子中",
    complexity_time="O(状态数 × 转移数)",
    complexity_space="O(状态数)"
)
class StoneDistributionAlgorithm(BaseAlgorithm):
    """石头分配算法类"""
    
    def get_metadata(self) -> AlgorithmMetadata:
        """获取算法元数据"""
        return AlgorithmMetadata(
            name="stone_distribution",
            display_name="石头分配问题",
            category="数学优化",
            description="通过最少步数将K个格子中的N个石头P等分到指定格子中",
            complexity_time="O(状态数 × 转移数)",
            complexity_space="O(状态数)",
            author="Claude"
        )
    
    def get_config_schema(self) -> Dict[str, Any]:
        """获取算法配置模式"""
        return {
            "type": "object",
            "properties": {
                "k_boxes": {
                    "type": "integer",
                    "minimum": 3,
                    "maximum": 20,
                    "default": 9,
                    "description": "格子数量K"
                },
                "n_stones": {
                    "type": "integer",
                    "minimum": 3,
                    "maximum": 300,
                    "default": 90,
                    "description": "石头总数N"
                },
                "p_parts": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 10,
                    "default": 3,
                    "description": "等分数量P"
                },
            },
            "required": ["k_boxes", "n_stones", "p_parts"]
        }
    
    def execute(self, data: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行石头分配算法"""
        # 获取参数
        if config is None:
            config = {}
        
        k_boxes = config.get("k_boxes", 9)
        n_stones = config.get("n_stones", 90)
        p_parts = config.get("p_parts", 3)
        initial_box = 0  # 始终从第0个格子开始
        
        # 验证输入
        if n_stones % p_parts != 0:
            raise ValueError(f"石头数量{n_stones}无法{p_parts}等分")
        
        if p_parts > k_boxes:
            raise ValueError(f"等分数{p_parts}不能大于格子数{k_boxes}")
        
        
        target_stones_per_part = n_stones // p_parts
        
        # 初始状态
        initial_state = [0] * k_boxes
        initial_state[initial_box] = n_stones
        
        # 目标状态：前P个格子各有target_stones_per_part个石头
        target_state = [target_stones_per_part if i < p_parts else 0 for i in range(k_boxes)]
        
        self.add_step(
            action="initialize",
            data_snapshot={
                "current_state": initial_state.copy(),
                "target_state": target_state.copy(),
                "k_boxes": k_boxes,
                "n_stones": n_stones,
                "p_parts": p_parts,
                "target_per_part": target_stones_per_part,
                "step_count": 0,
                "visited_states": 1
            },
            highlight=[initial_box],
            description=f"初始状态: 格子{initial_box}有{n_stones}个石头，目标: 前{p_parts}个格子各有{target_stones_per_part}个石头"
        )
        
        # BFS搜索最优解
        result = self._bfs_solve(initial_state, target_state, k_boxes)
        
        if result is None:
            self.add_step(
                action="no_solution",
                data_snapshot={
                    "current_state": initial_state.copy(),
                    "target_state": target_state.copy(),
                    "step_count": -1,
                    "message": "算法无解或搜索空间过大"
                },
                highlight=[],
                description="算法无解或搜索空间过大，请尝试调整参数"
            )
            return {
                "min_steps": -1,
                "path": [],
                "initial_state": initial_state,
                "target_state": target_state,
                "message": "算法无解或搜索空间过大"
            }
        
        steps, path = result
        
        # 记录解的路径
        for i, (action_type, from_box, to_box, amount, state) in enumerate(path):
            action_desc = "移动一半" if action_type == "half" else "移动全部"
            self.add_step(
                action="move",
                data_snapshot={
                    "current_state": state.copy(),
                    "target_state": target_state.copy(),
                    "step_count": i + 1,
                    "action_type": action_type,
                    "from_box": from_box,
                    "to_box": to_box,
                    "amount": amount
                },
                highlight=[from_box, to_box],
                description=f"第{i+1}步: {action_desc} - 从格子{from_box}移动{amount}个石头到格子{to_box}"
            )
        
        self.add_step(
            action="complete",
            data_snapshot={
                "current_state": path[-1][4].copy() if path else target_state.copy(),
                "target_state": target_state.copy(),
                "step_count": steps,
                "solution_found": True
            },
            highlight=list(range(p_parts)),
            description=f"找到最优解！最少需要{steps}步完成{p_parts}等分"
        )
        
        return {
            "min_steps": steps,
            "path": path,
            "initial_state": initial_state,
            "target_state": target_state,
            "k_boxes": k_boxes,
            "n_stones": n_stones,
            "p_parts": p_parts
        }
    
    def _bfs_solve(self, initial_state: List[int], target_state: List[int], 
                   k_boxes: int) -> Tuple[int, List]:
        """使用BFS搜索最优解"""
        
        def state_to_tuple(state):
            return tuple(state)
        
        def is_target(state):
            return state == target_state
        
        def generate_moves(state):
            """生成所有可能的移动"""
            moves = []
            for i in range(k_boxes):
                if state[i] > 0:
                    for j in range(k_boxes):
                        if i != j:
                            # 操作1: 移动一半石头
                            if state[i] >= 2:
                                half = state[i] // 2
                                new_state = state.copy()
                                new_state[i] -= half
                                new_state[j] += half
                                moves.append(("half", i, j, half, new_state))
                            
                            # 操作2: 移动全部石头
                            all_stones = state[i]
                            new_state = state.copy()
                            new_state[i] = 0
                            new_state[j] += all_stones
                            moves.append(("all", i, j, all_stones, new_state))
            return moves
        
        # BFS
        queue = deque([(initial_state, 0, [])])  # (state, steps, path)
        visited = {state_to_tuple(initial_state)}
        states_explored = 0
        
        while queue and states_explored < 100000:  # 防止无限搜索
            current_state, steps, path = queue.popleft()
            states_explored += 1
            
            if is_target(current_state):
                return steps, path
            
            
            # 定期记录搜索进度
            if states_explored % 1000 == 0:
                self.add_step(
                    action="searching",
                    data_snapshot={
                        "current_state": current_state.copy(),
                        "target_state": target_state,
                        "step_count": steps,
                        "states_explored": states_explored,
                        "queue_size": len(queue)
                    },
                    highlight=[],
                    description=f"搜索中... 已探索{states_explored}个状态，当前步数{steps}"
                )
            
            # 生成所有可能的下一步
            for move in generate_moves(current_state):
                action_type, from_box, to_box, amount, new_state = move
                state_tuple = state_to_tuple(new_state)
                
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    new_path = path + [move]
                    queue.append((new_state, steps + 1, new_path))
        
        return None  # 未找到解


# 注册算法
def get_algorithm():
    """获取算法实例"""
    return StoneDistributionAlgorithm()