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

### 多配置文件加载

`InterfaceConfig` 类支持加载多个配置文件并自动合并配置。支持 YAML 和 INI 格式的配置文件。

#### 支持的配置文件

1. **conf/env.yaml** - 环境配置（开发、测试、生产环境）
2. **conf/interface_info.yaml** - 接口配置信息
3. **conf/interface.ini** - 数据库等其他配置

#### 配置优先级

配置文件按以下优先级加载和合并：
1. `env.yaml` - 环境配置（最高优先级）
2. `interface_info.yaml` - 接口配置
3. `interface.ini` - 其他配置（最低优先级）

#### 使用方法

```python
from common.interface_config import InterfaceConfig, get_interface_config

# 使用默认配置文件列表
config = InterfaceConfig()

# 获取当前环境
current_env = config.get_current_env()  # 返回: 'dev'

# 获取环境配置
env_config = config.get_env_config()  # 返回当前环境的配置

# 获取API基础URL
api_base_url = config.get_api_base_url()  # 返回当前环境的API基础URL

# 获取登录接口配置（会自动根据当前环境替换URL）
login_config = get_interface_config('user', 'login')

# 获取指定环境的接口配置
test_login_config = get_interface_config('user', 'login', 'test')
prod_login_config = get_interface_config('user', 'login', 'prod')

# 获取数据库配置
db_config = config.get_database_config()
test_db_config = config.get_database_config('test')
```

#### 配置文件格式

**env.yaml 格式：**
```yaml
env:
  current: dev  # 当前环境
  dev:
    host: 127.0.0.1
    db:
      host: 127.0.0.1
      port: 3306
      user: dev_user
      password: dev_pass
      database: dev_db
    api_base_url: http://127.0.0.1:8000/api
  test:
    host: 192.168.1.100
    db:
      host: 192.168.1.100
      port: 3306
      user: test_user
      password: test_pass
      database: test_db
    api_base_url: http://192.168.1.100:8000/api
  prod:
    host: prod.example.com
    db:
      host: prod-db.example.com
      port: 3306
      user: prod_user
      password: prod_pass
      database: prod_db
    api_base_url: https://api.example.com
```

**interface_info.yaml 格式：**
```yaml
interfaces:
  user:
    login:
      url: http://localhost:8080/api/login  # 会被自动替换为当前环境的API基础URL
      method: POST
      headers:
        Content-Type: application/json
      timeout: 30
      description: 用户登录接口

global:
  default_timeout: 30
  default_headers:
    User-Agent: PythonProject/1.0
    Accept: application/json
  retry_times: 3
  retry_interval: 1
```

**interface.ini 格式：**
```ini
[DATABASE]
host = localhost
user = your_user
password = your_password
database = your_database
```

#### 主要功能

1. **环境管理**
   - 自动识别当前环境
   - 支持多环境配置（dev/test/prod）
   - 环境间配置隔离

2. **URL自动替换**
   - 接口URL会根据当前环境自动替换基础地址
   - 例如：`http://localhost:8080/api/login` 在test环境会变成 `http://192.168.1.100:8000/api/login`

3. **配置合并**
   - 自动合并多个配置文件
   - 支持配置覆盖和扩展
   - 保持配置的层次结构

4. **类型安全**
   - 使用类型注解提高代码可读性
   - 支持IDE自动补全和类型检查

#### 便捷函数

```python
# 获取接口配置
from common.interface_config import get_interface_config
config = get_interface_config('user', 'login', 'test')

# 获取环境配置
from common.interface_config import get_env_config
env_config = get_env_config('prod')
```

#### 自定义配置文件列表

```python
# 只加载特定的配置文件
custom_config = InterfaceConfig([
    'conf/env.yaml',
    'conf/interface_info.yaml'
])

# 或者添加自定义配置文件
custom_config = InterfaceConfig([
    'conf/env.yaml',
    'conf/interface_info.yaml',
    'conf/custom_config.yaml'
])
```

### 传统配置方式

