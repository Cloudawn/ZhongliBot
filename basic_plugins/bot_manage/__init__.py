import imp
import json
import os
import random
import re

from basic_plugins.bot_manage.ban_users import anti_abuse, ban_users
from nonebot import on_command, on_keyword, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (GROUP_MEMBER, Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment,
                                         PrivateMessageEvent)
from nonebot.exception import FinishedException,ActionFailed
from nonebot.internal.matcher import Matcher
from nonebot.log import logger
from nonebot.params import CommandArg, Depends, EventPlainText
from nonebot.rule import to_me
from src.utils.config import config
from src.utils.function import MessageEvent_to_text,get_message_at,get_userName,get_owner_id
from src.utils.rule import all_nickname
from nonebot.permission import SUPERUSER


# 救命，我好希望你们能穿上苦茶籽
onMsg_AllNickname = on_regex(
    r"(.*)(?i)(hso|好色|龙根|脐橙|骑乘|被日|精液|被干|后入|中出|口交|骚|操我|草我|草.*批|草你|龙奶|龙精|摸钟离|屁股|摸pg|上我|上你|做爱|交尾|交配|hs0|好涩|很涩|很色|太色|太涩|好瑟|口我|璃月魂|臀|doi|橄榄|超市|日我|草我|草你|艹你|看.*批|小批|奶头|寄吧|奶子|日.批|淫)(.*)",
    priority=5, rule=all_nickname, block=True)

set_admin = on_command("设置管理",priority=5,block=True,permission=SUPERUSER)
cancle_admin = on_command("取消管理",priority=5,block=True,permission=SUPERUSER)

sensitive_words = {"屎", "智障", "傻逼", "爬", "爪巴",
                   "去死", "滚", "牛马", "贵物", "💩", "尿","垃圾","辣鸡"}
onKwrd_AllNickname = on_keyword(
    keywords=sensitive_words, priority=1, block=True, rule=all_nickname)


@onMsg_AllNickname.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    await ban_users(bot=bot, event=event, onMsg_AllNickname=onMsg_AllNickname)
    matcher.stop_propagation()


@onKwrd_AllNickname.handle()
async def _(bot: Bot, matcher: Matcher, event: MessageEvent, abuse=EventPlainText()):
    await anti_abuse(bot=bot, event=event, abuse=abuse)
    matcher.stop_propagation()

@set_admin.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
        admin_name = await get_userName(bot,event,user_id)
        user_data = await bot.get_group_member_info(group_id = event.group_id,user_id=user_id)
        zl_data = await bot.get_group_member_info(group_id = event.group_id,user_id=event.self_id)
        if zl_data["role"] !="owner":
            owner_id = await get_owner_id(bot,event)
            owner_name = await get_userName(bot,event,owner_id)
            msg = f"按理来说，只有「群主」{owner_name}有权任命管理。"
        elif user_data["role"] != "admin":
            await bot.set_group_admin(group_id = event.group_id,user_id=user_id,enable=True)
            msg = f"已设置【{admin_name}】为群管理。"
        else:
            msg = f"【{admin_name}】已经是群管理了。"
    else:
        msg = "设置哪一位为管理呢？"
    await set_admin.finish(msg)

@cancle_admin.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
        admin_name = await get_userName(bot,event,user_id)
        user_data = await bot.get_group_member_info(group_id = event.group_id,user_id=user_id)
        zl_data = await bot.get_group_member_info(group_id = event.group_id,user_id=event.self_id)
        if zl_data["role"] !="owner":
            owner_id = await get_owner_id(bot,event)
            owner_name = await get_userName(bot,event,owner_id)
            msg = f"按理来说，只有「群主」{owner_name}有权取消管理。"
        elif user_data["role"] != "admin":
            msg = f"【{admin_name}】不是群管理。"
        else:
            await bot.set_group_admin(group_id = event.group_id,user_id=user_id,enable=False)
            msg = f"已取消【{admin_name}】群管理。"
    else:
        msg = "设置哪一位为管理呢？"
    await cancle_admin.finish(msg)


