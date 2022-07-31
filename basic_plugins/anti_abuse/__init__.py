
from nonebot import on_command, on_keyword, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (GROUP_MEMBER, Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment,
                                         PrivateMessageEvent)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.log import logger
from nonebot.params import EventPlainText
from nonebot.rule import to_me
from src.utils.config import config
from src.utils.rule import all_nickname

from .ban_users import anti_abuse, ban_users

# 救命，我好希望你们能穿上苦茶籽
onMsg_AllNickname = on_regex(
    r"(.*)(?i)(hso|好色|龙根|脐橙|骑乘|被日|精液|被干|后入|中出|口交|骚|操我|草我|草.*批|草你|龙奶|龙精|摸钟离|屁股|摸pg|上我|上你|做爱|交尾|交配|hs0|好涩|很涩|很色|太色|太涩|好瑟|口我|璃月魂|臀|doi|橄榄|超市|日我|草我|草你|艹你|看.*批|小批|奶头|寄吧|奶子|日.批|淫)(.*)",
    priority=5, rule=all_nickname, block=True)

sensitive_words = {"屎", "智障", "傻逼", "爬", "爪巴",
                   "去死", "滚", "牛马", "贵物", "💩", "尿", "垃圾", "辣鸡"}
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