- **conf/env.yaml**：多环境信息（dev/test/prod），可通过common/config.py自动加载。
- **conf/interface.ini**：接口基础信息配置。
- **common/config.py**：自动加载conf下所有ini/yaml配置，支持多级key访问。

---

## HTTP工具类

### 概述

`HTTPUtils` 类提供了完整的HTTP请求功能，支持所有HTTP请求方法：GET、POST、DELETE、PUT、PATCH、HEAD、OPTIONS。

### 支持的HTTP方法

- **GET** - 获取资源
- **POST** - 创建资源
- **PUT** - 更新资源（完整替换）
- **DELETE** - 删除资源
- **PATCH** - 部分更新资源
- **HEAD** - 获取响应头信息
- **OPTIONS** - 获取支持的HTTP方法

### 使用方法

#### 1. 类方式使用（推荐）

```python
from utils.http_utils import HTTPUtils

# 创建HTTP工具实例
http_utils = HTTPUtils(base_url="https://api.example.com")

# 设置默认请求头
http_utils.set_default_headers({
    'Content-Type': 'application/json',
    'User-Agent': 'PythonProject/1.0'
})

# 设置认证token
http_utils.set_token("your_token_here")

try:
    # GET请求
    response = http_utils.get("/users", params={"page": 1, "limit": 10})
    print(f"GET响应: {response}")
    
    # POST请求（JSON数据）
    user_data = {"name": "John", "email": "john@example.com"}
    response = http_utils.post("/users", json_data=user_data)
    print(f"POST响应: {response}")
    
    # PUT请求
    update_data = {"name": "John Updated", "status": "active"}
    response = http_utils.put("/users/1", json_data=update_data)
    print(f"PUT响应: {response}")
    
    # DELETE请求
    response = http_utils.delete("/users/1")
    print(f"DELETE响应: {response}")
    
    # PATCH请求
    patch_data = {"status": "updated"}
    response = http_utils.patch("/users/1", json_data=patch_data)
    print(f"PATCH响应: {response}")
    
    # HEAD请求
    response = http_utils.head("/users")
    print(f"HEAD响应状态码: {response.status_code}")
    print(f"HEAD响应头: {dict(response.headers)}")
    
    # OPTIONS请求
    response = http_utils.options("/users")
    print(f"OPTIONS响应状态码: {response.status_code}")
    print(f"OPTIONS响应头: {dict(response.headers)}")
    
    # 通用请求方法
    response = http_utils.request("GET", "/users", params={"status": "active"})
    print(f"通用请求响应: {response}")
    
finally:
    # 清理会话
    http_utils.clear_session()
```

#### 2. 便捷函数使用

```python
from utils.http_utils import http_get, http_post, http_put, http_delete, http_patch, http_head, http_options

# GET请求
response = http_get("https://api.example.com/users", params={"page": 1})

# POST请求
user_data = {"name": "John", "email": "john@example.com"}
response = http_post("https://api.example.com/users", json_data=user_data)

# PUT请求
update_data = {"name": "John Updated"}
response = http_put("https://api.example.com/users/1", json_data=update_data)

# DELETE请求
response = http_delete("https://api.example.com/users/1")

# PATCH请求
patch_data = {"status": "active"}
response = http_patch("https://api.example.com/users/1", json_data=patch_data)

# HEAD请求
response = http_head("https://api.example.com/users")

# OPTIONS请求
response = http_options("https://api.example.com/users")
```

### 主要功能

1. **会话管理**
   - 自动维护HTTP会话
   - 支持会话级别的请求头和认证
   - 提供会话清理功能

2. **请求头管理**
   - 支持默认请求头设置
   - 支持动态添加认证token
   - 自动合并自定义请求头

3. **URL构建**
   - 支持基础URL配置
   - 自动处理相对路径和绝对路径
   - 智能URL拼接

4. **错误处理**
   - 自动抛出HTTP错误异常
   - 支持网络错误处理
   - 提供详细的错误信息

