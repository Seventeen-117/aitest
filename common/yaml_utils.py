import yaml
import os

def load_yaml(file_path, encoding='utf-8'):
    """
    加载Yaml文件为Python对象
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return yaml.safe_load(f)

def write_yaml(data, file_path, encoding='utf-8'):
    """
    将Python对象写入Yaml文件
    """
    with open(file_path, 'w', encoding=encoding) as f:
        yaml.safe_dump(data, f, allow_unicode=True)

def merge_yaml(yaml1, yaml2):
    """
    合并两个Yaml对象（字典），后者覆盖前者同名key
    """
    if not isinstance(yaml1, dict) or not isinstance(yaml2, dict):
        raise ValueError('只能合并字典类型Yaml')
    result = yaml1.copy()
    result.update(yaml2)
    return result

def validate_yaml_structure(data, required_keys):
    """
    校验Yaml对象是否包含所有必需key
    :param data: Yaml对象（dict）
    :param required_keys: 必需key列表
    :return: bool
    """
    return all(k in data for k in required_keys) 