#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖安装脚本 - 安装项目所需的所有Python包
"""

import subprocess
import sys
import importlib

def install_package(package):
    """安装单个包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--user", package
        ])
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败: {e}")
        return False

def check_package(package):
    """检查包是否已安装"""
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False

def main():
    print("=== 项目依赖安装 ===")
    
    # 需要安装的包列表
    packages = [
        "pytest",
        "pytest-html", 
        "pandas",
        "PyYAML",
        "requests",
        "openpyxl"
    ]
    
    success_count = 0
    for package in packages:
        # 检查是否已安装
        if check_package(package.replace("-", "_")):
            print(f"✓ {package} 已安装")
            success_count += 1
        else:
            # 尝试安装
            if install_package(package):
                success_count += 1
    
    print(f"\n=== 安装完成 ===")
    print(f"成功安装: {success_count}/{len(packages)} 个包")
    
    if success_count == len(packages):
        print("✓ 所有依赖都已安装完成!")
        print("现在可以运行: python run.py")
    else:
        print("⚠ 部分依赖安装失败，请手动安装缺失的包")

if __name__ == "__main__":
    main() 