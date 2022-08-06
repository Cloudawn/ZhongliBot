from typing import Dict, List

from nonebot import export, on_command, on_fullmatch
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from src.utils.log import logger
from src.utils.scheduler import the_scheduler

from .individual import money as money
from .multiplayer import russian as russian
from .multiplayer import shot as shot
from .utils import GAMBLER, GAMBLER_GROUP, GAMBLER_SELF, scheduler

Export = export()
Export.plugin_name = "俄罗斯轮盘"
Export.plugin_command = "单人模式 | 多人模式"
Export.plugin_usage = "娱乐插件，和钟离对赌"
Export.default_status = True

remake = on_fullmatch("重置轮盘", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@scheduler.scheduled_job("cron", hour=0, minute=2)
async def _():
    try:
        '''每天零点重置俄罗斯轮盘数据'''
        logger.info("正在重置俄罗斯轮盘数据")
        GAMBLER_SELF.clear()
        GAMBLER.clear()
        GAMBLER_GROUP.clear()
        logger.info("俄罗斯轮盘数据已重置")
    except Exception as e:
        logger.error(f"重置俄罗斯轮盘错误 e:{e}")


@remake.handle()
async def _ (event: GroupMessageEvent):
    GAMBLER_SELF.clear()
    GAMBLER.clear()
    GAMBLER_GROUP.clear()
    await remake.finish("俄罗斯轮盘已重置")
