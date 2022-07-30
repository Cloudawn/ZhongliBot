from sched import scheduler
from typing import Dict, List

from src.utils.log import logger
from src.utils.scheduler import scheduler

from .individual import money as money
from .multiplayer import russian as russian
from .multiplayer import shot as shot
from .utils import GAMBLER, GAMBLER_GROUP, GAMBLER_SELF


@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    '''每天零点重置俄罗斯轮盘数据'''
    logger.info("正在重置俄罗斯轮盘数据")
    GAMBLER_SELF.clear()
    GAMBLER.clear()
    GAMBLER_GROUP.clear()
    logger.info("俄罗斯轮盘数据已重置")
