import asyncio
import json
import os
import random
import re
import time
from calendar import month
from datetime import date
from typing import NoReturn, Type

from configs.path_config import DATA_PATH, IMAGE_PATH
from data.Get_dict import dailyChat_dict
from nonebot.adapters.onebot.v11 import (Bot, Message, MessageEvent,
                                         MessageSegment)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.log import logger
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import Replace

pic_root_path = f"{config.bot_path}resources/image"
face_path = f"{config.bot_path}resources/image/zlface"


async def date_with_zl(onMsg_AllNickname: Type[Matcher], event: MessageEvent, matcher: Matcher, event_msg: str):
    user_id = event.user_id
    random_value = random.randint(0, 10)
    data = await UserInfo.get_userInfo(user_id)
    last_sign = data["last_date_sign"]
    nickname = data["nickname"]
    fri_lev = data["friendly_lev"]
    print(f"昨天签到日期是{last_sign}")
    if last_sign == date.today():
        msg = random.choice([
            f"这就是「磨损」吗，略感疲惫......啊，抱歉，{nickname}有何事？",
            f"嗯.....下雨了，着实遗憾。{nickname}，我们明天再出去吧。 ",
            f"抱歉，{nickname}。今天还有一场典仪，恕我难以奉陪了。明日再叙，如何？",
            f"嗯......乌云密布，恐怕雷雨将至。不适合再逗留在外了，我送{nickname}回家吧。",
            "醒来便听到了窗外嘈杂的雨声，应是昨夜的雨还没停止。既然如此，那今日就不要出门了。只是可惜了田先生的说书。"
        ])
        return(msg)
    if 4 > int(time.strftime("%H")) >= 0:
        msg = random.choice(
            ["夜色已深，集市港口已收，不妨早些休息吧，明日再去也不迟。", "（夜已深沉，客卿睡下了，改日再寻吧。）"])
        return msg
    if fri_lev <= 0:
        change_value = await UserInfo.date_sign_in(user_id=user_id)
        return(MessageSegment.reply(event.message_id) + "......谢谢，劳你费心了。" + f"\n——好感度+{change_value}")
    if re.match(r"(.*)(吃|喝|买)(.*)", event_msg, re.U):
        pattern_1 = re.match(r"(.*)(吃|喝|买)(.*)", event_msg, re.U)
        assert pattern_1 is not None
        match_target = pattern_1.group(3)
        if match_target == "":
            msg = "？"
            return(msg)
        if re.match(r'(.*)杏仁豆腐(.*)', match_target, re.U):
            return(MessageSegment.reply(event.message_id) + random.choice([
                "嗯......白嫩光滑，细腻柔软，品相与滋味均为上呈，劳你费心了。",
                "这个味道......或许魈会喜欢。他对食物也可算刁钻，当然，是另一种意义上的。"
            ]) + f"\n——好感度+{change_value}")
        elif re.match(r'(.*)(海鲜|触手|极致一钓|鱼)(.*)', match_target, re.U):
            return(MessageSegment.reply(event.message_id) + Message(random.choice([
                f"对{nickname}而言，试探我对不同事物的反应，颇有乐趣对么。不过......我不太喜欢这个。",
                f"[CQ:image,file=file:///{face_path}/心虚2.jpg]{nickname}，谢谢。",
                "这......多谢。"
            ]) + f"\n——好感度+{change_value}"))
        elif re.match(r'(.*)腌笃鲜(.*)', match_target, re.U):
            return(MessageSegment.reply(event.message_id) + f"嗯......是来自轻策庄的春笋？想必，这一定费了你颇多心思吧，感谢你，{nickname}。" + f"\n——好感度+{change_value}")
    if 0 <= random_value <= 7:
        return(MessageSegment.reply(event.message_id) + random.choice(dailyChat_dict.成功约会()) + f"\n——好感度+{change_value}")
    else:
        record_path = f"{config.bot_path}resources/record/每日约会"
        record_list = os.listdir(record_path)
        await onMsg_AllNickname.send(MessageSegment.record(
            f"file:///{record_path}/{random.choice(record_list)}"))
        return(MessageSegment.reply(event.message_id)+f"——好感度+{change_value}")
    # await give_gifts(onMsg_AllNickname, matcher, event, nickname, fri_lev)


async def give_gifts(onMsg_AllNickname: Type[Matcher], matcher: Matcher, event: MessageEvent, nickname: str, fri_lev: int):
    if fri_lev < 4 or random.randint(1, 10) > 1:
        matcher.stop_propagation()
    else:
        gift_list = [
            "磐陀裂生之花",
            "星罗圭璧之晷",
            "不动玄石之相",
            "勋绩之花",
            "盟誓金爵",
            "坚牢黄玉",
            "嵯峨群峰之翼",
            "巉岩琢塑之樽"
            "古老的戒指"
        ]
        return (f"我稍微为{nickname}备了一点薄礼，但愿它能合你心意。\n你收到了钟离赠送的【{random.choice(gift_list)}】")