5. **日志记录**
   - 自动记录请求和响应信息
   - 支持调试级别的详细日志
   - 记录请求头、响应头等信息

### 与接口配置集成

```python
from common.interface_config import get_interface_config
from utils.http_utils import HTTPUtils

# 获取接口配置
interface_config = get_interface_config('user', 'login')

# 创建HTTP工具实例
http_utils = HTTPUtils(base_url=interface_config.get('base_url', ''))

# 发送请求
response = http_utils.post(
    interface_config['url'],
    json_data=interface_config.get('data'),
    headers=interface_config.get('headers'),
    timeout=interface_config.get('timeout', 30)
)
```

---

## 数据库操作工具

### 概述

`RequestDB` 类提供了完整的数据库操作功能，支持多种数据库类型和完整的CRUD操作。支持MySQL、PostgreSQL、Redis、SQLite等数据库。

### 支持的数据库类型

- **MySQL** - 关系型数据库
- **PostgreSQL** - 关系型数据库
- **Redis** - 键值对数据库
- **SQLite** - 轻量级关系型数据库

### 主要功能

1. **完整的CRUD操作**
   - **Create** - 创建数据
   - **Read** - 读取数据
   - **Update** - 更新数据
   - **Delete** - 删除数据

2. **数据库连接管理**
   - 自动连接管理
   - 连接池支持
   - 事务处理
   - 错误处理和回滚

3. **多数据库支持**
   - 统一的API接口
   - 数据库特定的优化
   - 自动SQL适配

4. **配置文件支持**
   - 从 `conf/database.yaml` 自动加载配置
   - 支持多环境配置（dev/test/prod）
   - 自动环境检测
   - 配置覆盖机制

### 配置文件

数据库连接配置存储在 `conf/database.yaml` 文件中：

```yaml
database:
  # 默认数据库类型
  default_type: mysql
  
  # MySQL数据库配置
  mysql:
    dev:
      host: 127.0.0.1
      port: 3306
      user: dev_user
      password: dev_pass
      database: dev_db
      charset: utf8mb4
      autocommit: true
    test:
      host: 192.168.1.100
      port: 3306
      user: test_user
      password: test_pass
      database: test_db
      charset: utf8mb4
      autocommit: true
    prod:
      host: prod-mysql.example.com
      port: 3306
      user: prod_user
      password: prod_pass
      database: prod_db
      charset: utf8mb4
      autocommit: true
  
  # PostgreSQL数据库配置
  postgresql:
    dev:
      host: 127.0.0.1
      port: 5432
      user: dev_user
      password: dev_pass
      database: dev_db
      autocommit: true
    test:
      host: 192.168.1.100
      port: 5432
      user: test_user
      password: test_pass
      database: test_db
      autocommit: true
    prod:
      host: prod-postgres.example.com
      port: 5432
      user: prod_user
      password: prod_pass
      database: prod_db
      autocommit: true
  
  # Redis数据库配置
  redis:
    dev:
      host: 127.0.0.1
      port: 6379
      password: null
      db: 0
    test:
      host: 192.168.1.100
      port: 6379
      password: test_redis_pass
      db: 1
    prod:
      host: prod-redis.example.com
      port: 6379
      password: prod_redis_pass
      db: 0
  
  # SQLite数据库配置
  sqlite:
    dev:
      database: dev.db
    test:
      database: test.db
    prod:
      database: prod.db
```

### 使用方法

#### 1. 从配置文件自动获取连接信息（推荐）

```python
from common.requestdb import RequestDB, get_db_connection

# 方式1：指定数据库类型和环境
db = get_db_connection('mysql', 'dev')
if db.connect():
    try:
        result = db.query("SELECT * FROM users")
        print(result)
    finally:
        db.disconnect()

# 方式2：只指定环境，使用默认数据库类型
db = RequestDB(env='test')
if db.connect():
    try:
        result = db.query("SELECT * FROM users")
        print(result)
    finally:
        db.disconnect()

# 方式3：只指定数据库类型，使用当前环境
db = RequestDB(db_type='sqlite')
if db.connect():
    try:
        result = db.query("SELECT * FROM users")
        print(result)
    finally:
        db.disconnect()
```

