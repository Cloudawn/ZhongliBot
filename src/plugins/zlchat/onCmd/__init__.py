
import random
import re
from tokenize import group

from data.Get_dict import dailyChat_dict
from nonebot import on_command
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (GROUP_MEMBER, Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment)
# from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.rule import to_me
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import Replace
from src.utils.log import logger

from ..utils import join_list
from .interaction import momo, momo_me, repeat_users, zl_eat
from .nickname import get_nickname, set_nickname
from .title import set_title

# 钟离部分文案（包括故事、早晚安、进群欢迎）来自lof同人作者 [@阿辰不会写刀](https://whz0508.lofter.com)，禁止抄袭或无授权更改引用。

pic_root_path = f"{config.bot_path}resources/image"
face_path = f"{config.bot_path}resources/image/zlface"

temp_touch = []
for x in config.nickname:
    temp_touch.append("摸摸" + x + "的")
    temp_touch.append("摸" + x + "的")
    temp_touch.append("摸" + x)
    temp_touch.append("摸摸" + x)

_touch = on_command("摸先生的", aliases=set(temp_touch), priority=29, block=True)
onCmdRepeat = on_command(
    "跟我学", aliases={"和我学", "跟我说", "和我说"}, priority=28, rule=to_me(), block=True)
SetNickname = on_command(
    "叫我", aliases={
        "以后叫我",
        "以后请叫我",
        "称呼我",
        "称呼我为",
        "请称呼我",
        "以后请称呼我",
        "以后称呼我",
        "请叫我",
        "我的名字是",
        "我的昵称是"
    }, rule=to_me(), priority=6, block=True)

GetNickname = on_command(
    "我是谁", aliases={"我叫什么", "我的名字是什么"}, rule=to_me(), priority=6, block=True)

eat = on_command("吃", aliases={"喝", "品尝", "请享用",
                 "请吃", "请喝","吃不吃","喝不喝"}, rule=to_me(), priority=27, block=True)

_title = on_command("给我头衔", aliases={"我要头衔"},
                    priority=9, rule=to_me(), block=True)

touch_me = on_command("摸摸", aliases={"摸摸我","摸摸我的"},
                    priority=28, rule=to_me(), block=True)


# 设置昵称
@SetNickname.handle()
async def _(event: MessageEvent, theName: Message = CommandArg()):
    Name = theName.extract_plain_text().strip()
    if not Name:
        send_msg = random.choice([
            "该如何称呼旅者呢？",
            "称呼旅者为无名？"]
        )
        await SetNickname.finish(send_msg)
    else:
        await set_nickname(SetNickname=SetNickname, event=event, theName=Name)


# 查询昵称
@GetNickname.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    send_msg = await get_nickname(GetNickname, bot, event)
    await GetNickname.send(Message(send_msg))
    matcher.stop_propagation()


# 摸钟离
@_touch.handle()
async def _(bot: Bot, event: MessageEvent, touch_part: Message = CommandArg()):
    if not touch_part.extract_plain_text():
        send_msg = "唔......触碰哪个位置呢？"
    else:
        name = await UserInfo.get_userInfo(user_id=event.user_id)
        name = name.get("nickname")
        send_msg = await momo(event=event, touch_part=touch_part)
        send_msg = Replace(send_msg).replace("旅者", f"{name}")
    await _touch.finish(Message(send_msg))

# 摸旅者
@touch_me.handle()
async def _(bot: Bot, event: MessageEvent, touch_part: Message = CommandArg()):
    if not touch_part.extract_plain_text():
        send_msg = "唔......触碰哪个位置呢？"
    else:
        name = await UserInfo.get_userInfo(user_id=event.user_id)
        name = name.get("nickname")
        send_msg = await momo_me(event=event, touch_part=touch_part)
        send_msg = Replace(send_msg).replace("旅者", f"{name}")
    await touch_me.finish(Message(send_msg))


# 学发言人说话
@onCmdRepeat.handle()
async def _(event: MessageEvent, userWords: Message = CommandArg()):
    if not userWords.extract_plain_text():
        await onCmdRepeat.finish("学什么？")
    else:
        await repeat_users(event=event, onCmdRepeat=onCmdRepeat, userWords=userWords)


# 设置头衔
@_title.handle()
async def _(bot: Bot, event: GroupMessageEvent, title: Message = CommandArg()):
    await set_title(_title, bot, event, title)


# 投喂食物
@eat.handle()
async def _(bot: Bot, event: MessageEvent, food: Message = CommandArg()):
    msg = await zl_eat(eat, bot, event, food)
    await eat.finish(msg)
