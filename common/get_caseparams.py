# coding: utf-8
# @Author: bgtech
import pandas as pd
import json
import os
import sys

# 尝试导入yaml，如果不可用则提供替代方案
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("警告: PyYAML未安装，YAML文件将无法读取")

def safe_yaml_load(file):
    """安全的YAML加载函数，处理Python版本兼容性问题"""
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML is not installed")
    
    try:
        return yaml.safe_load(file)
    except AttributeError as e:
        if "Hashable" in str(e):
            # 修复Python 3.10+的collections.Hashable问题
            import collections.abc
            # 重新定义SafeLoader以使用collections.abc.Hashable
            class SafeLoader(yaml.SafeLoader):
                pass
            
            def construct_mapping(loader, node):
                return dict(loader.construct_pairs(node))
            
            SafeLoader.add_constructor(
                yaml.resolver.Resolver.DEFAULT_MAPPING_TAG,
                construct_mapping
            )
            
            # 重新加载文件
            file.seek(0)
            return yaml.load(file, Loader=SafeLoader)
        else:
            raise e

def read_test_data(file_path, encoding='utf-8'):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == '.xlsx':
            return pd.read_excel(file_path).to_dict(orient='records')
        elif ext in ('.yaml', '.yml'):
            if not YAML_AVAILABLE:
                raise ImportError(f"PyYAML is required to read {file_path}. Please install it with: pip install PyYAML")
            with open(file_path, 'r', encoding=encoding) as file:
                return safe_yaml_load(file)
        elif ext == '.csv':
            return pd.read_csv(file_path, encoding=encoding).to_dict(orient='records')
        elif ext == '.tsv':
            return pd.read_csv(file_path, sep='\t', encoding=encoding).to_dict(orient='records')
        elif ext == '.json':
            with open(file_path, 'r', encoding=encoding) as file:
                return json.load(file)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        raise RuntimeError(f"Failed to read {file_path} with encoding {encoding}: {e}")