async def hand_in_hand(onMsg_AllNickname: Type[Matcher], event: MessageEvent) -> NoReturn:
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    fri_lv = data["friendly_lev"]
    msg: Message = Message()
    if fri_lv <= 0:
        msg = random.choice(dailyChat_dict.touch_lv0())
    elif 0 < fri_lv <= 2:
        msg = random.choice(dailyChat_dict.hand_in_hand_lv1())
    elif 2 < fri_lv:
        msg = random.choice(dailyChat_dict.hand_in_hand_lv2())
    msg = Replace(msg).replace("旅者", f"{nickname}")
    await onMsg_AllNickname.finish(Message(msg))


async def treat_user(onMsg_AllNickname: Type[Matcher], event: MessageEvent) -> NoReturn:
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    fri_lv = data["friendly_lev"]
    if fri_lv <= 0:
        msg = random.choice(dailyChat_dict.likeZl_lv0())
        await onMsg_AllNickname.finish(Message(msg))
    else:
        record_path = f"{config.bot_path}resources/record/先生可以给我买吗"
        record_list = os.listdir(record_path)
        msg = MessageSegment.record(
            f"file:///{record_path}/{random.choice(record_list)}")
        await onMsg_AllNickname.finish(msg)


async def hug(event: MessageEvent):
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    fri_lev = data["friendly_lev"]
    if fri_lev <= 0:
        msg = random.choice(dailyChat_dict.touch_lv0())
    elif 0 < fri_lev <= 2:
        msg = random.choice([
            f"若没记错，{nickname}应该已经过了瑶瑶小朋友的年纪了。",
            f"{nickname}，这是何意？"
        ])
    else:
        msg = random.choice([
            f"[CQ:image,file=file:///{face_path}/忍俊不禁.jpg]旅者变成孩童了吗？ ",
            f"[CQ:image,file=file:///{face_path}/宠溺.jpg]好了，旅者满意了吗？",
            f"[CQ:image,file=file:///{face_path}/几颗牙.jpg]旅者，今年几岁了？",
            "旅者的身子有些烫，可是着了风寒？且随我回屋吧，我备了些汤药。"
        ])
    return(Message(msg))


async def kiss(event: MessageEvent):
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    fri_lev = data["friendly_lev"]
    if fri_lev <= 0:
        msg = Message(random.choice(dailyChat_dict.touch_lv0()))
        return msg
    elif 0 < fri_lev <= 1:
        msg = Message(random.choice(dailyChat_dict.likeZl_lv0()))
        return msg
    else:
        fri_dict: dict = {
            "2": [
                f"出于礼节的话，可以。",
                f"{nickname}，这或许有些亲密。",
                f"......太近了。入乡随俗，在璃月的话，{nickname}还是使用含蓄的礼节吧。",
                f"[CQ:image,file=file:///{face_path}/2965dbdc8a4895a7.jpg]该说{nickname}是童心未泯，还是涉世未深呢？"
            ],
            "3": [
                "......作为问好的话，一次便可。......好了，够了。",
                f"{nickname}在撒娇吗？",
                "这样看来，蒙德的文化已对你深有影响。",
                f"这是{nickname}家乡的礼仪吗？至冬、蒙德也有类似的礼节，称作「贴面礼」。{nickname}这是需要我......亲吻面颊？",
                f"[CQ:image,file=file:///{face_path}/-6843543330053208.jpg]该说{nickname}是涉世未深，还是童心未泯呢......",
                f"[CQ:image,file=file:///{face_path}/忍俊不禁2.jpg]这种事可不能开玩笑。"
            ],
            "4": [
                f"[CQ:image,file=file:///{face_path}/害羞.jpg]我们之间的情谊，应该如何定义呢？",
                "......作为问好的话，一次便可。......好了，够了。",
                f"{nickname}在撒娇吗？",
                "这样看来，蒙德的文化已对你深有影响。",
                f"这是{nickname}家乡的礼仪吗？至冬、蒙德也有类似的礼节，称作「贴面礼」。{nickname}这是需要我......亲吻面颊？",
                f"[CQ:image,file=file:///{face_path}/略带坏笑.png]该说{nickname}是涉世未深，还是童心未泯呢......",
                f"[CQ:image,file=file:///{face_path}/微笑2.jpg]今日又来了？",
                "嗯......我虽是老派璃月人，但也并非不能接受年轻人的礼节。"
            ],
            "5": [
                f"[CQ:image,file=file:///{face_path}/害羞.jpg]我们之间的情谊，应该如何定义呢？",
                "......作为问好的话，一次便可。......好了，够了。",
                f"{nickname}在撒娇吗？",
                "这样看来，蒙德的文化已对你深有影响。",
                f"这是{nickname}家乡的礼仪吗？至冬、蒙德也有类似的礼节，称作「贴面礼」。{nickname}这是需要我......亲吻面颊？",
                f"[CQ:image,file=file:///{face_path}/略带坏笑.png]该说{nickname}是涉世未深，还是童心未泯呢......",
                f"[CQ:image,file=file:///{face_path}/微笑2.jpg]今日又来了？",
                "嗯......我虽是老派璃月人，但也并非不能接受年轻人的礼节。"
            ]
        }
        msg = Message(random.choice(fri_dict[str(fri_lev)]))
        msg = Message(MessageSegment.reply(event.message_id)+msg)
        return(Message(msg))
