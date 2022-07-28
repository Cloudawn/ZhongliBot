import asyncio
# try:
#     import ujson as json
# except ModuleNotFoundError:
import json
import os
import random
import time
from calendar import month
from datetime import date
from typing import NoReturn, Type

from configs.path_config import DATA_PATH, IMAGE_PATH
# zlchat = json.load(open(DATA_PATH / "zlchat.json", "r", encoding="utf8"))
from data.Get_dict import dailyChat_dict
from nonebot.adapters.onebot.v11 import (Bot, Message, MessageEvent,
                                         MessageSegment)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.log import logger
from src.modules.user_info import UserInfo
from src.utils.config import config
from zhdate import ZhDate

from ..utils import join_list

pic_root_path = f"{config.bot_path}resources/image"
face_path = f"{config.bot_path}resources/image/zlface"
record_path = f"{config.bot_path}resources/record"


async def Tozl_HappyBirthday(onMsg_AllNickname: Type[Matcher]):
    if int(time.strftime("%m")) == 12 and int(time.strftime("%d")) == 31:
        random_value = random.randint(0, 10)
        # asyncio.create_task(onMsg_AllNickname.finish("你得到了钟离赠送的？"))
        asyncio.create_task(get_BirthdayGifts(onMsg_AllNickname))
        if 10 >= random_value > 8:
            await onMsg_AllNickname.send("不知不觉，又到了一年之始。")
            await asyncio.sleep(1)
            return(Message(f"[CQ:image,file=file:///{face_path}/-69daf10b6c6b9daa.jpg]颇为特别的一天，既是结束，也是开始。每逢今日，便会心生感慨。"))
        elif 8 >= random_value > 6:
            await onMsg_AllNickname.send("在这般特殊的日子，我也想见见这个世界的明镜，旅者。")
            await asyncio.sleep(1)
            return("旅行许久的人，也应回来休憩片刻了。")
        else:
            return(Message(random.choice(dailyChat_dict.Tozl_HappyBirthday())))
    else:
        return(random.choice(["旅者，今天并非我的生日。", "今天并非钟某生日，旅者可是记错了？", "今日虽并非我的生辰，但劳旅者挂念了。谢谢你，我的朋友。"]))


async def get_BirthdayGifts(onMsg_AllNickname):
    gifts_list = [
        "琉璃百合的干花", "异梦溶媒", "霓裳花", "琉璃袋", "老石", "山水玲珑对杯"
    ]
    gift = random.choice(gifts_list)
    await asyncio.sleep(3.5)
    return(f"你得到了钟离赠送的的「{gift}」\n►我的背包")


async def ToUser_HappyBirthday(onMsg_AllNickname: Type[Matcher]):
    asyncio.create_task(get_BirthdayGifts(onMsg_AllNickname))
    _month = time.strftime("%m")
    _date = time.strftime("%d")
    return(f'''{_month}月{_date}日，原来这一天是你的诞辰吗？嗯，我记住了。祝愿你生日快乐。''')


async def BegAttention(onMsg_AllNickname: Type[Matcher]):
    await onMsg_AllNickname.send(random.choice(dailyChat_dict.理我()))
    await asyncio.sleep(1.5)
    return(random.choice(dailyChat_dict.回的慢原因()))


async def Lantern_Ftvl(event: MessageEvent, onMsg_AllNickname: Type[Matcher]):
    # 后续将赠礼写入背包
    zhtoday = str(ZhDate.today())
    year = time.strftime("%Y")
    if zhtoday != str(f"农历{year}年1月15日"):
        return(f"旅者，今天并非元宵节。")
    else:
        return(MessageSegment.reply(event.message_id)+f"元宵节快乐，旅者。\n你收到了一份「手制汤圆」\n►我的背包")


async def ZhuYue_Ftvl(event: MessageEvent, onMsg_AllNickname: Type[Matcher]):
    user_id = event.user_id
    nickname = (await UserInfo.get_userInfo(user_id))["nickname"]
    _month = time.strftime("%m")
    if _month != "9":
        return(f"{nickname}，今天并非逐月节。")
    else:
        return(MessageSegment.reply(event.message_id)+random.choice([

            "愿逐月华流照君。",
            "逐月节……今年，你有什么想许的愿望吗？",
            f"好久不见，{nickname}从须弥回来了？",
            "天星照我，愿逐月华。",
            "时节刚好，理应出去走走，等一桌美食。"
        ]))
