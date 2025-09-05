#!/usr/bin/env python3
"""
测试石头分配算法
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.algorithms.stone_distribution import StoneDistributionAlgorithm

def test_simple_case():
    """测试简单情况：9格子，90石头，3等分"""
    print("=== 测试石头分配算法 ===")
    
    algorithm = StoneDistributionAlgorithm()
    algorithm.reset_steps()
    
    # 测试配置
    data = {}
    config = {
        "k_boxes": 9,
        "n_stones": 90,
        "p_parts": 3,
        "initial_box": 0,
        "max_steps": 25
    }
    
    try:
        print(f"问题: {config['k_boxes']}个格子，{config['n_stones']}个石头，{config['p_parts']}等分")
        print(f"初始状态: 格子{config['initial_box']}有{config['n_stones']}个石头")
        print(f"目标: 前{config['p_parts']}个格子各有{config['n_stones']//config['p_parts']}个石头")
        print()
        
        result = algorithm.execute(data, config)
        
        print(f"结果: 最少需要 {result['min_steps']} 步")
        
        if result['min_steps'] > 0:
            print("\n解决方案:")
            for i, (action_type, from_box, to_box, amount, state) in enumerate(result['path']):
                action_desc = "移动一半" if action_type == "half" else "移动全部"
                print(f"第{i+1}步: {action_desc} - 从格子{from_box}移动{amount}个石头到格子{to_box}")
                print(f"     状态: {state}")
            
            print(f"\n最终状态: {result['path'][-1][4] if result['path'] else result['target_state']}")
        
        # 显示步骤信息
        print(f"\n算法执行了 {len(algorithm.steps)} 个步骤")
        
        return result
        
    except Exception as e:
        print(f"算法执行失败: {e}")
        return None

def test_multiple_cases():
    """测试多个案例"""
    test_cases = [
        {"k": 4, "n": 12, "p": 3, "desc": "简单情况"},
        {"k": 5, "n": 20, "p": 2, "desc": "5格子20石头2等分"},
        {"k": 6, "n": 18, "p": 3, "desc": "6格子18石头3等分"},
    ]
    
    for case in test_cases:
        print(f"\n{'='*50}")
        print(f"测试案例: {case['desc']}")
        
        algorithm = StoneDistributionAlgorithm()
        algorithm.reset_steps()
        
        config = {
            "k_boxes": case["k"],
            "n_stones": case["n"], 
            "p_parts": case["p"],
            "initial_box": 0,
            "max_steps": 10
        }
        
        try:
            result = algorithm.execute({}, config)
            print(f"结果: {result['min_steps']} 步")
        except Exception as e:
            print(f"失败: {e}")

if __name__ == "__main__":
    # 测试原问题
    result = test_simple_case()
    
    # 测试其他案例
    test_multiple_cases()