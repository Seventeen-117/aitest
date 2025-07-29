# coding: utf-8
# @Author: bgtech
def assert_response(actual, expected):
    assert actual == expected, f"Expected {expected}, but got {actual}"