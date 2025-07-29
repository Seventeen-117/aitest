# coding: utf-8
# @Author: bgtech
import pytest
import os

if __name__ == "__main__":
    # 确保report目录存在
    report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    # 生成带时间戳的报告文件名
    import datetime
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"report_{now}.html")
    # 执行pytest并生成html报告
    pytest.main([
        "testcase",
        f"--html={report_file}",
        "--self-contained-html"
    ])git add