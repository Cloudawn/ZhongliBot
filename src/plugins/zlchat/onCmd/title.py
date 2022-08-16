
import random

from data.Get_dict import dailyChat_dict
from nonebot.adapters.onebot.v11 import (GROUP_MEMBER, Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment)
# from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.rule import to_me
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import (Replace, get_message_at, get_owner_id,
                                get_userName)
from src.utils.log import logger

pic_root_path = f"{config.bot_path}resources/image"
face_path = f"{config.bot_path}resources/image/zlface"


async def set_title(_title, bot: Bot, event: GroupMessageEvent, title: Message = CommandArg()):
    title_text = title.extract_plain_text()
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
    else:
        user_id = event.user_id
    nickname = (await UserInfo.get_userInfo(user_id))["nickname"]
    if title_text == "":
        msg = f"{nickname}想要什么头衔？"
        await _title.finish(msg)
    user_data = await bot.call_api(
        api="get_group_member_info",
        group_id=event.group_id,
        user_id=event.self_id
    )
    if user_data["role"] != "owner":
        owner_id: int = await get_owner_id(bot, event)
        owner_name = await get_userName(bot, event, user_id=owner_id)
        msg = random.choice([f"按理来说，只有「群主」{owner_name}有权赠予头衔。{nickname}你看......",
                             f"头衔一事……理应由一群之主赠予，我并无缘由干涉。如此，{nickname}不妨去寻{owner_name}商榷。"])
        await _title.finish(msg)
    data = await UserInfo.get_userInfo(user_id=user_id)
    fri_lev = data["friendly_lev"]
    if fri_lev < 3:
        msg = "好感等级不足。"
    elif len(title_text) > 6:
        await _title.finish("如此长的头衔，旅者长期佩戴，可感疲惫？")
    else:
        await bot.call_api(
            api="set_group_special_title",
            group_id=event.group_id,
            user_id=user_id,
            special_title=title_text,
            duration=-1
        )
        logger.debug(
            f"<y>群{event.group_id}用户{event.user_id}头衔设置为{title_text}</y>")
        msg = f"{title_text}，嗯，已经为{nickname}加上了。"
        await _title.finish(msg)