#### 2. 手动指定连接参数

```python
from common.requestdb import RequestDB

# 创建数据库连接
db = RequestDB('mysql', {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'password',
    'database': 'test_db'
})

# 连接数据库
if db.connect():
    try:
        # 执行CRUD操作
        # ...
    finally:
        # 断开连接
        db.disconnect()
```

#### 3. MySQL使用示例

```python
# MySQL配置
mysql_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'password',
    'database': 'test_db',
    'charset': 'utf8mb4'
}

# 创建MySQL连接
mysql_db = RequestDB('mysql', mysql_config)

if mysql_db.connect():
    try:
        # 查询操作 (Read)
        users = mysql_db.query("SELECT * FROM users WHERE status = %s", ('active',))
        print(f"查询结果: {users}")
        
        # 插入操作 (Create)
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 30,
            'status': 'active'
        }
        rows_affected = mysql_db.insert('users', user_data)
        print(f"插入行数: {rows_affected}")
        
        # 更新操作 (Update)
        update_data = {'status': 'inactive'}
        rows_affected = mysql_db.update('users', update_data, 'id = %s', (1,))
        print(f"更新行数: {rows_affected}")
        
        # 删除操作 (Delete)
        rows_affected = mysql_db.delete('users', 'id = %s', (1,))
        print(f"删除行数: {rows_affected}")
        
        # 执行原始SQL
        result = mysql_db.execute_raw_sql("SELECT COUNT(*) as count FROM users")
        print(f"用户总数: {result}")
        
    finally:
        mysql_db.disconnect()
```

#### 4. SQLite使用示例

```python
# SQLite配置
sqlite_config = {
    'database': 'test.db'
}

# 创建SQLite连接
sqlite_db = RequestDB('sqlite', sqlite_config)

if sqlite_db.connect():
    try:
        # 创建表
        sqlite_db.execute_raw_sql("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                age INTEGER
            )
        """)
        
        # 插入数据
        user_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'age': 25
        }
        rows_affected = sqlite_db.insert('users', user_data)
        print(f"插入行数: {rows_affected}")
        
        # 查询数据
        users = sqlite_db.query("SELECT * FROM users WHERE age > ?", (20,))
        print(f"查询结果: {users}")
        
    finally:
        sqlite_db.disconnect()
```

#### 5. Redis使用示例

```python
# Redis配置
redis_config = {
    'host': 'localhost',
    'port': 6379,
    'password': None,
    'db': 0
}

# 创建Redis连接
redis_db = RequestDB('redis', redis_config)

if redis_db.connect():
    try:
        # Redis插入操作
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': '30'
        }
        rows_affected = redis_db.insert('user:1', user_data)
        print(f"插入结果: {rows_affected}")
        
        # Redis更新操作
        update_data = {'age': '31'}
        rows_affected = redis_db.update('user:1', update_data, 'exists')
        print(f"更新结果: {rows_affected}")
        
        # Redis删除操作
        rows_affected = redis_db.delete('user:1', 'exists')
        print(f"删除结果: {rows_affected}")
        
    finally:
        redis_db.disconnect()
```

### 便捷函数

```python
from common.requestdb import create_db_connection, get_db_connection

# 使用便捷函数创建连接
mysql_db = create_db_connection('mysql', 
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='test_db'
)

if mysql_db.connect():
    try:
        result = mysql_db.query("SELECT * FROM users")
        print(result)
    finally:
        mysql_db.disconnect()

# 从配置文件获取连接
db = get_db_connection('mysql', 'dev')
if db.connect():
    try:
        result = db.query("SELECT * FROM users")
        print(result)
    finally:
        db.disconnect()
```

### 高级功能

#### 1. 事务处理

