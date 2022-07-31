import os
import random

from nonebot import  on_notice
from nonebot.adapters.onebot.v11 import (Bot, GroupAdminNoticeEvent,
                                         GroupIncreaseNoticeEvent, Message,
                                         MessageSegment, PokeNotifyEvent)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.log import logger



poke = on_notice(priority=5, block=False)


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



