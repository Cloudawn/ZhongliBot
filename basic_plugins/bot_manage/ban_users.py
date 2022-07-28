import asyncio
import os
import random
from typing import Type

# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent, Message,
                                         MessageEvent, MessageSegment)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.log import logger


async def ban_users(bot: Bot, event: GroupMessageEvent, onMsg_AllNickname: Type[Matcher]):
    user_id = event.user_id
    change_value = random.randint(-10, -5)
    await UserInfo.change_frendly(user_id, change_value)
    record_path = f"{config.bot_path}/resources/record/凶"
    img_path = f"{config.bot_path}/resources/image/zlface/不满"
    record_list = os.listdir(record_path)
    img_list = os.listdir(img_path)
    try:
        await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
    except ActionFailed:
        pass
    await onMsg_AllNickname.send(MessageSegment.record(f"file:///{record_path}/{random.choice(record_list)}"))
    warning_list = ["请莫要如此消遣我了", "食岩之罚，你自己好好体会吧", "注意礼数", "无礼"]
    await onMsg_AllNickname.finish(MessageSegment.image(f"file:///{img_path}/{random.choice(img_list)}") + f"{random.choice(warning_list)}\n——好感度{change_value}")


async def anti_abuse(bot, event,  abuse):
    # abuse_words = abuse.MessageEvent_to_text()
    await bot.send_group_msg(
        group_id=config.main_group,
        message=f"有人对钟离说 {abuse}\nfrom 群{event.group_id}，用户QQ：{event.user_id}")