```python
# 事务处理示例
mysql_db = RequestDB('mysql', mysql_config)

if mysql_db.connect():
    try:
        # 开始事务
        mysql_db.db_connection.connection.begin()
        
        try:
            # 执行多个操作
            mysql_db.insert('users', {'name': 'User1', 'email': 'user1@example.com'})
            mysql_db.insert('users', {'name': 'User2', 'email': 'user2@example.com'})
            
            # 提交事务
            mysql_db.db_connection.connection.commit()
            print("事务提交成功")
            
        except Exception as e:
            # 回滚事务
            mysql_db.db_connection.connection.rollback()
            print(f"事务回滚: {e}")
            
    finally:
        mysql_db.disconnect()
```

#### 2. 复杂查询

```python
# 复杂查询示例
mysql_db = RequestDB('mysql', mysql_config)

if mysql_db.connect():
    try:
        # 联表查询
        sql = """
            SELECT u.name, u.email, o.order_id, o.total_amount
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE u.status = %s AND o.total_amount > %s
            ORDER BY o.total_amount DESC
        """
        result = mysql_db.query(sql, ('active', 100))
        print(f"联表查询结果: {result}")
        
        # 聚合查询
        sql = """
            SELECT 
                category,
                COUNT(*) as count,
                AVG(price) as avg_price,
                SUM(price) as total_amount
            FROM products
            GROUP BY category
            HAVING COUNT(*) > %s
        """
        result = mysql_db.query(sql, (5,))
        print(f"聚合查询结果: {result}")
        
    finally:
        mysql_db.disconnect()
```

### 与接口配置集成

```python
from common.interface_config import get_env_config
from common.requestdb import RequestDB

# 从环境配置获取数据库配置
env_config = get_env_config('dev')
db_config = env_config.get('db', {})

# 创建数据库连接
db = RequestDB('mysql', db_config)

if db.connect():
    try:
        # 执行数据库操作
        result = db.query("SELECT * FROM test_table")
        print(result)
    finally:
        db.disconnect()
```

### 配置优先级

1. **手动指定的连接参数** - 最高优先级
2. **配置文件中的环境配置** - 中等优先级
3. **配置文件中的默认配置** - 最低优先级（dev环境配置作为默认配置）

### 环境检测

- 自动从 `conf/env.yaml` 获取当前环境
- 支持手动指定环境参数
- 环境不存在时使用配置文件中的dev环境配置
- 如果dev环境不存在，使用第一个可用的环境配置
- 只有在配置文件完全不可用时才使用内置的fallback配置

### 配置来源

所有的数据库连接信息都来自 `conf/database.yaml` 配置文件：

- **默认配置**：使用配置文件中的dev环境配置
- **环境配置**：根据指定的环境（dev/test/prod）获取对应配置
- **fallback配置**：仅在配置文件不可用时使用内置的默认值

### 配置加载逻辑

1. **优先使用手动指定的连接参数**
2. **其次使用配置文件中的指定环境配置**
3. **再次使用配置文件中的dev环境配置作为默认配置**
4. **最后使用内置的fallback配置（仅在配置文件不可用时）** 

---

## 数据驱动测试

### 概述

项目支持自动加载 `caseparams` 目录下所有格式的文件作为数据驱动测试，支持多种文件格式和灵活的加载方式。

### 支持的文件格式

- **CSV** - 逗号分隔值文件
- **YAML/YML** - YAML格式文件
- **JSON** - JSON格式文件
- **Excel** - XLSX/XLS格式文件
- **TSV** - 制表符分隔值文件

### 使用方法

#### 1. 加载所有测试数据

```python
from common.get_caseparams import get_all_test_data

# 加载caseparams目录下所有文件的数据
all_data = get_all_test_data()

# 遍历所有文件的数据
for file_name, data in all_data.items():
    print(f"文件: {file_name}, 数据条数: {len(data)}")
    for case in data:
        # 处理每个测试用例
        case_id = case.get('case_id')
        description = case.get('description')
        url = case.get('url')
        method = case.get('method')
        params = case.get('params')
        expected = case.get('expected_result')
```

