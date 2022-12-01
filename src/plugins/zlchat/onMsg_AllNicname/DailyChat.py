import asyncio
import os
import random
import re
import time
from typing import Type

from data.Get_dict import dailyChat_dict
from nonebot.adapters.onebot.v11 import (Bot, Message, MessageEvent,
                                         MessageSegment)
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import Replace
from src.utils.log import logger

face_path = f"{config.bot_path}resources/image/zlface"


async def say_hello(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    打招呼
    """
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    random_value = random.randint(0, 10)
    if 0 <= random_value < 8:
        msg = Replace(random.choice(dailyChat_dict.打招呼())
                      ).replace("旅者", f"{nickname}")
    else:
        record_path = f"{config.bot_path}/resources/record/问好"
        record_list = os.listdir(record_path)
        msg = (MessageSegment.record(
            f"file:///{record_path}/{random.choice(record_list)}"))
    return msg


async def say_morning(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    早上好
    """
    random_value = random.randint(0, 10)
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    msg:Message = Message()
    msg = random.choice(dailyChat_dict.起晚了())
    if 4 <= int(time.strftime("%H")) < 7:
        if 0 <= random_value < 8:
            msg = (MessageSegment.reply(event.message_id)+random.choice(dailyChat_dict.起早了()))
        else:
            food_list = [
                "莲子禽蛋羹", "白汁时蔬烩肉", "珍珠翡翠白玉汤", "摩拉肉", "金丝虾球", "仙跳墙"
            ]
            food = random.choice(food_list)
            await onMsg_AllNickname.send(MessageSegment.reply(event.message_id)+"天色未亮，你便出门了吗......今日可有要事在身？")
            await asyncio.sleep(1)
            msg =(MessageSegment.reply(event.message_id)+f"我这恰好多出一份{food}，时间虽紧，{nickname}也别忘了吃早饭。")

    elif 7 <= int(time.strftime("%H")) < 10:
        if 0 <= random_value <=2 :
            await onMsg_AllNickname.send(MessageSegment.reply(event.message_id)+f"早上好，今日{nickname}比昨日稍迟一些？")
            await asyncio.sleep(1.5)
            msg =(MessageSegment.reply(event.message_id)+"明日你可以试着来早一点。朝朝暮夕，彩云流霞，同我去天衡山看云吧。")
        if 2 < random_value <= 4:
            await onMsg_AllNickname.send(MessageSegment.reply(event.message_id)+"来日若是一起前往绝云高地，定要看看霞光万道的景色。落日光景，在何地看，何时看，也是有讲究的。")
            await asyncio.sleep(1.5)
            msg = (MessageSegment.reply(event.message_id)+f"嗯?{nickname}说和何人看也有讲究？")
        else:
            msg = random.choice(dailyChat_dict.早())
    return(Message(msg))

async def say_noon(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    中午好
    """
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    if int(time.strftime("%H")) >= 14:
        msg = random.choice(dailyChat_dict.中午过了())
    elif int(time.strftime("%H")) < 10:
        msg = random.choice(dailyChat_dict.中午没到())

    else:
        msg = random.choice(dailyChat_dict.中午好())
    # msg = Replace(msg).replace("旅者", f"{nickname}")
    return(MessageSegment.reply(event.message_id)+Message(msg))


async def say_afternoon(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    下午好
    """
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    if 19 > int(time.strftime("%H")) >= 13:
        msg = random.choice(dailyChat_dict.下午好())
    else:
        msg = random.choice(dailyChat_dict.不是下午())
    # msg = Replace(msg).replace("旅者", f"{nickname}")
    return(MessageSegment.reply(event.message_id)+Message(msg))


async def say_evening(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    晚上好
    """
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    if 4 > int(time.strftime("%H")) >= 0:
        msg = random.choice(dailyChat_dict.很晚了())
    elif 18 > int(time.strftime("%H")) >= 4:
        msg = random.choice(dailyChat_dict.没到晚上())
    else:
        msg = random.choice(dailyChat_dict.晚上好())
    # msg = Replace(msg).replace("旅者", f"{nickname}")
    return(Message(msg))


async def say_night(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    晚安
    """
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    if 4 > int(time.strftime("%H")) >= 0:
        msg = random.choice(dailyChat_dict.很晚了())
    elif 18 > int(time.strftime("%H")) >= 4:
        msg = random.choice(dailyChat_dict.没到晚上())
    else:
        msg = random.choice(dailyChat_dict.晚安())
    # msg = Replace(msg).replace("旅者", f"{nickname}")
    return(Message(msg))


async def help_me(event: MessageEvent, match_target: str):
    """
    钟离帮我xxx
    """
    data = await UserInfo.get_userInfo(event.user_id)
    friendly_lev = data["friendly_lev"]
    nickname = data["nickname"]
    match_dict: dict = {
        "(.*)(圣遗物|副本|打本)(.*)": [
            "若要获得秘宝，需激活石化古树、地脉之花。旅者树脂是否足够？",
            "传说，所有银白的古树与银白的花的根系在大地的极深处隐秘相连，而原粹树脂联通的痕迹绘制出了地脉的轨迹…"
        ],
        "(.*)口(!|一下|交|一会)?": [
            f"[CQ:image,file=file:///{face_path}/问号.jpg]"
        ]
    }
    msg = random.choice([
        f"{match_target}？这样的要求......嗯，并非不可实现。",
        "我知道了，需要我怎么做？",
        f"{match_target}.....嗯，略知一二，交给我吧",
        "契约已成，如你所愿。"
    ])
    # msg = Replace(send_msg=msg).replace("我", f"{nickname}")
    for pattern in match_dict.keys():
        if re.match(pattern, match_target, re.U):
            msg = random.choice(match_dict[pattern])
    if friendly_lev <= 0:
        msg = random.choice([
            "还需自食其力。",
            "很遗憾，不能。"
        ])
    return(Message(msg))


async def judge_me(onMsg_AllNickname: Type[Matcher], event: MessageEvent, user_id: int):
    """
    钟离认为我怎么样
    """
    fri = (await UserInfo.get_userInfo(user_id))["friendly_lev"]
    if fri <= 0:
        msg = Message(random.choice([
            "......说起来，现在到吃饭的时间了。",
            "不便评价。",
            "钟某不擅评价他人，见谅。"
        ]))
    else:
        record_path = f"{config.bot_path}resources/record/夸旅行者"
        record_list = os.listdir(record_path)
        msg = Message(MessageSegment.record(
            f"file:///{record_path}/{random.choice(record_list)}"))
    return msg


async def make_dinner(onMsg_AllNickname: Type[Matcher], event: MessageEvent, user_id: int):
    """
    做饭
    """
    random_value = random.randint(1, 10)
    if random_value >= 5:
        await onMsg_AllNickname.send("连绵的细雨倒是休止了，趁着天晴去轻策庄踏青顺道采摘些新鲜的竹笋，堂主那孩子，前几天吵闹着想吃我做的腌笃鲜，正好做一份给她过把嘴瘾。")
        await asyncio.sleep(2)
        return("要做好的食物，需静下心来。腌笃鲜，火腿要选用新鲜的清泉镇野猪肉，配着新鲜的笋块，以浓汤调香，如此，加上文火慢炖，方才入味。接下来，就是等着腌笃鲜出锅的时候了。")
    else:
        return("很快雨季就要来了。不妨等雨停了，去轻策庄踏青走走，顺道摘些清脆的竹笋，回来给堂主做份腌笃鲜吧，这孩子，前些时间吵闹着想吃我做的菜了。")


async def zl_hows_it_going(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    近日如何
    """
    nickname = (await UserInfo.get_userInfo(event.user_id))["nickname"]
    random_value = random.randint(0, 10)
    if 0 <= random_value <= 7:
        msg = (random.choice(dailyChat_dict.近日如何())
               )
    else:
        await onMsg_AllNickname.send("今日在茶馆听云先生的新戏，点上一杯清茗，轻呷入口，茶是好茶，戏也是佳作。只是心下仍有些失落。")
        await onMsg_AllNickname.send("两周前我便预定了「明星斋」的古玩，直到今日才上新货。本来想着晚上去拿的，结果店主谈及却说被别人以双倍价格买走了。")
        await asyncio.sleep(2)
        msg = ("那古玩乃是一份茶具，预售价格也仅是五十万摩拉。本来想着拿到再将账单寄到往生堂……现在看来，也不必了。")
    return msg


async def go_with_me(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    钟离我们去xxxx
    """
    nickname = (await UserInfo.get_userInfo(event.user_id))["nickname"]
    fri = (await UserInfo.get_userInfo(event.user_id))["friendly_lev"]
    if fri <= 0:
        msg = random.choice(
            dailyChat_dict.likeZl_lv0()
        )
    else:
        msg = random.choice(
            dailyChat_dict.钟离和我()
        )
    # msg = msg.replace("旅者", f"{nickname}")
    return msg


async def dance(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    钟离跳舞
    """
    nickname = (await UserInfo.get_userInfo(event.user_id))["nickname"]
    if random.randint(1, 10) >= 5:
        msg = Message(random.choice([
            f"{nickname}说笑了，舞蹈并非我强项。",
            "我并非伶人。",
            f"戏曲舞蹈之事，{nickname}当寻云堇先生。",
            "戏曲舞蹈之事，我并不在行",
            f"{nickname}先来一段，如何？",
            f"唉，{nickname}莫再拿我取笑了。",
            f"戏曲舞蹈，当首选云先生。说起来......今晚就有她的表演，{nickname}不一起去看看吗？"
        ],
        ))
    else:
        video_path = f"{config.bot_path}resources/video/dance"
        video_list = os.listdir(video_path)
        vd = random.choice(video_list)
        logger.debug(f"<r>视频是{vd}</r>")
        msg = Message(
            f"[CQ:video,file=file:///{video_path}/{vd},cover=file:///{video_path}/{vd}.jpg]")
        await onMsg_AllNickname.send(Message(msg))
        msg = (Message(random.choice(
            ["真是奇妙，像是在欣赏他人的舞蹈。", f"[CQ:image,file=file:///{face_path}/-737f53f34d737a1e.jpg]这位舞者，模样竟与我这般相似。"])))
    return msg


async def miss_U(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    钟离，我想你了
    """
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    fri = data["all_friendly"]
    if fri <= 0:
        msg = "谢谢。"
    else:
        msg = random.choice(dailyChat_dict.先生我想你())
    # msg = msg.replace("旅者", f"{nickname}")
    return(Message(msg))


async def neineinei(onMsg_AllNickname: Type[Matcher]):
    """
    异世相遇，尽享美味。
    """
    rec_path = f"{config.bot_path}resources/record/zlau"
    await onMsg_AllNickname.send((Message(random.choice(dailyChat_dict.异世相遇()))))
    return(Message(f"[CQ:record,file=file:///{rec_path}/呐呐呐.mp3]"))


async def calm_down(onMsg_AllNickname: Type[Matcher], matcher: Matcher):
    """
    钟离xxx？！
    """
    rd = random.randint(1, 10)
    if rd > 7:
        matcher.stop_propagation()
        await onMsg_AllNickname.send("嗯")
        await asyncio.sleep(1)
        return("各位似乎......有些惊讶？")
    elif 7 >= rd > 4:
        send_msg = random.choice(["不必惊讶，无碍。", "嗯。", "问题不大"])
        return send_msg
    else:
        matcher.stop_propagation()
        return FinishedException


async def zl_sing(event: MessageEvent):
    """
    钟离唱歌
    """
    data = await UserInfo.get_userInfo(event.user_id)
    fri = data["all_friendly"]
    nickname = data["nickname"]
    if fri <= 1:
        msg = random.choice(dailyChat_dict.钟离不唱歌())
    else:
        msg = random.choice(dailyChat_dict.钟离唱歌())
    # msg = msg.replace("旅者", f"{nickname}")
    return(Message(msg))


async def hungry(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    钟离，我饿了
    """
    data = await UserInfo.get_userInfo(event.user_id)
    fri = data["all_friendly"]
    nickname = data["nickname"]
    if fri <= 0:
        msg = Message(MessageSegment.reply(event.message_id) +
                      (f"外面食店不少，{nickname}出去便是。"))
    else:
        rec_path = f"{config.bot_path}resources/record/zlau"
        await onMsg_AllNickname.send(MessageSegment.record(f"file:///{rec_path}/先生饿饿.mp3"))
        await asyncio.sleep(1.5)
        msg = Message(random.choice([
            "而且，我这里还有一些桂花糕。",
            "一起去吧，我请客。",
            f"{nickname}想吃什么？"
        ]))
    return(Message(msg))


async def comfort(event: MessageEvent):
    """
    钟离安慰我
    """
    data = await UserInfo.get_userInfo(event.user_id)
    fri = data["all_friendly"]
    nickname = data["nickname"]
    if fri <= 0:
        msg = Message(MessageSegment.reply(event.message_id)+random.choice([
            "尝试自己解决吧。"
            "心理素质亟待加强。",
            "心理咨询吗......嗯，可以。但需要预约。"
        ]))
    else:
        msg = Message(random.choice([
            "（轻轻抱住)",
            f"走吧，{nickname}，我们一起出去散心。 ",
            f"可是有人欺负了{nickname}？  ",
            f"（轻轻擦去{nickname}的眼泪）",
            f"我在这里。{nickname}若有烦扰之事，可与我详谈。",
            f"{nickname}不必难过。走吧，我陪你出去散散心。",
            f"{nickname}，这是在撒娇吗？"
        ]))
    return(Message(msg))


async def I_pain(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    帝君痛痛，盾盾
    """
    data = await UserInfo.get_userInfo(event.user_id)
    fri = data["all_friendly"]
    nickname = data["nickname"]
    if fri <= 0:
        msg = Message(MessageSegment.reply(event.message_id)+random.choice([
            "尝试自己解决吧。"
            "心理素质亟待加强。",
            "心理咨询吗......嗯，可以。但需要预约。",
            "武艺方面还需精进。",
            "你应该多加锻炼了。",
            "嗯...能力还有所欠缺，稍加练习吧"
        ]))
    else:
        record_path = f"{config.bot_path}/resources/record/安慰你"
        record_list = os.listdir(record_path)
        await onMsg_AllNickname.send(
            MessageSegment.record(
                f"file:///{record_path}/{random.choice(record_list)}")
        )
        msg = Message(random.choice([
            f"是谁伤了{nickname}？",
            f"{nickname}伤在哪了？有无大碍？"]))
    return(Message(msg))


async def zai_ma(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    钟离你还在吗？
    """
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    rec_path = f"{config.bot_path}resources/record/zlau"
    await onMsg_AllNickname.send(
        Message(random.choice(
            [
                f"[CQ:record,file=file:///{rec_path}/欲买桂花同载酒.mp3]",
                f"[CQ:image,file=file:///{face_path}/喝茶沉思.jpg]......"
            ]
        ))
    )
    await asyncio.sleep(1.5)
    msg = random.choice([
        "......啊，抱歉。刚刚说到哪了？",
        "....啊，抱歉。怎么了？",
        ".....嗯？抱歉，走神了。",
        f"{nickname}？"
    ])
    return(Message(msg))


async def kick_me(onMsg_AllNickname: Type[Matcher], event: MessageEvent):
    """
    钟离踢我
    """
    data = await UserInfo.get_userInfo(event.user_id)
    fri = data["all_friendly"]
    nickname = data["nickname"]
    if fri <= 0:
        msg = (MessageSegment.reply(event.message_id)+random.choice([
            "挑衅么？可惜对我没用。"
            "（似乎没有听见）"
        ]))
    else:
        msg = Message(random.choice(dailyChat_dict.kick_me()).replace("旅者", f"{nickname}"))
        msg = (MessageSegment.reply(event.message_id)+msg)
    return(Message(msg))

async def weather(event: MessageEvent):
    """
    根据季节回答
    """
    data = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    if 5 >= int(time.strftime("%m")) >= 3:
        msg = Message(random.choice(
            [
                "璃月这边已然开春，天气渐暖。",
                "最近天气都很好，晴空万里，让人心情愉快。",
                f"璃月近日都有雨，{nickname}可趁此多采一些琉璃袋。",
                "气候渐暖，璃月港这边已落了春雨。",
                "正值春季，是出门踏青的好时节"
            ]
        ))
    elif 8 >= int(time.strftime("%m")) >= 6:
        msg = Message(random.choice(
            [
                f"炎炎夏日，{nickname}记得防暑。",
                f"近日天气很热，{nickname}在外旅行，切忌中暑。"
                
            ]
        ))
    elif 11 >= int(time.strftime("%m")) >= 9:
        msg = Message(random.choice(
            [
                f"秋高气爽，身心舒畅。",
                f"转眼又是秋季，食肆上了新菜，你若有空，去尝尝鲜吧。"
            ]
        ))
    else:
        msg = Message(random.choice(
            [
                f"今年冬雪来得及，若{nickname}有闲暇时日，可温一盅桂花酒，观雪赏景，得闲一时辰。",
                f"近日气候寒冷，{nickname}记得防寒保暖，莫要着凉。"
            ]
        ))
    return(Message(msg))
