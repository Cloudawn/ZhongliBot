import asyncio
# try:
#     import ujson as json
# except ModuleNotFoundError:
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

# from src.utils.function import Replace

pic_root_path = f"{config.bot_path}resources/image"
face_path = f"{config.bot_path}resources/image/zlface"
record_path = f"{config.bot_path}resources/record"


async def answer_like(event: MessageEvent, event_msg: str, mat_tar: str):
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    fri_lv = data["friendly_lev"]
    msg = Message(random.choice([
        "自然是喜欢的。",
        "是的。",
        f"{nickname}认为我喜欢吗？",
        f"嗯。那{nickname}喜欢吗？",
        f"[CQ:image,file=file:///{config.bot_path}resources/image/zlface/6120d2a44ecd5c0b.png]不太好说。",
        "",
        "",
        "",
        "",
        ""
    ]))
    if re.match(r'(.*)希望(.*)', event_msg, re.U):
        msg = Message("谢谢，我很喜欢")
        return(Message(msg))

    elif re.match(r'(我(.*)(喜欢|心悦|爱|心里有)你(.*)|.*我?.*贴贴.*)', event_msg, re.U):
        if fri_lv <= 0:
            msg = random.choice(dailyChat_dict.likeZl_lv0())
        elif 0 < fri_lv <= 1:
            msg = random.choice(dailyChat_dict.likeZl_lv1())
        elif 1 < fri_lv <= 2:
            if random.randint(0, 10) > 3:
                msg = random.choice(dailyChat_dict.likeZl_lv2())
            else:
                record_path = f"{config.bot_path}resources/record/中等好感吃桃"
                record_list = os.listdir(record_path)
                msg = Message(MessageSegment.record(
                    f"file:///{record_path}/{random.choice(record_list)}"))
        elif 2 < fri_lv:
            if random.randint(0, 10) > 3:
                msg = random.choice(dailyChat_dict.likeZl_lv3())
            else:
                record_path = f"{config.bot_path}resources/record/高好感吃桃"
                record_list = os.listdir(record_path)
                msg = Message(MessageSegment.record(
                    f"file:///{record_path}/{random.choice(record_list)}"))
        else:
            ...
        return(Message(msg))

    elif re.match(r'(.*)(什么|谁)(.*)', mat_tar, re.M | re.I):
        msg = random.choice(dailyChat_dict.zl_LikeWhat())
        return(Message(msg))

    elif re.match(rf'^(我|{nickname})$', mat_tar, re.U):
        if fri_lv <= 0:
            msg = Message("并非如此。")
        else:
            msg = MessageSegment.reply(
                event.message_id) + Message(random.choice(dailyChat_dict.钟离喜欢我吗()))
        return(Message(msg))
    match_dict: dict = {
        "(.*)(海鲜|触手)(.*)": [
            "我不喜欢海鲜。那种滑溜溜的触感，洗不净的腥味......"
        ],
        "(.*)(射|奶|乳|插|后入|淦|艾草|茎叶)(.*)": [
            f"[CQ:image,file=file:///{face_path}/问号.jpg]",
            "唔.......",
            f"[CQ:image,file=file:///{face_path}/思索.png]......"
            ""
        ]
    }
    # if re.match(r'(.*)(海鲜|触手)(.*)', mat_tar, re.U):
    #     msg = Message("我不喜欢海鲜。那种滑溜溜的触感，洗不净的腥味......")
    for pattern in match_dict.keys():
        if re.match(pattern, mat_tar, re.U):
            msg = random.choice(match_dict[pattern])
    return(Message(msg))


