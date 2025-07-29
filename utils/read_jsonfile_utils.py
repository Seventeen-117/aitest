import json

def read_json_file(file_path, encoding='utf-8'):
    """
    读取指定路径的json文件内容并返回解析后的对象。
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return json.load(f) 