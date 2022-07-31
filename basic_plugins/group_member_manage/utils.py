import random

import nonebot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import ActionFailed, Bot, GroupMessageEvent
from src.utils.log import logger

from .config import global_config, plugin_config

su = global_config.superusers


async def banSb(gid: int, ban_list: list, time: int = None, scope: list = None):
    """
    构造禁言
    :param gid: 群号
    :param time: 时间（s)
    :param ban_list: at列表
    :param scope: 用于被动检测禁言的时间范围
    :return:禁言操作
    """
    if 'all' in ban_list:
        yield nonebot.get_bot().set_group_whole_ban(
            group_id=gid,
            enable=True
        )
    else:
        if time is None:
            if scope is None:
                time = random.randint(
                    plugin_config.ban_rand_time_min, plugin_config.ban_rand_time_max)
            else:
                time = random.randint(scope[0], scope[1])
        for qq in ban_list:
            if int(qq) in su or str(qq) in su:
                logger.info(f"SUPERUSER无法被禁言, {qq}")

            else:
                yield nonebot.get_bot().set_group_ban(
                    group_id=gid,
                    user_id=qq,
                    duration=time,
                )
