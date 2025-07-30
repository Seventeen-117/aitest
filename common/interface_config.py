from common.yaml_utils import load_yaml
from common.config import get_config
import os
import configparser
from typing import Dict, List, Any, Optional

class InterfaceConfig:
    """
    接口配置管理工具
    用于读取和管理接口基本信息，支持多配置文件加载
    """
    
    def __init__(self, config_files: Optional[List[str]] = None):
        """
        初始化接口配置
        :param config_files: 配置文件路径列表，支持yaml和ini格式
        """
        if config_files is None:
            # 默认配置文件列表
            config_files = [
                'conf/env.yaml',
                'conf/interface_info.yaml',
                'conf/interface.ini'
            ]
        
        self.config_files = config_files
        self.interface_config = {}
        self.env_config = {}
        self.database_config = {}
        
        # 按优先级加载配置文件
        self._load_all_configs()
    
    def _load_all_configs(self):
        """
        按优先级加载所有配置文件
        优先级：env.yaml > interface_info.yaml > interface.ini
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        for config_file in self.config_files:
            config_path = os.path.join(base_dir, config_file)
            if os.path.exists(config_path):
                self._load_single_config(config_path)
            else:
                print(f"警告: 配置文件不存在: {config_path}")
    
    def _load_single_config(self, config_path: str):
        """
        加载单个配置文件
        :param config_path: 配置文件路径
        """
        try:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                self._load_yaml_config(config_path)
            elif config_path.endswith('.ini'):
                self._load_ini_config(config_path)
            else:
                print(f"警告: 不支持的配置文件格式: {config_path}")
        except Exception as e:
            print(f"加载配置文件失败 {config_path}: {e}")
    
    def _load_yaml_config(self, config_path: str):
        """
        加载YAML配置文件
        :param config_path: YAML配置文件路径
        """
        config_data = load_yaml(config_path)
        
        if 'env' in config_data:
            # 环境配置文件
            self.env_config.update(config_data['env'])
        elif 'interfaces' in config_data:
            # 接口配置文件
            self._merge_interface_config(config_data)
        else:
            # 其他YAML配置，直接合并到interface_config
            self._merge_config(self.interface_config, config_data)
    
    def _load_ini_config(self, config_path: str):
        """
        加载INI配置文件
        :param config_path: INI配置文件路径
        """
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        # 将INI配置转换为字典格式
        ini_dict = {}
        for section in config.sections():
            ini_dict[section] = dict(config[section])
        
        # 合并到interface_config
        self._merge_config(self.interface_config, ini_dict)
    
    def _merge_interface_config(self, new_config: Dict):
        """
        合并接口配置
        :param new_config: 新的配置数据
        """
        if 'interfaces' in new_config:
            if 'interfaces' not in self.interface_config:
                self.interface_config['interfaces'] = {}
            
            # 合并接口配置
            for module, interfaces in new_config['interfaces'].items():
                if module not in self.interface_config['interfaces']:
                    self.interface_config['interfaces'][module] = {}
                
                for interface, config in interfaces.items():
                    self.interface_config['interfaces'][module][interface] = config
        
        # 合并全局配置
        if 'global' in new_config:
            if 'global' not in self.interface_config:
                self.interface_config['global'] = {}
            self._merge_config(self.interface_config['global'], new_config['global'])
    
    def _merge_config(self, target: Dict, source: Dict):
        """
        递归合并配置字典
        :param target: 目标配置
        :param source: 源配置
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_config(target[key], value)
            else:
                target[key] = value
    
    def get_current_env(self) -> str:
        """
        获取当前环境
        :return: 当前环境名称
        """
        return self.env_config.get('current', 'dev')
    
    def get_env_config(self, env: Optional[str] = None) -> Dict:
        """
        获取环境配置
        :param env: 环境名称，默认为当前环境
        :return: 环境配置信息
        """
        if env is None:
            env = self.get_current_env()
        return self.env_config.get(env, {})
    
    def get_api_base_url(self, env: Optional[str] = None) -> str:
        """
        获取API基础URL
        :param env: 环境名称，默认为当前环境
        :return: API基础URL
        """
        env_config = self.get_env_config(env)
        return env_config.get('api_base_url', 'http://localhost:8080')
    
    def get_database_config(self, env: Optional[str] = None) -> Dict:
        """
        获取数据库配置
        :param env: 环境名称，默认为当前环境
        :return: 数据库配置信息
        """
        env_config = self.get_env_config(env)
        return env_config.get('db', {})
    
    def get_interface_info(self, module: str, interface: str, env: Optional[str] = None) -> Dict:
        """
        获取指定接口的基本信息
        :param module: 模块名（如 user, order, product）
        :param interface: 接口名（如 login, get_user_info）
        :param env: 环境名称，默认为当前环境
        :return: 接口配置信息
        """
        try:
            interface_info = self.interface_config['interfaces'][module][interface].copy()
            
            # 合并全局配置
            global_config = self.interface_config.get('global', {})
            
            # 合并默认headers
            if 'headers' not in interface_info:
                interface_info['headers'] = {}
            interface_info['headers'].update(global_config.get('default_headers', {}))
            
            # 设置默认timeout
            if 'timeout' not in interface_info:
                interface_info['timeout'] = global_config.get('default_timeout', 30)
            
            # 根据环境替换URL中的基础地址
            if 'url' in interface_info:
                api_base_url = self.get_api_base_url(env)
                if interface_info['url'].startswith('http://localhost:8080'):
                    # 替换为当前环境的基础URL
                    interface_info['url'] = interface_info['url'].replace(
                        'http://localhost:8080', 
                        api_base_url
                    )
            
            return interface_info
        except KeyError as e:
            raise ValueError(f"接口配置不存在: {module}.{interface}")
        except Exception as e:
            raise Exception(f"获取接口配置失败: {e}")
    
    def get_all_interfaces(self) -> Dict:
        """
        获取所有接口信息
        :return: 所有接口配置字典
        """
        return self.interface_config.get('interfaces', {})
    
    def get_module_interfaces(self, module: str) -> Dict:
        """
        获取指定模块的所有接口
        :param module: 模块名
        :return: 模块下的所有接口配置
        """
        try:
            return self.interface_config['interfaces'][module]
        except KeyError:
            raise ValueError(f"模块不存在: {module}")
    
    def get_global_config(self) -> Dict:
        """
        获取全局配置
        :return: 全局配置信息
        """
        return self.interface_config.get('global', {})
    
    def get_all_configs(self) -> Dict:
        """
        获取所有配置信息
        :return: 所有配置信息
        """
        return {
            'interface_config': self.interface_config,
            'env_config': self.env_config,
            'current_env': self.get_current_env()
        }

