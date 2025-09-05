#!/usr/bin/env python3
"""
Algorithm Visualization Platform - 前端一键启动脚本
克隆仓库后直接运行此脚本即可启动前端服务
"""
import sys
import subprocess
import os
import shutil
import json
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

def check_node_npm():
    """检查Node.js和npm是否安装"""
    print("🔍 检查Node.js和npm...")
    
    try:
        # 检查Node.js
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            node_version = result.stdout.strip()
            print(f"✅ Node.js 已安装: {node_version}")
        else:
            print("❌ Node.js 未安装")
            print("💡 请访问 https://nodejs.org/ 下载并安装 Node.js")
            return False
        
        # 检查npm
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            npm_version = result.stdout.strip()
            print(f"✅ npm 已安装: {npm_version}")
            return True
        else:
            print("❌ npm 未安装")
            print("💡 请访问 https://nodejs.org/ 下载并安装 Node.js")
            return False
            
    except Exception as e:
        print(f"❌ Node.js/npm 检查失败: {e}")
        print("💡 请访问 https://nodejs.org/ 下载并安装 Node.js")
        return False

def clean_install():
    """清理并重新安装依赖"""
    print("🧹 清理旧的依赖...")
    
    # 删除node_modules和package-lock.json
    node_modules_path = Path("node_modules")
    lock_file_path = Path("package-lock.json")
    
    if node_modules_path.exists():
        print("🔄 删除 node_modules...")
        try:
            # Windows上可能需要多次尝试删除
            import time
            max_retries = 3
            for i in range(max_retries):
                try:
                    shutil.rmtree(node_modules_path)
                    print("✅ node_modules 已删除")
                    break
                except PermissionError as e:
                    if i < max_retries - 1:
                        print(f"⚠️  删除失败，可能有进程占用文件，3秒后重试... ({i+1}/{max_retries})")
                        time.sleep(3)
                    else:
                        print(f"❌ 无法删除 node_modules: {e}")
                        print("💡 请确保没有开发服务器正在运行，或手动删除 node_modules 文件夹")
                        print("💡 如果服务器正在运行，请按 Ctrl+C 停止后再运行此脚本")
                        return False
        except Exception as e:
            print(f"❌ 删除 node_modules 失败: {e}")
            return False
    
    if lock_file_path.exists():
        print("🔄 删除 package-lock.json...")
        try:
            lock_file_path.unlink()
            print("✅ package-lock.json 已删除")
        except Exception as e:
            print(f"❌ 删除 package-lock.json 失败: {e}")
            return False
    
    return True

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装前端依赖...")
    
    if not run_command("npm install"):
        print("❌ 安装依赖失败")
        return False
    
    print("✅ 依赖安装完成!")
    return True

def start_dev_server():
    """启动开发服务器"""
    print("🚀 正在启动Vue开发服务器...")
    
    try:
        # Windows需要shell=True
        subprocess.run(["npm", "run", "dev"], shell=True)
    except KeyboardInterrupt:
        print("\n🛑 开发服务器已停止")
    except Exception as e:
        print(f"❌ 启动开发服务器失败: {e}")

def check_package_json():
    """检查package.json是否存在和配置正确"""
    if not os.path.exists("package.json"):
        print("❌ 错误: 找不到package.json文件")
        return False
    
    try:
        with open("package.json", "r", encoding="utf-8") as f:
            package_data = json.load(f)
        
        # 检查是否有dev脚本
        scripts = package_data.get("scripts", {})
        if "dev" not in scripts:
            print("⚠️  警告: package.json中没有找到dev脚本")
            print("💡 请确保package.json中有 'dev' 脚本配置")
            return False
        
        print(f"✅ package.json 配置正确")
        return True
    except json.JSONDecodeError:
        print("❌ 错误: package.json 格式不正确")
        return False
    except Exception as e:
        print(f"❌ 读取package.json失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🎨 Algorithm Visualization Platform - 前端启动")
    print("=" * 60)
    
    # 确保在frontend目录中
    if not os.path.exists("package.json"):
        print("❌ 错误: 请在frontend目录中运行此脚本")
        print(f"📍 当前目录: {os.getcwd()}")
        print("💡 提示: cd frontend && python start.py")
        sys.exit(1)
    
    try:
        # 1. 检查Node.js和npm
        if not check_node_npm():
            print("❌ Node.js/npm 检查失败，退出")
            sys.exit(1)
        
        # 2. 检查package.json
        if not check_package_json():
            print("❌ package.json 检查失败，退出") 
            sys.exit(1)
        
        # 3. 清理并安装依赖
        if not clean_install():
            print("❌ 清理失败，退出")
            sys.exit(1)
            
        if not install_dependencies():
            print("❌ 依赖安装失败，退出")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("🎉 设置完成! 正在启动开发服务器...")
        print("🌐 前端地址: http://localhost:5173")
        print("🔗 确保后端已启动: http://localhost:8000")
        print("🛑 按 Ctrl+C 停止服务器")
        print("=" * 60 + "\n")
        
        # 4. 启动开发服务器
        start_dev_server()
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断，退出")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()