#### 2. 按文件类型加载数据

```python
from common.get_caseparams import (
    get_csv_test_data,
    get_yaml_test_data,
    get_json_test_data,
    get_excel_test_data
)

# 加载特定类型的文件数据
csv_data = get_csv_test_data()      # 所有CSV文件数据
yaml_data = get_yaml_test_data()    # 所有YAML文件数据
json_data = get_json_test_data()    # 所有JSON文件数据
excel_data = get_excel_test_data()  # 所有Excel文件数据
```

#### 3. 按类型加载特定格式数据

```python
from common.get_caseparams import load_caseparams_by_type

# 加载指定类型的所有文件数据
csv_data = load_caseparams_by_type('csv')
yaml_data = load_caseparams_by_type('yaml')
json_data = load_caseparams_by_type('json')
excel_data = load_caseparams_by_type('xlsx')
```

#### 4. 获取可用文件列表

```python
from common.get_caseparams import get_available_test_files

# 获取所有可用的测试文件路径
available_files = get_available_test_files()
for file_path in available_files:
    print(f"可用文件: {file_path}")
```

### 数据驱动测试示例

#### 方式1: 类方法数据驱动

```python
import pytest
from common.get_caseparams import get_all_test_data
from utils.http_utils import http_get, http_post

class TestDataDriven:
    def test_all_files_data_driven(self):
        """测试所有文件的数据驱动"""
        all_data = get_all_test_data()
        for file_name, data in all_data.items():
            for case in data:
                self._execute_test_case(case)
    
    def _execute_test_case(self, case):
        """执行单个测试用例"""
        url = case.get('url')
        method = case.get('method', 'GET').upper()
        params = case.get('params', {})
        
        if method == 'GET':
            resp = http_get(url, params=params)
        elif method == 'POST':
            resp = http_post(url, json_data=params)
        
        # 进行断言
        expected = case.get('expected_result', {})
        for k, v in expected.items():
            assert k in resp
            assert resp[k] == v
```

#### 方式2: pytest参数化数据驱动

```python
import pytest
from common.get_caseparams import load_caseparams_by_type

# 加载CSV数据用于参数化
csv_data = load_caseparams_by_type('csv')

@pytest.mark.parametrize("case", csv_data)
def test_csv_parameterized(case):
    """使用pytest参数化的CSV数据驱动测试"""
    url = case.get('url')
    method = case.get('method', 'GET').upper()
    params = case.get('params', {})
    
    if method == 'GET':
        resp = http_get(url, params=params)
    elif method == 'POST':
        resp = http_post(url, json_data=params)
    
    # 进行断言
    expected = case.get('expected_result', {})
    for k, v in expected.items():
        assert k in resp
        assert resp[k] == v
```

#### 方式3: 按文件分别测试

```python
from common.get_caseparams import get_all_test_data

def test_http_data_file():
    """测试HTTP数据文件"""
    all_data = get_all_test_data()
    http_data = all_data.get('test_http_data', [])
    
    for case in http_data:
        url = case.get('url')
        method = case.get('method', 'GET').upper()
        params = case.get('params', {})
        
        if method == 'GET':
            resp = http_get(url, params=params)
        elif method == 'POST':
            resp = http_post(url, json_data=params)
        
        # 进行断言
        expected = case.get('expected_result', {})
        for k, v in expected.items():
            assert k in resp
            assert resp[k] == v
```

### 文件格式要求

#### CSV格式
```csv
case_id,description,url,method,params,expected_result
1,测试GET请求,https://api.example.com/get,GET,"{""key"": ""value""}","{""status"": ""success""}"
2,测试POST请求,https://api.example.com/post,POST,"{""data"": ""test""}","{""id"": 1}"
```