# 便捷函数
def get_interface_config(module: str, interface: str, env: Optional[str] = None) -> Dict:
    """
    便捷函数：获取接口配置
    :param module: 模块名
    :param interface: 接口名
    :param env: 环境名称
    :return: 接口配置信息
    """
    config = InterfaceConfig()
    return config.get_interface_info(module, interface, env)

def get_env_config(env: Optional[str] = None) -> Dict:
    """
    便捷函数：获取环境配置
    :param env: 环境名称
    :return: 环境配置信息
    """
    config = InterfaceConfig()
    return config.get_env_config(env)

# 示例用法
if __name__ == "__main__":
    # 创建配置实例
    config = InterfaceConfig()
    
    # 获取当前环境
    current_env = config.get_current_env()
    print(f"当前环境: {current_env}")
    
    # 获取环境配置
    env_config = config.get_env_config()
    print(f"环境配置: {env_config}")
    
    # 获取API基础URL
    api_base_url = config.get_api_base_url()
    print(f"API基础URL: {api_base_url}")
    
    # 获取登录接口配置（会根据当前环境自动替换URL）
    login_config = get_interface_config('user', 'login')
    print(f"登录接口配置: {login_config}")
    
    # 获取所有接口
    all_interfaces = config.get_all_interfaces()
    print(f"所有接口模块: {list(all_interfaces.keys())}")
    
    # 获取所有配置信息
    all_configs = config.get_all_configs()
    print(f"所有配置信息: {all_configs}") 