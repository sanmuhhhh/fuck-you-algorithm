#!/usr/bin/env python3
"""
Algorithm Visualization Platform - 后端一键启动脚本
克隆仓库后直接运行此脚本即可启动后端服务
"""
import sys
import subprocess
import os
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, shell=True):
    """运行命令并实时显示输出"""
    print(f"执行: {cmd}")
    try:
        process = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd,
            bufsize=1,
            universal_newlines=True
        )
        
        for line in process.stdout:
            print(line.rstrip())
            
        process.wait()
        if process.returncode != 0:
            print(f"命令执行失败，退出码: {process.returncode}")
            return False
        return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def setup_virtual_environment():
    """设置虚拟环境"""
    venv_path = Path("venv")
    
    # 如果虚拟环境已存在，删除它
    if venv_path.exists():
        print("🔄 发现已存在的虚拟环境，正在删除...")
        shutil.rmtree(venv_path)
        print("✅ 旧虚拟环境已删除")
    
    # 创建新的虚拟环境
    print("🚀 正在创建新的虚拟环境...")
    if not run_command(f"{sys.executable} -m venv venv"):
        print("❌ 创建虚拟环境失败")
        return False
    
    print("✅ 虚拟环境创建成功!")
    return True

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装Python依赖...")
    
    # 确定虚拟环境中的Python路径
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python.exe"
        pip_path = "venv\\Scripts\\pip.exe"
    else:  # Unix/Linux/Mac
        python_path = "venv/bin/python"
        pip_path = "venv/bin/pip"
    
    # 升级pip
    print("⬆️  升级pip...")
    if not run_command(f"{python_path} -m pip install --upgrade pip"):
        print("❌ 升级pip失败")
        return False
    
    # 安装依赖
    print("📥 安装项目依赖...")
    if not run_command(f"{pip_path} install -r requirements.txt"):
        print("❌ 安装依赖失败")
        return False
    
    print("✅ 依赖安装完成!")
    return True

def start_server():
    """启动服务器"""
    print("🚀 正在启动FastAPI服务器...")
    
    # 确定虚拟环境中的Python路径
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python.exe"
    else:  # Unix/Linux/Mac
        python_path = "venv/bin/python"
    
    try:
        # 启动服务器
        subprocess.run([
            python_path, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 Algorithm Visualization Platform - 后端启动")
    print("=" * 60)
    
    # 确保在backend目录中
    if not os.path.exists("app"):
        print("❌ 错误: 请在backend目录中运行此脚本")
        print(f"📍 当前目录: {os.getcwd()}")
        print("💡 提示: cd backend && python start.py")
        sys.exit(1)
    
    # 检查requirements.txt是否存在
    if not os.path.exists("requirements.txt"):
        print("❌ 错误: 找不到requirements.txt文件")
        sys.exit(1)
    
    try:
        # 1. 设置虚拟环境
        if not setup_virtual_environment():
            print("❌ 虚拟环境设置失败，退出")
            sys.exit(1)
        
        # 2. 安装依赖
        if not install_dependencies():
            print("❌ 依赖安装失败，退出")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("🎉 设置完成! 正在启动服务器...")
        print("🌐 服务器地址: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/docs")
        print("⚡ 健康检查: http://localhost:8000/health")
        print("🛑 按 Ctrl+C 停止服务器")
        print("=" * 60 + "\n")
        
        # 3. 启动服务器
        start_server()
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断，退出")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()