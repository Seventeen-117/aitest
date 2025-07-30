#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本 - 检查pytest和相关依赖是否已安装
"""

import sys
import subprocess
import importlib

def check_module(module_name):
    """检查模块是否已安装"""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def main():
    print("=== Python环境检查 ===")
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    print("\n=== 依赖检查 ===")
    modules_to_check = [
        'pytest',
        'pytest_html',
        'requests',
        'yaml',
        'pandas'
    ]
    
    missing_modules = []
    for module in modules_to_check:
        if check_module(module):
            print(f"✓ {module} - 已安装")
        else:
            print(f"✗ {module} - 未安装")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n=== 需要安装的模块 ===")
        print("请运行以下命令安装缺失的模块:")
        print(f"pip install {' '.join(missing_modules)}")
        
        # 如果pytest未安装，提供替代方案
        if 'pytest' in missing_modules:
            print("\n=== 临时解决方案 ===")
            print("如果无法安装pytest，可以修改run.py使用unittest替代:")
            print("1. 将run.py中的pytest.main()替换为unittest.main()")
            print("2. 或者使用Python内置的unittest模块")
    
    else:
        print("\n✓ 所有依赖都已安装，可以正常运行测试!")
        print("运行命令: python run.py")

if __name__ == "__main__":
    main() 