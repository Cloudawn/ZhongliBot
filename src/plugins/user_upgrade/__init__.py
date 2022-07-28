from nonebot import on_command, on_fullmatch, on_keyword, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (GROUP_MEMBER, Bot, Message,
                                         MessageEvent, MessageSegment)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.log import logger
from src.modules.user_attr import UserAttr
from src.modules.user_info import UserInfo
from src.utils.function import get_message_at
from src.utils.rule import all_nickname
from typing_extensions import Self

MyAttr = on_command(
    "我的面板", aliases={"我的属性", "查看面板", "查看属性"}, priority=5, block=True)

MyInfo = on_command("我的好感", aliases={"我的信息", "好感度", "我的背包", "有多喜欢我", "查看背包", "多喜欢我"},
                    priority=5, block=True)

ZLInfo = on_regex(r"^((钱包|背包)|翻.*钱包)$", rule=all_nickname,
                  priority=5, block=True)

Ascend = on_regex(r"^(突破|等级突破|突破等级)$", priority=5, block=True)

UPgrade = on_regex(r"^经验$", priority=5, block=True)

gold_dict = {"0": 10000, "1": 12500, "2": 16000,
             "3": 18000, "4": 21000, "5": 25000}

lev_dict = {
    "0": 1,
    "1": 20,
    "2": 40,
    "3": 50,
    "4": 60,
    "5": 70,
    "6": 80}


@Ascend.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    """
    等级突破
    """
    user_id = event.user_id
    data_info = await UserInfo.get_userInfo(user_id)
    data_attr = await UserAttr.get_userAttr(user_id)
    gold = data_info.get("all_gold")
    lev = data_attr.get("level")
    ascrendLev = data_attr.get("ascrendLev")
    reduce_gold = gold_dict.get(str(f"{ascrendLev}"))
    can_ascend = await UserAttr.Ascend(user_id=user_id, gold=gold, reduce_gold=reduce_gold)

    if can_ascend:
        await UserInfo.change_gold(user_id, reduce_gold)
        gold = data_info.get("all_gold")
        await Ascend.finish(f"突破成功，现原石为{gold-reduce_gold}, 等级为{lev}，突破等级为{ascrendLev+1}")
    else:
        if gold < reduce_gold:
            await Ascend.finish(f"突破失败，现原石为{gold}, 差{reduce_gold-gold}, 等级为{lev}，突破等级为{ascrendLev}")
        else:
            # if lev_dict.get(str(ascrendLev)):
            await Ascend.finish(f"突破失败，当前等级为{lev}，当前突破等级为{ascrendLev}，下一突破所需等级为{lev_dict.get(str(ascrendLev+1))}")


@MyAttr.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    """
    查看个人属性或者他人属性
    """
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
    else:
        user_id = event.user_id
    data_attr = await UserAttr.get_userAttr(user_id)
    atk = data_attr["atk"]
    version = data_attr["version"]
    lev = data_attr["level"]
    ascLev = data_attr["ascrendLev"]
    maxHP = data_attr["maxHP"]
    crtHP = data_attr["crtHP"]
    maxEXP = data_attr["maxEXP"]
    crtEXP = data_attr["crtEXP"]
    eleMas = data_attr["eleMas"]
    critRate = round(data_attr["critRate"], 2)
    critDmg = data_attr["critDmg"]
    speed = data_attr["speed"]
    _def = data_attr["def"]
    msg = f"属性：{version}\n角色等级：{lev}\n突破等级：{ascLev}\n攻击力：{atk}\n生命值：{crtHP}/{maxHP}\n双暴：{critRate}/{critDmg}\n经验值：{crtEXP}/{maxEXP}\n元素精通：{eleMas}\n速度：{speed}\n防御值：{_def}"
    await MyAttr.finish(MessageSegment.reply(event.message_id)+(msg))
    # matcher.stop_propagation


@MyInfo.handle()
async def _(bot: Bot, event: MessageEvent):
    """
    查看个人信息或者他人信息
    """
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
    else:
        user_id = event.user_id
    data_attr = await UserInfo.get_userInfo(user_id)
    gold = data_attr["all_gold"]
    all_friendly = data_attr["all_friendly"]
    friendly_lev = data_attr["friendly_lev"]
    max_friendly = data_attr["max_friendly"]
    msg = f"原石：{gold}\n好感度：{all_friendly}/{max_friendly}\n好感等级：{friendly_lev}"
    await MyInfo.finish(MessageSegment.reply(event.message_id)+(msg))


@ZLInfo.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    """
    查看钟离信息
    """
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
    else:
        user_id = event.user_id
    gold = (await UserInfo.get_userInfo(event.self_id))["all_gold"]
    msg = f"钟离的原石：{gold}"
    await MyInfo.finish(MessageSegment.reply(event.message_id)+(msg))


@UPgrade.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    """
    等级突破
    """
    user_id = event.user_id
    data_attr = await UserAttr.add_exp(user_id)
    data = await UserAttr.get_userAttr(user_id)
    lev = data.get("level")
    ascrendLev = data.get("ascrendLev")
    await MyAttr.finish(f"经验增加了{data_attr}，角色等级为{lev}，突破等级为{ascrendLev}")
