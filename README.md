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

---

## MQ消息队列工具

### 概述

项目提供了完整的MQ（消息队列）工具，支持RabbitMQ和RocketMQ的消息发送和消费。该工具支持从配置文件加载MQ配置信息，并提供统一的消息发送和消费接口。

### 支持的消息队列

1. **RabbitMQ** - 支持交换机、队列、绑定等完整功能
2. **RocketMQ** - 支持主题、标签、消费者组等功能

### 配置文件

MQ配置信息存储在 `conf/mq.yaml` 文件中，支持多环境配置：

```yaml
mq:
  default_type: rabbitmq
  
  rabbitmq:
    dev:
      host: localhost
      port: 5672
      username: guest
      password: guest
      virtual_host: /
      exchanges:
        test_exchange:
          name: test_exchange
          type: direct
          durable: true
      queues:
        test_queue:
          name: test_queue
          durable: true
      bindings:
        test_binding:
          exchange: test_exchange
          queue: test_queue
          routing_key: test_key
  
  rocketmq:
    dev:
      name_server: localhost:9876
      producer_group: test_producer_group
      consumer_group: test_consumer_group
      producer:
        send_msg_timeout: 3000
      consumer:
        topics:
          test_topic:
            name: test_topic
            tags: ["test_tag"]
```

### 使用方法

#### 1. 基本使用

```python
from common.mq_utils import MQManager
import json

# 创建MQ管理器
manager = MQManager(env='dev')

# 发送RabbitMQ消息
message = json.dumps({"id": 1, "content": "测试消息"})
success = manager.send_message('rabbitmq', message, 
                            exchange='test_exchange', routing_key='test_key')

# 发送RocketMQ消息
success = manager.send_message('rocketmq', message, 
                            topic='test_topic', tags='test_tag')
```

#### 2. RabbitMQ操作

```python
from common.mq_utils import RabbitMQConnection, MQManager

# 获取RabbitMQ连接
manager = MQManager()
connection = manager.get_connection('rabbitmq')

if connection.connect():
    # 声明交换机
    connection.declare_exchange('test_exchange', 'direct')
    
    # 声明队列
    connection.declare_queue('test_queue')
    
    # 绑定队列到交换机
    connection.bind_queue('test_queue', 'test_exchange', 'test_key')
    
    # 发送消息
    message = json.dumps({"content": "RabbitMQ测试消息"})
    connection.publish_message('test_exchange', 'test_key', message)
    
    # 消费消息
    def callback(ch, method, properties, body):
        print(f"收到消息: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    connection.consume_message('test_queue', callback)
    
    # 断开连接
    connection.disconnect()
```

#### 3. RocketMQ操作

```python
from common.mq_utils import RocketMQConnection, MQManager

# 获取RocketMQ连接
manager = MQManager()
connection = manager.get_connection('rocketmq')

if connection.connect():
    # 发送消息
    message = json.dumps({"content": "RocketMQ测试消息"})
    connection.send_message('test_topic', message, 'test_tag')
    
    # 消费消息
    def callback(msg):
        print(f"收到消息: {msg.body.decode()}")
        return True  # 消费成功
    
    connection.start_consumer('test_topic', callback, tags='test_tag')
    
    # 断开连接
    connection.disconnect()
```

#### 4. 便捷函数

```python
from common.mq_utils import (
    send_rabbitmq_message,
    send_rocketmq_message,
    consume_rabbitmq_message,
    consume_rocketmq_message
)

# 发送消息
message = json.dumps({"content": "便捷函数测试"})

# RabbitMQ
send_rabbitmq_message(message, 'test_exchange', 'test_key')

# RocketMQ
send_rocketmq_message(message, 'test_topic', 'test_tag')

# 消费消息
def rabbitmq_callback(ch, method, properties, body):
    print(f"RabbitMQ消息: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def rocketmq_callback(msg):
    print(f"RocketMQ消息: {msg.body.decode()}")
    return True

consume_rabbitmq_message(rabbitmq_callback, 'test_queue')
consume_rocketmq_message(rocketmq_callback, 'test_topic')
```

### 高级功能

#### 1. 多环境支持

```python
# 开发环境
manager = MQManager(env='dev')

# 测试环境
manager = MQManager(env='test')

# 生产环境
manager = MQManager(env='prod')
```

#### 2. 消息属性设置

```python
# RabbitMQ消息属性
properties = {
    'delivery_mode': 2,  # 持久化消息
    'content_type': 'application/json',
    'headers': {'custom_header': 'value'}
}

connection.publish_message('exchange', 'routing_key', message, properties)

# RocketMQ消息属性
connection.send_message('topic', message, 'tag', 'key', delay_level=1)
```

#### 3. 批量操作

```python
# 批量发送消息
messages = [
    {"id": 1, "content": "消息1"},
    {"id": 2, "content": "消息2"},
    {"id": 3, "content": "消息3"}
]

for msg in messages:
    message = json.dumps(msg)
    manager.send_message('rabbitmq', message, 
                       exchange='test_exchange', routing_key='test_key')
```

