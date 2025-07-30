# 解决 pytest 执行报错问题

## 问题描述
执行 `python run.py` 时出现以下错误：
```
ERROR: usage: run.py [options] [file_or_dir] [file_or_dir] [...]
run.py: error: unrecognized arguments: --html=C:\Users\sy_li\aitest\report\report_20250730_101920.html --self-contained-html
```

## 问题原因
1. **pytest 未安装**: 系统中没有安装 pytest 模块
2. **pytest-html 插件未安装**: 缺少生成 HTML 报告的插件
3. **参数传递问题**: 原始代码直接传递参数给 pytest.main() 可能导致参数解析错误

## 解决方案

### 1. 安装必要的依赖包
运行以下命令安装所需的包：
```bash
python -m pip install --user pytest pytest-html pandas PyYAML requests openpyxl
```

或者使用提供的安装脚本：
```bash
python install_dependencies.py
```

### 2. 修改 run.py 文件
已更新 `run.py` 文件，主要改进：
- 添加了依赖检查机制
- 改进了参数传递方式
- 增加了错误处理和用户友好的提示信息
- 添加了详细的执行状态输出

### 3. 配置文件
创建了以下配置文件：
- `pytest.ini`: pytest 配置文件，设置测试路径和选项
- `requirements.txt`: 项目依赖列表

## 修复后的功能

### 主要改进
1. **智能依赖检查**: 自动检测 pytest-html 插件是否可用
2. **优雅降级**: 如果 HTML 报告插件不可用，仍可正常运行测试
3. **详细输出**: 提供清晰的执行状态和错误信息
4. **错误处理**: 完善的异常处理和退出码管理

### 使用方法
```bash
# 检查环境
python check_environment.py

# 安装依赖
python install_dependencies.py

# 运行测试
python run.py
```

## 替代方案
如果无法安装 pytest，可以使用 unittest 替代：
```bash
python run_unittest.py
```

## 文件说明
- `run.py`: 主测试执行脚本（已修复）
- `run_unittest.py`: 使用 unittest 的替代方案
- `check_environment.py`: 环境检查脚本
- `install_dependencies.py`: 依赖安装脚本
- `pytest.ini`: pytest 配置文件
- `requirements.txt`: 项目依赖列表

## 验证修复
运行以下命令验证修复是否成功：
```bash
python check_environment.py
python run.py
```

如果看到类似以下输出，说明修复成功：
```
将生成HTML报告: C:\Users\sy_li\aitest\report\report_20250730_104840.html
开始执行测试...
======================================== test session starts =========================================
```

## 注意事项
1. 确保 Python 环境正确配置
2. 如果使用虚拟环境，请先激活虚拟环境
3. 如果遇到权限问题，使用 `--user` 参数安装包
4. 某些包可能需要较长时间下载，请耐心等待 