#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速安装脚本 - 只安装必要的依赖
"""

import subprocess
import sys

def install_package(package):
    """安装单个包"""
    try:
        print(f"正在安装 {package}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--user", package
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✓ {package} 安装成功")
            return True
        else:
            print(f"✗ {package} 安装失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {package} 安装超时")
        return False
    except Exception as e:
        print(f"✗ {package} 安装失败: {e}")
        return False

def main():
    print("=== 快速安装必要依赖 ===")
    
    # 只安装最必要的包
    essential_packages = [
        "PyYAML",
        "pandas"
    ]
    
    success_count = 0
    for package in essential_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n=== 安装完成 ===")
    print(f"成功安装: {success_count}/{len(essential_packages)} 个包")
    
    if success_count == len(essential_packages):
        print("✓ 所有必要依赖都已安装完成!")
        print("现在可以运行: python run.py")
    else:
        print("⚠ 部分依赖安装失败，请手动安装:")
        print("pip install PyYAML pandas")

if __name__ == "__main__":
    main() 