async def answer_MA(user_id: int, match_target: str):
    data = await UserInfo.get_userInfo(user_id)
    nickname = data["nickname"]
    match_dict: dict = {
        "(.*)(好吃)(.*)": [
            "味道不错。",
            "不论口感还是滋味，均为一流。",
            "是的。如果想品尝，下次我为旅者带一份便是。",
            "很不错。",
            "用料讲究，做法地道。属实不易。"
        ],
        "(.*)口(!|一下|交|一会)?": [
            f"[CQ:image,file=file:///{face_path}/问号.jpg]"
        ],
        "(.*)(到家|回家)(.*)": [
            "嗯，是的。",
            "还没有，今日委托比以往更多。",
            "璃月的土地上，处处皆是归宿。"
        ],
        "(去.*)": [
            "嗯，之后去。",
            "暂时没有这个打算。",
            "要务缠身，只能他日启程了。",
            "这么说来，现在刚好得空，可以出发。",
            f"嗯，{nickname}一起吗？"
        ],
        f"(.*{nickname}要.*)": [
            f"这需视{nickname}自身情况而定。"
        ],
        f"(.*{nickname}.*)": [
            ""
        ],  # 阻断匹配目标中含有“我”的内容
        "(.*了.*)": [
            f"嗯，已经{match_target}。",
            f"还没有，之后吧。{nickname}{match_target}吗？",
            "",
            "",
            "",
            ""
        ],  # match_target的内容是xxx了
        "(.*)(睡|睡觉|睡了)(.*)": [
            "还没有。怎么了？",
            "还没有。你已打算歇下了吗？",
            "这个时间，也可以休息了。",
            "显而易见，我醒着。",
            "......嗯？啊，抱歉，有些困乏。这些日子，总感到疲惫。即便是磐石......也会被磨损罢。",
            f"[CQ:image,file=file:///{pic_root_path}/钟离自拍/83873FAFBA6AD693779C7C5BAD729C1F.jpg]"
        ]
    }
    msg = random.choice(
        [random.choice(dailyChat_dict.是吧()), "", "", "", "", ""])
    for pattern in match_dict.keys():
        if re.match(pattern, match_target, re.U):
            msg = random.choice(match_dict[pattern])
    # msg = msg.replace("旅者", f"{nickname}")
    return(Message(msg))


async def answer_think(user_id: int, match_target: str):
    data = await UserInfo.get_userInfo(user_id)
    nickname = data["nickname"]
    if re.match("(.*)我怎么(.*)", match_target, re.U):
        record_path = f"{config.bot_path}resources/record/夸旅行者"
        record_list = os.listdir(record_path)
        msg = Message(MessageSegment.record(
            f"file:///{record_path}/{random.choice(record_list)}"))
        # return(msg)
    else:

        msg = Message(random.choice([
            "要想公正评判，其实并不容易。",
            f"我想听听{nickname}的见解。",
            f"{nickname}心中已早有定论，特地前来问我，是为何啊？",
            "这倒是不知如何回答......",
            "我的看法......其实无足轻重，不必在意。",
            f"{nickname}有何高见？",
            f"好了，{nickname}莫执着于我的看法了。",
            f"{nickname}如何看待？",
            f"我觉得......嗯，还是交由{nickname}评判吧。"
        ]))

    return(Message(msg))


async def answer_will_u(event: MessageEvent, match_target: str):
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]

    msg = random.choice([
        "略通一二。",
        f"{match_target}？或许能试试。",
        "嗯，是的。",
        f"{match_target}......大概不会",
        f"哦？那{nickname}认为......会吗？",
        f"[CQ:image,file=file:///{face_path}/IMG_20211111_195149.jpg]......",
        f"[CQ:image,file=file:///{face_path}/lofter_1642691135289.jpg]......",
        f"[CQ:image,file=file:///{face_path}/1632014114208.jpeg]",
        "",
        ""
    ])
    # for pattern in match_dict.keys():
    #     if re.match(pattern, match_target, re.U):
    #         msg = random.choice(match_dict[pattern])
    # msg = Replace(msg).replace("我", f"{nickname}").replace(
    #     "钟离", "我").replace("旅者", f"{nickname}")
    return(Message(msg))


async def answer_can_u(event: MessageEvent, match_target: str):
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    msg: Message = Message()
    fri_lev = data["friendly_lev"]
    fri_dict: dict = {
        "0": [
            "不可以。",
            "不能。",
            "大概不可以。"
        ],
        "1": [
            "抱歉，大概不行。",
            "这是何意？",
            "唔，可以再具体说说吗？",
            "乍一听也没什么，但以普遍理性而论，这或许不太合适。",
            f"{nickname}，你可是在说笑？"
        ],
        "2": [
            "或许可以。",
            "说来听听。 ",
            "我能帮得上忙。",
            "嗯，我明白了。需要我怎么做？",
            f"凡是「契约」之内的事，{nickname}皆可与我详谈。",
            f"[CQ:image,file=file:///{face_path}/伸手.png]乐意效劳。"
        ],
        "3": [
            "乐意之至。",
            f"需要帮忙的话，{nickname}唤我便是。",
            f"当然可以，{nickname}。",
            f"{nickname}下次不必询问，直接找我便可。",
            f"[CQ:image,file=file:///{face_path}/1632014123919.jpg]乐意效劳。"
        ],
        "4": [
            f"当然。{nickname}为何现在才来找我？",
            f"当然可以，毕竟是你，{nickname}。",
            f"来吧，事不宜迟。",
            f"「契约」之外的事,{nickname}也可同我商量，毕竟，凡事我都略知一二。",
            f"乐意之至。不过，虽说如此，我也有希望{nickname}做的事。毕竟，这才符合「公平」。"
        ],
        "5": [
            f"当然。{nickname}为何现在才来找我？",
            f"当然可以，毕竟是你，{nickname}。",
            f"来吧，事不宜迟。",
            f"「契约」之外的事，{nickname}也可同我商量，毕竟，凡事我都略知一二。",
            f"乐意之至。不过，虽说如此，我也有希望{nickname}做的事。毕竟，这才符合「公平」。"
        ]
    }
    msg = Message(random.choice(fri_dict[str(fri_lev)]))
    msg = Message(MessageSegment.reply(event.message_id)+msg)
    return(Message(msg))


