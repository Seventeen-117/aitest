# coding: utf-8
# @Author: bgtech
# 使用unittest的替代方案，当pytest不可用时使用

import unittest
import os
import sys
import datetime

def run_tests_with_unittest():
    """使用unittest运行测试"""
    # 确保report目录存在
    report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # 生成带时间戳的报告文件名
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"report_{now}.txt")
    
    print("开始执行测试...")
    print(f"测试报告将保存到: {report_file}")
    
    # 发现并运行测试
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testcase')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # 运行测试并捕获输出
    with open(report_file, 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)
    
    # 打印结果到控制台
    print(f"\n测试执行完成!")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return len(result.failures) + len(result.errors) == 0

if __name__ == "__main__":
    success = run_tests_with_unittest()
    sys.exit(0 if success else 1) 