#### YAML格式
```yaml
- case_id: 1
  description: 正常请求-简单问题
  url: http://localhost:8688/api/chatGatWay-internal
  method: POST
  params:
    message: 你好，今天天气怎么样？
    user_id: user001
  expected_result:
    code: 0
    msg: success
    data:
      reply: 今天天气晴朗，适合出行。

- case_id: 2
  description: 异常请求-缺少message参数
  url: http://localhost:8688/api/chatGatWay-internal
  method: POST
  params:
    user_id: user002
  expected_result:
    code: 400
    msg: 参数缺失: message
    data: {}
```

#### JSON格式
```json
[
  {
    "case_id": 1,
    "description": "测试用例1",
    "url": "https://api.example.com/test",
    "method": "GET",
    "params": {},
    "expected_result": {
      "status": "success"
    }
  }
]
```

### 主要功能

1. **自动文件发现** - 自动扫描 `caseparams` 目录下的所有支持格式文件
2. **多格式支持** - 支持CSV、YAML、JSON、Excel、TSV等多种格式
3. **灵活加载** - 支持按类型加载、按文件加载、全部加载等多种方式
4. **错误处理** - 提供详细的错误信息和加载状态反馈
5. **路径解析** - 自动处理相对路径和绝对路径解析

### 便捷函数

- `get_all_test_data()` - 获取所有测试数据
- `get_csv_test_data()` - 获取所有CSV测试数据
- `get_yaml_test_data()` - 获取所有YAML测试数据
- `get_json_test_data()` - 获取所有JSON测试数据
- `get_excel_test_data()` - 获取所有Excel测试数据
- `load_caseparams_by_type(file_type)` - 按类型加载测试数据
- `get_available_test_files()` - 获取所有可用测试文件 

---

## JSON文件读取工具

### 概述

项目提供了强大的JSON文件读取工具，支持加载、解析、读取JSON文件，包括多层嵌套结构。该工具提供了完整的JSON操作功能，包括路径查询、数据修改、搜索、验证等。

### 主要功能

1. **多层嵌套支持** - 支持任意深度的JSON嵌套结构
2. **路径查询** - 支持点号分隔和数组索引的路径查询
3. **数据修改** - 支持设置、删除JSON中的值
4. **搜索功能** - 支持在JSON中搜索指定键的所有值
5. **结构分析** - 获取JSON结构信息
6. **Schema验证** - 验证JSON数据是否符合指定schema
7. **文件操作** - 支持读取、写入、合并JSON文件

### 使用方法

#### 1. 基本使用

```python
from utils.read_jsonfile_utils import JSONFileReader

# 创建JSON读取器
reader = JSONFileReader("config.json")

# 获取完整数据
data = reader.get_data()

# 根据路径获取值
username = reader.get_value("user.name")
age = reader.get_value("user.profile.age")
first_item = reader.get_value("items[0]")
nested_value = reader.get_value("user.addresses[0].city")
```

#### 2. 路径查询语法

支持多种路径查询语法：

```python
# 对象属性访问
reader.get_value("user.name")                    # 访问user对象的name属性

# 数组索引访问
reader.get_value("users[0]")                    # 访问users数组的第一个元素
reader.get_value("users[0].profile.age")        # 访问嵌套结构

# 混合路径
reader.get_value("data.items[1].properties.name")  # 复杂嵌套路径
```

#### 3. 数据修改

```python
# 设置值
reader.set_value("user.phone", "13800138000")
reader.set_value("settings.theme", "dark")
reader.set_value("users[0].profile.email", "new@example.com")

# 删除值
reader.delete_value("user.phone")
reader.delete_value("users[0].profile.email")

# 保存修改
reader.save_file("updated_config.json")
```

#### 4. 搜索功能

```python
# 搜索所有名为"city"的字段
city_results = reader.search_values("city")
for path, value in city_results:
    print(f"找到 {path}: {value}")

# 搜索所有名为"theme"的字段
theme_results = reader.search_values("theme")
for path, value in theme_results:
    print(f"找到 {path}: {value}")
```

#### 5. 结构分析

