#!/usr/bin/env python3
"""
API测试脚本
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_algorithms_list():
    """测试获取算法列表"""
    try:
        response = requests.get(f"{BASE_URL}/api/algorithms")
        print(f"Algorithms list: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total']} algorithms:")
            for alg in data['algorithms']:
                print(f"  - {alg['display_name']} ({alg['name']})")
        return response.status_code == 200
    except Exception as e:
        print(f"Algorithms list failed: {e}")
        return False

def test_algorithm_config():
    """测试获取算法配置"""
    try:
        response = requests.get(f"{BASE_URL}/api/algorithms/hello_world/config")
        print(f"Algorithm config: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Config schema: {json.dumps(data['schema'], indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Algorithm config failed: {e}")
        return False

def test_algorithm_execution():
    """测试算法执行"""
    try:
        payload = {
            "data": {"num1": 5, "num2": 3},
            "config": {"num1": 5, "num2": 3, "show_steps": True}
        }
        response = requests.post(f"{BASE_URL}/api/algorithms/hello_world/execute", json=payload)
        print(f"Algorithm execution: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Result: {data['final_result']}")
            print(f"Steps: {len(data['steps'])}")
            print(f"Execution time: {data['execution_time']*1000:.2f}ms")
            for i, step in enumerate(data['steps']):
                print(f"  Step {i+1}: {step['description']}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Algorithm execution failed: {e}")
        return False

def main():
    print("=== API测试开始 ===")
    
    # 等待服务器启动
    print("等待服务器启动...")
    for i in range(10):
        if test_health():
            break
        time.sleep(2)
        print(f"等待中... ({i+1}/10)")
    else:
        print("服务器启动失败!")
        return
    
    print("\n=== 测试算法列表 ===")
    test_algorithms_list()
    
    print("\n=== 测试算法配置 ===")
    test_algorithm_config()
    
    print("\n=== 测试算法执行 ===")
    test_algorithm_execution()
    
    print("\n=== API测试完成 ===")

if __name__ == "__main__":
    main()