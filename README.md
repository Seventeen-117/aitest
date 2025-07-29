# PythonProject 接口自动化测试平台

## 项目简介
本项目是基于 Python + pytest + requests 的企业级接口自动化测试平台，支持多环境配置、数据驱动、日志与报告自动生成，适用于企业接口测试全流程。

---

## 测试流程总览

1. **了解分析需求**：明确接口输入、输出。
2. **数据准备**：整理接口基本信息（url、请求方式）、入参、预期结果。
3. **设计测试**：生成可执行测试用例文件，设计断言。
4. **执行测试**：读取准备数据进行参数化，调用接口并断言验证输出，输出日志。
5. **查看结果**：查看测试报告和日志，分析接口表现。

---

## 目录结构

```
PythonProject/
├── caseparams/           # 测试用例数据（csv/yaml/excel等）
├── common/               # 通用基础模块（配置、日志、断言等）
├── conf/                 # 环境/接口/数据库等配置
├── data_prepare/         # 数据准备与预处理（如造数、数据库操作等）
├── design/               # 测试设计相关（断言模板、用例生成模板等）
├── execution/            # 测试执行相关（参数化、执行入口等）
├── log/                  # 日志输出目录
├── report/               # 测试报告输出目录
├── testcase/             # 自动生成/手写的pytest测试用例脚本
├── utils/                # 工具类（http、json、excel等）
└── README.md             # 项目说明文档
```

---

## 各目录职责说明

- **caseparams/**  
  存放所有接口的测试数据文件，支持csv/yaml/excel等多格式，便于数据驱动。
- **common/**  
  放置全局通用的基础能力，如配置加载（config.py）、日志（log.py）、断言（assertion.py）等。
- **conf/**  
  存放环境、接口、数据库等配置文件，支持ini/yaml等格式。
- **data_prepare/**  
  数据准备相关，如数据库操作（db_utils.py）、造数脚本（data_factory.py）等。
- **design/**  
  测试设计相关，如断言模板（assertion_template.py）、用例生成模板（testcase_template.py）等。
- **execution/**  
  测试执行相关，如pytest钩子（conftest.py）、批量执行器（executor.py）等。
- **log/**  
  日志输出目录，自动生成和轮转。
- **report/**  
  测试报告输出目录，存放html等格式的测试报告。
- **testcase/**  
  存放自动生成或手写的pytest测试用例脚本。
- **utils/**  
  工具类目录，封装http、json、excel等常用工具。

---

## 环境配置

- **conf/env.yaml**：多环境信息（dev/test/prod），可通过common/config.py自动加载。
- **conf/interface.ini**：接口基础信息配置。
- **common/config.py**：自动加载conf下所有ini/yaml配置，支持多级key访问。

---

## 数据准备

- **caseparams/**：存放各接口的测试数据（如test_http_data.csv、test_chat_gateway.yaml等）。
- **data_prepare/db_utils.py**：数据库连接与查询工具。
- **data_prepare/data_factory.py**：造数脚本示例。

---

## 测试设计

- **design/assertion_template.py**：常用断言函数模板。
- **design/testcase_template.py**：pytest用例生成模板。

---

## 测试执行

- **execution/conftest.py**：pytest参数化和前置后置钩子。
- **execution/executor.py**：批量执行pytest并生成报告。
- **run.py**：主执行入口，自动生成报告到report目录。

---

## 日志与报告

- **log/**：所有测试日志自动输出到log/log.log，每天轮转，保留7天。
- **report/**：pytest-html自动生成的测试报告，支持历史报告归档。

---

## 用例开发与执行流程

1. **准备接口配置和测试数据**
   - 在conf/interface.ini、env.yaml中配置接口和环境信息。
   - 在caseparams/下新建csv/yaml/excel等测试数据文件。
2. **生成/编写测试用例**
   - 可用design/testcase_template.py批量生成用例，也可手写testcase/下的pytest用例。
3. **执行测试**
   - 推荐用run.py或execution/executor.py批量执行，自动生成报告。
   - 也可用命令行：
     ```
     set PYTHONPATH=E:\PythonProject
     pytest testcase --html=report/report.html --self-contained-html
     ```
4. **查看结果**
   - 查看report/下的html报告和log/下的日志文件。

---

## 常见问题

- **ModuleNotFoundError: No module named 'common'**
  - 需设置PYTHONPATH为项目根目录，或在run.py中自动添加sys.path。
- **ConnectionRefusedError**
  - 检查接口服务是否已启动，地址端口是否正确。
- **Excel/CSV/YAML数据读取异常**
  - 检查文件格式、路径、编码，推荐用pandas/yaml等库统一读取。

---

## 联系与贡献

如有问题或建议，欢迎提交issue或联系项目维护者。 