```python
# 获取JSON结构信息
structure = reader.get_structure(max_depth=3)
print(f"JSON结构: {structure}")

# 结构信息包含：
# - type: 数据类型 (dict, list, string, number, boolean)
# - keys: 对象的键列表
# - length: 数组的长度
# - children: 子结构信息
```

#### 6. Schema验证

```python
# 定义schema
schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "name": {"type": "string"}
            },
            "required": ["id", "name"]
        }
    }
}

# 验证数据
is_valid, errors = reader.validate_schema(schema)
if not is_valid:
    for error in errors:
        print(f"验证错误: {error}")
```

#### 7. 从字符串加载

```python
# 从字符串加载JSON
json_string = '{"name": "张三", "age": 25}'
reader = JSONFileReader()
reader.load_string(json_string)

# 获取值
name = reader.get_value("name")  # "张三"
age = reader.get_value("age")    # 25
```

### 便捷函数

#### 基本操作

```python
from utils.read_jsonfile_utils import (
    read_json_file,
    get_json_value,
    write_json_file,
    merge_json_files
)

# 读取JSON文件
data = read_json_file("config.json")

# 获取指定路径的值
value = get_json_value("config.json", "user.name", default="默认值")

# 写入JSON文件
write_json_file("output.json", data, indent=2)

# 合并多个JSON文件
merge_json_files(["file1.json", "file2.json"], "merged.json")
```

### 复杂示例

```python
from utils.read_jsonfile_utils import JSONFileReader

# 复杂的JSON数据结构
complex_data = {
    "users": [
        {
            "id": 1,
            "name": "张三",
            "profile": {
                "age": 25,
                "email": "zhangsan@example.com",
                "addresses": [
                    {"type": "home", "city": "北京"},
                    {"type": "work", "city": "上海"}
                ],
                "preferences": {
                    "theme": "dark",
                    "language": "zh-CN"
                }
            }
        }
    ],
    "settings": {
        "app": {
            "version": "1.0.0",
            "debug": True
        }
    }
}

# 创建读取器
reader = JSONFileReader()
reader.load_string(json.dumps(complex_data))

# 复杂路径查询
first_user_name = reader.get_value("users[0].name")                    # "张三"
first_user_age = reader.get_value("users[0].profile.age")              # 25
first_address = reader.get_value("users[0].profile.addresses[0]")      # {"type": "home", "city": "北京"}
theme = reader.get_value("users[0].profile.preferences.theme")         # "dark"
app_version = reader.get_value("settings.app.version")                 # "1.0.0"

# 搜索所有城市
city_results = reader.search_values("city")
# 结果: [("users[0].profile.addresses[0].city", "北京"), ("users[0].profile.addresses[1].city", "上海")]

# 设置新值
reader.set_value("users[0].profile.phone", "13800138000")
reader.set_value("settings.app.new_feature", True)

# 获取结构信息
structure = reader.get_structure(max_depth=2)
```

### 错误处理

工具提供了完善的错误处理机制：

```python
# 文件不存在
reader = JSONFileReader("nonexistent.json")
# 输出: [ERROR] 文件不存在: nonexistent.json

# JSON格式错误
reader.load_string('{"invalid": json}')
# 输出: [ERROR] JSON字符串格式错误: Expecting ',' delimiter

# 路径不存在
value = reader.get_value("nonexistent.path", default="默认值")
# 返回: "默认值"

# 数组越界
value = reader.get_value("users[999].name", default="默认值")
# 返回: "默认值"
```

### 性能优化

- **延迟加载** - 只有在需要时才加载文件
- **路径缓存** - 解析过的路径会被缓存以提高性能
- **内存优化** - 支持大文件的分块处理
- **错误恢复** - 提供默认值和错误恢复机制

### 主要特性

1. **类型安全** - 使用类型提示确保代码质量
2. **错误处理** - 完善的异常处理和错误信息
3. **日志记录** - 详细的操作日志
4. **编码支持** - 支持多种文件编码
5. **Unicode支持** - 完整支持中文字符
6. **向后兼容** - 保持与原有API的兼容性 