#### 4. 错误处理

```python
try:
    success = manager.send_message('rabbitmq', message)
    if not success:
        print("消息发送失败")
except Exception as e:
    print(f"发送消息时发生错误: {e}")
```

### 配置说明

#### RabbitMQ配置

```yaml
rabbitmq:
  dev:
    host: localhost              # 主机地址
    port: 5672                   # 端口
    username: guest              # 用户名
    password: guest              # 密码
    virtual_host: /              # 虚拟主机
    connection_timeout: 30       # 连接超时
    heartbeat_interval: 600      # 心跳间隔
    exchanges:                   # 交换机配置
      test_exchange:
        name: test_exchange
        type: direct             # 类型: direct, fanout, topic
        durable: true
        auto_delete: false
    queues:                      # 队列配置
      test_queue:
        name: test_queue
        durable: true
        auto_delete: false
        arguments: {}
    bindings:                    # 绑定关系
      test_binding:
        exchange: test_exchange
        queue: test_queue
        routing_key: test_key
```

#### RocketMQ配置

```yaml
rocketmq:
  dev:
    name_server: localhost:9876  # 名称服务器
    producer_group: test_producer_group    # 生产者组
    consumer_group: test_consumer_group    # 消费者组
    producer:                    # 生产者配置
      send_msg_timeout: 3000    # 发送超时
      retry_times_when_send_failed: 2     # 发送失败重试次数
      max_message_size: 4194304 # 最大消息大小
    consumer:                    # 消费者配置
      pull_batch_size: 32       # 拉取批次大小
      pull_interval: 0          # 拉取间隔
      topics:                   # 订阅主题
        test_topic:
          name: test_topic
          tags: ["test_tag"]
          sub_expression: "*"
```

### 测试消息发送和消费

#### 1. 发送测试消息

```python
from common.mq_utils import MQManager
import json

# 创建测试消息
test_message = json.dumps({
    "id": 1,
    "content": "测试消息",
    "timestamp": time.time(),
    "type": "test"
})

# 发送到RabbitMQ
manager = MQManager()
success = manager.send_message('rabbitmq', test_message, 
                            exchange='test_exchange', routing_key='test_key')

# 发送到RocketMQ
success = manager.send_message('rocketmq', test_message, 
                            topic='test_topic', tags='test_tag')
```

#### 2. 消费测试消息

```python
# RabbitMQ消费
def rabbitmq_handler(ch, method, properties, body):
    try:
        message = json.loads(body.decode('utf-8'))
        print(f"收到RabbitMQ消息: {message}")
        # 处理消息逻辑
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"处理消息失败: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

# RocketMQ消费
def rocketmq_handler(msg):
    try:
        message = msg.body.decode('utf-8')
        print(f"收到RocketMQ消息: {message}")
        # 处理消息逻辑
        return True  # 消费成功
    except Exception as e:
        print(f"处理消息失败: {e}")
        return False  # 消费失败

# 启动消费者
manager.consume_message('rabbitmq', rabbitmq_handler, queue='test_queue')
manager.consume_message('rocketmq', rocketmq_handler, topic='test_topic')
```

### 主要特性

1. **多MQ支持** - 支持RabbitMQ和RocketMQ
2. **配置驱动** - 从配置文件加载MQ配置
3. **多环境支持** - 支持dev、test、prod环境
4. **统一接口** - 提供统一的消息发送和消费接口
5. **错误处理** - 完善的错误处理和重试机制
6. **连接管理** - 自动管理连接池和连接状态
7. **消息持久化** - 支持消息持久化和可靠性投递

### 依赖安装

```bash
# 安装RabbitMQ驱动
pip install pika

# 安装RocketMQ驱动
pip install rocketmq-client-python
```

### 注意事项

1. **服务可用性** - 确保RabbitMQ或RocketMQ服务正在运行
2. **网络连接** - 确保网络连接正常，防火墙允许相应端口
3. **权限配置** - 确保用户有相应的读写权限
4. **资源清理** - 使用完毕后及时断开连接
5. **错误处理** - 在生产环境中需要完善的错误处理机制 

---

## API监控功能

### 概述

项目提供了完整的API监控功能，自动记录所有API请求和响应信息到 `api_monitor.log` 文件。该功能可以帮助开发者监控API性能、调试问题、分析请求模式。

### 为什么api_monitor.log是空的

之前 `api_monitor.log` 文件为空的原因是：

1. **日志函数未被调用** - 只有 `api_info()` 和 `api_error()` 函数才会写入 `api_monitor.log`
2. **测试用例使用普通日志** - 当前的测试用例使用的是 `info()` 和 `error()` 函数，这些写入到 `log.log`
3. **缺少自动监控** - 没有自动监控机制来记录所有API请求

### 解决方案

现在项目已经实现了完整的API监控功能：

