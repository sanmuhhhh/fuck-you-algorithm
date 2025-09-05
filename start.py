#!/usr/bin/env python3
"""
Algorithm Visualization Platform - 全局一键启动脚本
同时启动前端和后端服务
"""
import sys
import subprocess
import os
import time
import threading
from pathlib import Path

def run_in_directory(directory, script_name, service_name):
    """在指定目录中运行脚本"""
    try:
        print(f"🚀 启动{service_name}...")
        os.chdir(directory)
        subprocess.run([sys.executable, script_name])
    except KeyboardInterrupt:
        print(f"\n🛑 {service_name}已停止")
    except Exception as e:
        print(f"❌ {service_name}启动失败: {e}")

def check_directories():
    """检查必要的目录和文件是否存在"""
    backend_dir = Path("backend")
    frontend_dir = Path("frontend")
    
    if not backend_dir.exists():
        print("❌ 错误: 找不到backend目录")
        return False
    
    if not frontend_dir.exists():
        print("❌ 错误: 找不到frontend目录")
        return False
    
    if not (backend_dir / "start.py").exists():
        print("❌ 错误: 找不到backend/start.py")
        return False
    
    if not (frontend_dir / "start.py").exists():
        print("❌ 错误: 找不到frontend/start.py")
        return False
    
    return True

def main():
    """主函数"""
    print("=" * 70)
    print("🎯 Algorithm Visualization Platform - 全平台启动")
    print("=" * 70)
    
    # 检查目录结构
    if not check_directories():
        print("❌ 目录检查失败，请确保在项目根目录运行此脚本")
        sys.exit(1)
    
    print("✅ 目录检查通过")
    print("\n" + "=" * 70)
    print("🚀 正在启动服务...")
    print("💡 建议:")
    print("   1. 先等待后端启动完成 (约30-60秒)")
    print("   2. 再启动前端服务")
    print("   3. 或者分别在不同终端运行:")
    print("      - cd backend && python start.py")
    print("      - cd frontend && python start.py")
    print("=" * 70)
    
    choice = input("\n请选择启动方式:\n1. 仅启动后端\n2. 仅启动前端\n3. 先启动后端，后启动前端\n请输入选择 (1/2/3): ").strip()
    
    try:
        if choice == "1":
            print("\n🔗 启动后端服务...")
            os.chdir("backend")
            subprocess.run([sys.executable, "start.py"])
            
        elif choice == "2":
            print("\n🎨 启动前端服务...")
            os.chdir("frontend") 
            subprocess.run([sys.executable, "start.py"])
            
        elif choice == "3":
            print("\n🔗 首先启动后端...")
            backend_thread = threading.Thread(
                target=run_in_directory, 
                args=("backend", "start.py", "后端服务")
            )
            backend_thread.daemon = True
            backend_thread.start()
            
            print("⏳ 等待后端启动 (30秒)...")
            time.sleep(30)
            
            print("\n🎨 现在启动前端...")
            os.chdir("frontend")
            subprocess.run([sys.executable, "start.py"])
            
        else:
            print("❌ 无效选择，退出")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 用户中断，退出")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()