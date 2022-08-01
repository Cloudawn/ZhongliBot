import asyncio
import random
import time
from typing import Literal

from nonebot import get_bots, on_notice, on_regex
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.adapters.onebot.v11.event import (FriendAddNoticeEvent,
                                               GroupMessageEvent)
from nonebot.adapters.onebot.v11.permission import (GROUP, GROUP_ADMIN,
                                                    GROUP_OWNER)
from nonebot.params import Depends
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
# from src.utils.browser import browser
from src.utils.log import logger
from src.utils.utils import GroupList_Async

from . import data_source as source

'''
群管理插件，实现功能有：
* 设置活跃值
* 机器人开关
* 滴滴
'''


set_activity = on_regex(pattern=r"^活跃值 (\d){1,2}$", permission=SUPERUSER |
                        GROUP_ADMIN | GROUP_OWNER, priority=2, block=True)  # 设置活跃值[0-99]

robot_status = on_regex(pattern=r"^(休息|醒醒)$", permission=SUPERUSER |
                        GROUP_ADMIN | GROUP_OWNER, priority=2, block=True, rule=to_me())  # 设置机器人开关

didi = on_regex(pattern=r"^滴滴 ", permission=GROUP_ADMIN |
                GROUP_OWNER, priority=3, block=True)  # 滴滴

get_notice = on_notice(priority=3, block=True)  # 通知事件

# -------------------------------------------------------------
#   Depends依赖
# -------------------------------------------------------------


def get_name(event: GroupMessageEvent) -> str:
    '''获取后置文本内容'''
    return event.get_plaintext().split(" ")[-1]


def get_status(event: GroupMessageEvent) -> bool:
    '''获取机器人开关'''
    status = event.get_plaintext().split(" ")[-1]
    print(status)
    return status == "醒醒"


async def get_didi_msg(bot: Bot, event: GroupMessageEvent) -> Message:
    '''返回要说的话'''
    msg = event.get_message()
    group = await bot.get_group_info(group_id=event.group_id)
    group_name = group['group_name']
    user_name = event.sender.card if event.sender.card != "" else event.sender.nickname
    msg_header = f"收到 | {user_name}({event.user_id}) | @群【{group_name}】({event.group_id}) | 的滴滴消息\n\n"
    msg[0] = MessageSegment.text(msg_header + str(msg[0])[3:])
    return msg

# ----------------------------------------------------------------
#  matcher实现
# ----------------------------------------------------------------


@set_activity.handle()
async def _(event: GroupMessageEvent, name: str = Depends(get_name)):
    '''设置活跃值'''
    logger.info(
        f"<y>群管理</y> | <g>群{event.group_id}</g> | 设置活跃值 | {name}"
    )
    activity = int(name)
    await source.set_activity(event.group_id, activity)
    await set_activity.finish(f"当前活跃值为：{name}")


@robot_status.handle()
async def _(event: GroupMessageEvent, status: bool = Depends(get_status)):
    '''设置机器人开关'''
    logger.info(
        f"<y>群管理</y> | <g>群{event.group_id}</g> | 设置机器人开关 | {status}"
    )
    await source.set_status(event.group_id, status)
    name = "开启"if status else "关闭"
    if name == "开启":
        await robot_status.finish(f"唔......我方才睡着了？")
    else:
        await robot_status.finish(f"那我便去休息了，再会。")


@didi.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = Depends(get_didi_msg)):
    '''滴滴功能'''
    logger.info(
        f"<y>群管理</y> | <g>群{event.group_id}</g> | 滴滴功能 | {msg}"
    )
    superusers = list(bot.config.superusers)
    if not superusers:
        await didi.finish("唔......发送给谁好呢？（未配置bot管理者，无法发送）")
    for user in superusers:
        await bot.send_private_msg(user_id=int(user), message=msg)
    await didi.finish()


@get_notice.handle()
async def _(bot: Bot, event: FriendAddNoticeEvent):
    '''好友增加通知事件'''
    friend = await bot.get_stranger_info(user_id=event.user_id)
    nickname = friend['nickname']
    msg = f"“一份新的契约？好吧，虽然我还在度假，但也可以陪你走一趟。度假期间的话，我会自称「钟离」，你呢，{nickname}，你会签下什么名字？”"
    superusers = list(bot.config.superusers)
    async for user_id in GroupList_Async(superusers):
        try:
            await bot.send_private_msg(user_id=user_id, message=f"{nickname}({event.user_id})已是我的友人了。")
        except Exception:
            pass
    await get_notice.finish(msg)
