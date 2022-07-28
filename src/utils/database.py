from tortoise import Tortoise

from .config import config
from .log import logger


async def database_init():
    '''
    初始化建表
    '''
    logger.debug('正在注册数据库')
    database_path = f"./db/data.db"
    db_url = f'sqlite://{database_path}'
    # 这里填要加载的表
    models = [
        'src.modules.group_info',
        'src.modules.user_info',
        'src.modules.user_attr',
        # 'src.plugins.ruassian_roulette.module'
    ]
    modules = {"models": models}
    await Tortoise.init(db_url=db_url, modules=modules)
    await Tortoise.generate_schemas()
    logger.info('<g>数据库初始化成功。</g>')


async def database_close():
    # 关闭数据库连接
    logger.debug(f'<g>正在断开数据库。</g>')
    await Tortoise.close_connections()
    logger.info(f'<g>数据库断开成功</g>')

