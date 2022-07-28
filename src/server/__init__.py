from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot
from src.utils.log import logger
from . import data_source as source

driver = get_driver()

@driver.on_bot_connect
async def _(bot: Bot):
    logger.debug(f"<g> Bot:{bot.self_id} 连接成功,正在注册... </>")
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id: int = group['group_id']
        group_name: str = group['group_name']
        # 注册群信息
        await source.group_init(group_id, group_name)
        # 注册插件
        await source.load_plugins(group_id)
        # 注册成员信息
        member_list = await bot.get_group_member_list(group_id=group_id)
        for one_member in member_list:
            user_id = one_member['user_id']
            await source.user_init(user_id)
    logger.info(
        f"<y>Bot {bot.self_id}</y> 注册完毕。"
    )