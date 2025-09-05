#!/usr/bin/env python3
"""
分析石头分配问题的数学性质
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.algorithms.stone_distribution import StoneDistributionAlgorithm

def analyze_simple_case():
    """分析简单情况找规律"""
    print("=== 分析简单情况 ===")
    
    # 测试6石头3等分的情况
    algorithm = StoneDistributionAlgorithm()
    algorithm.reset_steps()
    
    config = {
        "k_boxes": 4,
        "n_stones": 6,
        "p_parts": 3,
        "initial_box": 0,
        "max_steps": 10
    }
    
    print(f"问题: {config['k_boxes']}个格子，{config['n_stones']}个石头，{config['p_parts']}等分")
    print(f"目标: 前3个格子各有2个石头")
    
    result = algorithm.execute({}, config)
    
    if result['min_steps'] > 0:
        print(f"\n最优解需要 {result['min_steps']} 步:")
        for i, (action_type, from_box, to_box, amount, state) in enumerate(result['path']):
            action_desc = "移动一半" if action_type == "half" else "移动全部"
            print(f"第{i+1}步: {action_desc} - 从格子{from_box}移动{amount}个石头到格子{to_box}")
            print(f"     状态: {state}")
    
    print("\n=== 手工分析90石头3等分情况 ===")
    print("初始: [90, 0, 0, 0, 0, 0, 0, 0, 0]")
    print("目标: [30, 30, 30, 0, 0, 0, 0, 0, 0]")
    print()
    
    # 手工尝试找解
    print("可能的策略:")
    print("1. 直接分配策略:")
    print("   步骤1: 移动1/3 (30个) 从格子0到格子1 -> [60, 30, 0, ...]")
    print("   步骤2: 移动一半 (30个) 从格子0到格子2 -> [30, 30, 30, ...]")
    print("   但是问题: 无法直接移动1/3!")
    print()
    
    print("2. 通过一半操作的策略:")
    print("   步骤1: 移动一半 (45个) 从格子0到格子1 -> [45, 45, 0, ...]")
    print("   步骤2: 移动一半 (22个) 从格子0到格子2 -> [23, 45, 22, ...]") 
    print("   然后需要调整到 [30, 30, 30, ...]")
    print()
    
    # 测试更大的搜索空间
    print("3. 使用更大搜索深度测试:")
    algorithm2 = StoneDistributionAlgorithm()
    algorithm2.reset_steps()
    
    config2 = {
        "k_boxes": 9,
        "n_stones": 90,
        "p_parts": 3,
        "initial_box": 0,
        "max_steps": 30  # 增加搜索深度
    }
    
    result2 = algorithm2.execute({}, config2)
    if result2['min_steps'] > 0:
        print(f"找到解! 需要 {result2['min_steps']} 步")
    else:
        print("仍未在30步内找到解")

if __name__ == "__main__":
    analyze_simple_case()