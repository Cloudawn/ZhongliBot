import os
import random

from nonebot import on, on_notice
from nonebot.adapters.onebot.v11 import (Bot, GroupIncreaseNoticeEvent,
                                         Message, MessageSegment,
                                         PokeNotifyEvent)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from src.utils.config import config
from src.utils.log import logger

from .data import zl_send_welcome

welcome = on_notice(priority=1, block=False)

poke = on_notice(priority=5, block=False)


@welcome.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    logger.debug(f"<y>用户{event.user_id}</y>加入了<y>群{event.group_id}</y>")
    msg = await zl_send_welcome(welcome, event)
    await welcome.finish(msg)


@poke.handle()
async def _poke(bot: Bot, event: PokeNotifyEvent, matcher: Matcher):
    qq = event.target_id
    if qq != event.self_id:
        matcher.stop_propagation()
        raise FinishedException
    random_value = random.randint(1, 10)
    if random_value >= 5:
        poke_path = f"{config.bot_path}resources/image/poke"
        poke_list = os.listdir(poke_path)
        await poke.finish(MessageSegment.image(
            f"file:///{poke_path}/{random.choice(poke_list)}"))
    else:
        qq = event.user_id
        await poke.finish(MessageSegment("poke", {"qq": qq}))
