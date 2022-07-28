from pathlib import Path
from typing import Dict, List, Union,Optional

import yaml

SYSTEM_PROXY: Optional[str] = None  # 全局代理

class Config():
    '''配置文件类'''

    nickname: List[str]
    """昵称"""
    bot_path: str
    """路径"""
    admin_number: str
    """管理员账户"""

    main_group: str
    """主群群号"""

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(Config, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __getattr__(self, item) -> Dict[str, Union[str, int, bool]]:
        '''获取配置'''
        value = self._config.get(item)
        if value:
            return value
        raise AttributeError("未找到该配置字段，请检查config.yml文件！")

    def __init__(self):
        '''初始化'''
        workdir = Path.cwd()
        config_file = workdir / "config.yml"
        with open(config_file, 'r', encoding='utf-8') as f:
            cfg = f.read()
            self._config: dict = yaml.load(cfg, Loader=yaml.FullLoader)


config = Config()
"""
配置文件模块，用于读取项目内的config.yml文件配置内容
使用方法:
```
from src.utils.config import config
>>>config.your_config_key
```
"""
