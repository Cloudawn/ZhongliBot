import asyncio
# try:
#     import ujson as json
# except ModuleNotFoundError:
import os
import random
import time
from calendar import month
from datetime import date
from typing import NoReturn, Type

from configs.path_config import DATA_PATH, IMAGE_PATH
from nonebot.adapters.onebot.v11 import (Bot, Message, MessageEvent,
                                         MessageSegment)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.log import logger
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import Replace

from data.Get_dict import dailyChat_dict


async def choose_between(onMsg_tome: Type[Matcher], event: MessageEvent, c_1: str, c_2: str):
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    ask_times = 0
    if c_1 == c_2:
        msg = Message("二者有何区别？")
    else:
        msg = Message(random.choice([c_1, c_2]))
        msg = Replace(msg).replace("我", f"{nickname}").replace(
            "你", "我").replace("钟离", "我")
    return msg


async def lift_up(onMsg_tome: Type[Matcher], event: MessageEvent):
    img_path = f"{config.bot_path}resources/image/zlface"
    image_list = [f"file:///{img_path}/立柱子.jpg",
                  f"file:///{img_path}/立柱子2.jpg", f"file:///{img_path}/立柱子3.jpg"]
    await onMsg_tome.send(random.choice(["上来吧", "来吧"]))
    await onMsg_tome.finish(MessageSegment.image(random.choice(image_list)))


async def wife(onMsg_tome: Type[Matcher], event: MessageEvent):
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    fri_lv = data["friendly_lev"]
    msg: Message = Message()
    if fri_lv <= 0:
        msg = random.choice(dailyChat_dict.likeZl_lv0())
    else:
        msg = random.choice(dailyChat_dict.老婆())
    msg = Replace(msg).replace("旅者", f"{nickname}")
    return msg


async def husband(onMsg_tome: Type[Matcher], event: MessageEvent):
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    fri_lv = data["friendly_lev"]
    msg: Message = Message()
    if fri_lv <= 0:
        msg = random.choice(dailyChat_dict.likeZl_lv0())
    else:
        msg = random.choice(dailyChat_dict.老公())
    msg = Replace(msg).replace("旅者", f"{nickname}")
    return msg


async def say_overworked(onMsg_tome: Type[Matcher]):
    random_value = random.randint(0, 10)
    if 0 <= random_value <= 3:
        await onMsg_tome.send("额外的工作吗？嗯......并非不可接受")
        return ("不过，需额外支付对等的报酬。毕竟，交易的规矩是「契约」，准则是「公平」。")
    else:
        return (random.choice(dailyChat_dict.钟离加班()))


async def lost_patience(onMsg_tome: Type[Matcher], event: MessageEvent, ask_times):
    if ask_times > 5:
        msg = random.choice(dailyChat_dict.提问不耐烦())
        await onMsg_tome.finish(MessageSegment.reply(event.message_id)+msg)


async def zl_sad(onMsg_tome: Type[Matcher], event: MessageEvent):
    msg = random.choice(["近日往生堂的事务似乎增加了不少……唔。以普遍理性而论，有工作，便意味着有人办丧事。人之于世界，便犹如浮萍一般啊......(叹）",
                         "昔人已逝，旧友难觅，每每思及此处，不免有些伤感......",
                         "璃月，这片脱离神佑的琉璃之地，想必会在人的打磨下散发更醉人的光泽，这一点我从未怀疑过。只是漫长时光匆匆流逝，说不定哪天，我便追不上它的脚步，这该如何是好？"])
    return (MessageSegment.reply(event.message_id)+msg)


async def repeat_zhongli(onMsg_tome: Type[Matcher], event: MessageEvent):
    random_value = random.randint(0, 10)
    if 0 <= random_value <= 5:
        Msg = random.choice(dailyChat_dict.先生先生())
        return Msg
    elif 6 <= random_value <= 8:
        await onMsg_tome.send("你这样子，倒让我想起屋里那只画眉。")
        await asyncio.sleep(1)
        return random.choice(dailyChat_dict.小鸟很吵())
    else:
        await onMsg_tome.send((Message(random.choice(dailyChat_dict.小鸟喳喳叫()))))
        await asyncio.sleep(1)
        return random.choice(["罢了，约莫是幻觉",
                              "(客卿自然地关上了窗户)"])


async def no_money(event: MessageEvent):
    random_value = random.randint(0, 10)
    nickname = (await UserInfo.get_userInfo(user_id=event.user_id))["nickname"]
    if 0 <= random_value <= 5:
        msg = (random.choice(dailyChat_dict.钟离没钱()))
    else:
        record_path = f"{config.bot_path}/resources/record/摩拉"
        record_list = os.listdir(record_path)
        msg = Message(MessageSegment.record(
            f"file:///{record_path}/{random.choice(record_list)}"))
    return Replace(msg).replace("旅者", f"{nickname}")