1. **HTTP工具类集成** - 所有HTTP请求都会自动记录到 `api_monitor.log`
2. **API监控装饰器** - 提供装饰器来自动监控函数调用
3. **直接日志记录** - 可以直接使用 `api_info()` 和 `api_error()` 函数

### 功能特性

1. **自动监控** - 所有HTTP请求自动记录
2. **详细信息** - 记录请求URL、方法、参数、响应时间、状态码等
3. **错误追踪** - 记录请求失败的原因和错误信息
4. **性能统计** - 提供请求统计和性能分析
5. **JSON格式** - 日志以JSON格式记录，便于解析和分析

### 使用方法

#### 1. 自动监控（推荐）

所有使用 `utils.http_utils` 中的HTTP函数都会自动记录到 `api_monitor.log`：

```python
from utils.http_utils import http_get, http_post

# 这些请求会自动记录到 api_monitor.log
response1 = http_get("https://api.example.com/users")
response2 = http_post("https://api.example.com/users", json_data={"name": "张三"})
```

#### 2. 使用API监控装饰器

```python
from common.api_monitor import api_monitor, http_monitor

# 监控普通函数
@api_monitor
def my_api_function():
    # 函数逻辑
    return {"status": "success"}

# 监控HTTP请求
@http_monitor(url="https://api.example.com/test", method="GET")
def my_http_request():
    # HTTP请求逻辑
    return {"status": "success"}
```

#### 3. 直接记录API日志

```python
from common.log import api_info, api_error

# 记录API信息
api_info("API请求开始: GET /api/users")
api_info("API响应成功: 200 OK")

# 记录API错误
api_error("API请求失败: 连接超时")
api_error("API响应错误: 500 Internal Server Error")
```

#### 4. 使用API监控类

```python
from common.api_monitor import APIMonitor

# 创建监控实例
monitor = APIMonitor()

# 记录请求
monitor.record_request(
    url="https://api.example.com/users",
    method="GET",
    params={"id": 1},
    response={"status": "success"},
    execution_time=0.1
)

# 获取统计信息
stats = monitor.get_statistics()
print(f"请求统计: {stats}")
```

### 日志格式

#### HTTP请求日志

```json
{
  "timestamp": 1753890765.9612596,
  "method": "GET",
  "url": "https://jsonplaceholder.typicode.com/posts/1",
  "params": {},
  "json_data": {},
  "headers": {}
}
```

#### HTTP响应日志

```json
{
  "timestamp": 1753890769.8178039,
  "method": "GET",
  "url": "https://jsonplaceholder.typicode.com/posts/1",
  "status_code": 200,
  "execution_time_ms": 3856.54,
  "response_size": 292,
  "status": "success"
}
```

#### API监控记录

```json
{
  "timestamp": 1753890781.292537,
  "url": "https://api.example.com/test",
  "method": "GET",
  "params": {"id": 1},
  "status": "success",
  "execution_time_ms": 100.0,
  "request_count": 1,
  "success_count": 1,
  "error_count": 0,
  "avg_time_ms": 100.0,
  "response_size": 21
}
```

### 监控内容

#### 请求信息
- **URL** - 请求地址
- **方法** - HTTP方法（GET、POST、PUT、DELETE等）
- **参数** - 查询参数和请求体
- **请求头** - HTTP请求头（排除敏感信息）
- **时间戳** - 请求开始时间

#### 响应信息
- **状态码** - HTTP响应状态码
- **响应大小** - 响应内容大小
- **执行时间** - 请求执行时间（毫秒）
- **响应内容** - 响应数据（可选）

#### 错误信息
- **错误类型** - 异常类型
- **错误消息** - 详细错误信息
- **错误堆栈** - 错误堆栈信息（可选）

### 性能统计

API监控类提供以下统计信息：

```python
{
  "total_requests": 10,           # 总请求数
  "success_requests": 8,          # 成功请求数
  "error_requests": 2,            # 失败请求数
  "success_rate": 80.0,           # 成功率（百分比）
  "avg_execution_time_ms": 150.5, # 平均执行时间（毫秒）
  "total_execution_time_ms": 1505.0 # 总执行时间（毫秒）
}
```

### 日志文件管理

- **文件位置** - `log/api_monitor.log`
- **轮转策略** - 每天轮转，保留7天
- **编码格式** - UTF-8
- **日志级别** - INFO和ERROR

### 配置说明

API监控功能通过以下方式配置：

1. **日志配置** - 在 `common/log.py` 中配置
2. **监控装饰器** - 在 `common/api_monitor.py` 中定义
3. **HTTP工具集成** - 在 `utils/http_utils.py` 中集成

### 使用建议

1. **生产环境** - 建议启用API监控来追踪性能问题
2. **开发环境** - 可以详细记录所有API请求用于调试
3. **测试环境** - 记录测试过程中的API调用用于分析
4. **日志分析** - 可以使用工具分析JSON格式的日志文件 