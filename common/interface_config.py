from common.yaml_utils import load_yaml
from common.config import get_config
import os

class InterfaceConfig:
    """
    接口配置管理工具
    用于读取和管理接口基本信息
    """
    
    def __init__(self, config_file='conf/interface_info.yaml'):
        """
        初始化接口配置
        :param config_file: 接口配置文件路径
        """
        self.config_file = config_file
        self.interface_config = self._load_interface_config()
    
    def _load_interface_config(self):
        """
        加载接口配置文件
        """
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, self.config_file)
            return load_yaml(config_path)
        except Exception as e:
            print(f"加载接口配置文件失败: {e}")
            return {}
    
    def get_interface_info(self, module, interface):
        """
        获取指定接口的基本信息
        :param module: 模块名（如 user, order, product）
        :param interface: 接口名（如 login, get_user_info）
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
            
            return interface_info
        except KeyError as e:
            raise ValueError(f"接口配置不存在: {module}.{interface}")
        except Exception as e:
            raise Exception(f"获取接口配置失败: {e}")
    
    def get_all_interfaces(self):
        """
        获取所有接口信息
        :return: 所有接口配置字典
        """
        return self.interface_config.get('interfaces', {})
    
    def get_module_interfaces(self, module):
        """
        获取指定模块的所有接口
        :param module: 模块名
        :return: 模块下的所有接口配置
        """
        try:
            return self.interface_config['interfaces'][module]
        except KeyError:
            raise ValueError(f"模块不存在: {module}")
    
    def get_global_config(self):
        """
        获取全局配置
        :return: 全局配置信息
        """
        return self.interface_config.get('global', {})

# 使用示例
def get_interface_config(module, interface):
    """
    便捷函数：获取接口配置
    :param module: 模块名
    :param interface: 接口名
    :return: 接口配置信息
    """
    config = InterfaceConfig()
    return config.get_interface_info(module, interface)

# 示例用法
if __name__ == "__main__":
    # 获取登录接口配置
    login_config = get_interface_config('user', 'login')
    print(f"登录接口配置: {login_config}")
    
    # 获取所有接口
    config = InterfaceConfig()
    all_interfaces = config.get_all_interfaces()
    print(f"所有接口: {list(all_interfaces.keys())}") 