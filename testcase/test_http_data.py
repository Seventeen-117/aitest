import pytest
import json
from common.get_caseparams import read_test_data
from utils.http_utils import http_get, http_post
from common.log import info, error

# 读取csv测试数据
cases = read_test_data('caseparams/test_http_data.csv')

@pytest.mark.parametrize("case", cases)
def test_http_data(case):
    url = case['url']
    method = case['method'].upper()
    params = json.loads(case['params']) if case.get('params') else {}
    expected = json.loads(case['expected_result']) if case.get('expected_result') else {}

    info(f"执行用例: {case['case_id']} - {case['description']}")
    info(f"请求地址: {url}")
    info(f"请求参数: {params}")

    if method == 'GET':
        resp = http_get(url, params=params)
    elif method == 'POST':
        resp = http_post(url, json_data=params)
    else:
        error(f"暂不支持的请求方式: {method}")
        pytest.skip("暂不支持的请求方式")

    info(f"接口返回: {resp}")

    # 断言：预期内容应包含在返回内容中
    for k, v in expected.items():
        assert k in resp, f"返回内容缺少字段: {k}"
        assert resp[k] == v, f"断言失败: {k} 期望: {v} 实际: {resp[k]}" 