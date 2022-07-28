

import os
import random
from typing import Type
from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment,
                                         )

from src.modules.user_info import UserInfo
from src.utils.function import Replace
from src.utils.config import config
from data.Get_dict import dailyChat_dict


async def noTOME_say_hello(event: MessageEvent):
    """
    打招呼
    """
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    random_value = random.randint(0, 10)
    if 0 <= random_value < 8:
        msg = Replace(random.choice(dailyChat_dict.打招呼())
                      ).replace("旅者", f"{nickname}")
    else:
        record_path = f"{config.bot_path}/resources/record/问好"
        record_list = os.listdir(record_path)
        msg = (MessageSegment.record(
            f"file:///{record_path}/{random.choice(record_list)}"))
    return msg