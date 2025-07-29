# coding: utf-8
# @Author: bgtech
import pandas as pd
import yaml
import json
import os

def read_test_data(file_path, encoding='utf-8'):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == '.xlsx':
            return pd.read_excel(file_path).to_dict(orient='records')
        elif ext in ('.yaml', '.yml'):
            with open(file_path, 'r', encoding=encoding) as file:
                return yaml.safe_load(file)
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