async def answer_have(event: MessageEvent, match_target: str):
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    match_dict: dict = {
        "(空.*)": [
            "卸职以后，乐得清闲。",
            "这点闲暇还是有的。",
            f"怎么，{nickname}也想出去走走吗？",
            "难得闲暇，出门闲游吧。"
        ]
    }
    msg = random.choice([
        f"是的。{nickname}想了解哪一部分？",
        "这么一问.......一时半会不知从何谈起。稍等，容我整理思绪。",
        f"有的，{nickname}若感兴趣，我们可移步详谈。",
        "嗯，有。但......抱歉，不知要从何说起，我的记忆，或许也不如从前了。",
        f"或许有吧。{nickname}想听吗？",
        f"或许没有。怎么，{nickname}很感兴趣吗？"
    ])
    for pattern in match_dict.keys():
        if re.match(pattern, match_target, re.U):
            msg = random.choice(match_dict[pattern])
    return(Message(msg))


async def answer_be_your(event: MessageEvent, match_target: str):
    """
    做钟离的xxxx，或者让钟离做你的xxx
    """
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    fri_lev = data["friendly_lev"]
    if fri_lev <= 0:
        msg = random.choice([dailyChat_dict.likeZl_lv0()])
        return msg

    match_dict: dict = {
        "(.*)(友)(.*)": [
            f"{nickname}，你我本是友人。",
            f"{nickname}，你当然是我的友人。"
        ]
    }
    msg = random.choice([

        f"做{match_target}？嗯......成立契约吗？若是如此，效力、日期、条件、报酬......诸多细节，你我还需细细磋商。",
        f"做{match_target}？",
        f"做{match_target}？这......可否详述？",
        f"[CQ:image,file=file:///{face_path}/IMG_20211007_143441.png]",
        f"[CQ:image,file=file:///{face_path}/1626933670146.png]",
        f"嗯......我可以答应你。不过，{nickname}需要拿出相等的筹码。"
    ]
    )
    for pattern in match_dict.keys():
        if re.match(pattern, match_target, re.U):
            msg = random.choice(match_dict[pattern])
        return(Message(msg))


async def answer_are_you(event: MessageEvent, match_target: str):
    """
    钟离是xxx
    """
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]
    match_dict: dict = {
        "(.*)(生日|生辰)(.*)": [
            "12月31日，正是岁末。"
        ],
        "(.*多少.*)": [
            "该如何回答呢......",
            f"{nickname}想了解哪一方面？",
            "不才，难以解答。",
            "今日如此求知若渴？"
        ],
        "(.*)(女|娘|淫|批)(.*)": [
            f"[CQ:image,file=file:///{face_path}/问号.jpg]",
            "唔.......",
            f"[CQ:image,file=file:///{face_path}/思索.png]......"
            ""
        ]
    }
    msg = random.choice(
        [random.choice(
            dailyChat_dict._assert()), "", ""])  # 30%的几率回复
    for pattern in match_dict.keys():
        if re.match(pattern, match_target, re.U):
            msg = random.choice(match_dict[pattern])
    # msg = msg.replace("旅者", f"{nickname}")
    return(Message(msg))


async def I_want(event: MessageEvent, match_target: str):
    data = await UserInfo.get_userInfo(event.user_id)
    nickname = data["nickname"]

    msg = random.choice([
        f"{match_target}？为何？",
        f"可以，需要为{nickname}做些什么吗？",
        f"{match_target}？嗯...有些难办。",
        f"{nickname}请便。"
    ]).replace("你", "我").replace("钟离", "我")

    return(Message(msg))


async def answer_judge(event: MessageEvent, match_target: str):
    if random.randint(0, 10) > 7:
        msg = random.choice(
            dailyChat_dict.judge()
        )
        # .replace("你", "我").replace("钟离", "我")

        return(Message(msg))
