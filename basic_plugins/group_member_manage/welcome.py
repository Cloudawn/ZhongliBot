
import asyncio
import time
from random import choice
from typing import Type

from nonebot import on, on_notice, on_request
from nonebot.adapters.onebot.v11 import (Bot, GroupIncreaseNoticeEvent,
                                         GroupRequestEvent, Message,
                                         MessageSegment)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from scipy import rand
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import _get_qq_img, get_userName
from src.utils.log import logger

group_welcome = on_notice(priority=1, block=False)

group_request = on_request(priority=1, block=False)


@group_request.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    if event.sub_type == "add":
        data = await bot.get_stranger_info(user_id=event.user_id)
        head = await _get_qq_img(event.user_id)
        msg_head = MessageSegment.image(head)
        await group_request.send(
            choice([
                '嗯？有人在敲门？',
                '有客人来了。',
                '有敲门声。稍等，我去开门。'
            ]
            )
        )
        await asyncio.sleep(0.6)
        msg = f'''\n昵称：{data["nickname"]}'''
        msg += f'''\n账号：{data["user_id"]}'''
        msg += f'''\nQQ等级：{data["level"]}'''
        await group_request.finish(
            MessageSegment.text("这位旅人的信息是...")+msg_head +
            MessageSegment.text(msg)
        )


@group_welcome.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    logger.debug(f"<y>用户{event.user_id}</y>加入了<y>群{event.group_id}</y>")
    if 4 <= int(time.strftime("%H")) < 7:
        msg = (Message(MessageSegment.at(event.user_id) +
               "是不是第一次看见这样的璃月港？尚未到起床的时候。随我到别处坐坐，静候片刻，一同去吃新月轩的早茶。"))
    elif 7 <= int(time.strftime("%H")) < 11:
        await group_welcome.send(Message(MessageSegment.at(event.user_id) + "晨起时就听说来了个外乡人，想来璃月港万商云来之景，应当不会对“外乡人”感到惊奇。见着你……我便懂了。"))
        await asyncio.sleep(1)
        msg = (Message(MessageSegment.at(event.user_id) +
               "把脸擦一擦吧，你这是又去……你所说的“锄大地”了？这边脸上还有矿物的碎片。"))
    elif 11 <= int(time.strftime("%H")) < 13:
        msg = (Message(MessageSegment.at(event.user_id) +
               "好久不见，赶上了好时候。正巧我要去万民堂吃饭，一起么？"))
    elif 13 <= int(time.strftime("%H")) < 18:
        msg = (Message(MessageSegment.at(event.user_id) +
               "你来了？有茶水温在炉上，渴吗？来试试今年的新茶吧。"))
    elif 18 <= int(time.strftime("%H")) < 21:
        msg = (Message(MessageSegment.at(event.user_id) +
               "嗯……？回来了便好。吃过饭了吗？你要先去冒险家协会拿报酬……？也好，就当是饭后散步，我跟你一起去。"))
    elif 21 <= int(time.strftime("%H")) < 24:
        await group_welcome.send(Message(MessageSegment.at(event.user_id) + "夜已渐深，早些休息。我先出去一趟，很快回来"))
        await asyncio.sleep(1)
        msg = (Message(MessageSegment.at(event.user_id) +
               "……问我做什么？是我略有些急了，前些时候，联系了千岩军去找你。我现在去跟他们说一声，你已经返家。"))
    elif 0 <= int(time.strftime("%H")) < 4:
        msg = (Message(MessageSegment.at(event.user_id) +
               "这个时间，来者果然是你。夜已深沉，客房已收拾妥当，进屋歇息吧。"))
    else:
        msg = (Message(MessageSegment.at(event.user_id) +
               "异乡的旅人，原来是你吗？今日一见，阁下果真气宇不凡，有幸结识，倍感欣悦。时间正好，随我进来吧。"))
    await group_welcome.finish(msg)
