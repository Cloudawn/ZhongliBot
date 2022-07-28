import asyncio
# try:
#     import ujson as json
# except ModuleNotFoundError:
import random
import re
import time
from calendar import month
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
from src.utils.function import Replace

from ..utils import join_list

pic_root_path = f"{config.bot_path}resources/image"
face_path = f"{config.bot_path}resources/image/zlface"
record_path = f"{config.bot_path}resources/record"


async def momo(touch_part, event: MessageEvent):
    user_id = event.user_id
    data = await UserInfo.get_userInfo(user_id)
    fri_lev = data["friendly_lev"]
    nickname = data["nickname"]
    pic_path = f"{config.bot_path}resources/image/zlface"
    if fri_lev <= 0:
        send_msg = MessageSegment.reply(
            event.message_id)+Message(random.choice(dailyChat_dict.likeZl_lv0()))
    else:
        reply_list = [
            f"（你尝试把手放在先生{touch_part}上，他避开了）",
            f"我的{touch_part}......有何异常吗？",
            f"触碰{touch_part}，是有特殊含义吗？",
            f"(钟离注视着你的动作，面露不解)",
            "你的手很凉，披上外套吧",
            "......好了，把手放下吧",
            f"{nickname}，可否停下？",
            f"{touch_part}处于我而言……{nickname}可否不要闹了？",
            f"[CQ:image,file=file:///{pic_path}/IMG_20210928_182858.jpg]{nickname}的手很凉，披上外套吧"
        ]
        send_msg = MessageSegment.reply(
            event.message_id)+Message(random.choice(reply_list))
    return send_msg


async def momo_me(touch_part, event: MessageEvent):
    user_id = event.user_id
    data = await UserInfo.get_userInfo(user_id)
    fri_lev = data["friendly_lev"]
    nickname = data["nickname"]
    if fri_lev <= 0:
        send_msg = MessageSegment.reply(
            event.message_id)+Message(random.choice(dailyChat_dict.likeZl_lv0()))
    elif fri_lev <= 2:
        send_msg = MessageSegment.reply(
            event.message_id)+Message(random.choice(["这不合适。", f"{nickname}虽同我为契约之交，但也需注意分寸。"]))
    else:
        pic_path = f"{config.bot_path}resources/image/zlface"
        reply_list = [
            f"{touch_part}不舒服吗？",
            "为何？",
            "那......冒犯了。",
            "可以，但此举有何特殊含义？愿闻其详。",
            f"触摸{touch_part}......这里吗？",
            f"好吧。触碰{touch_part}，这个位置，对吗？",
            f"嗯，已经触碰到{touch_part}了......那么接下来呢？",
            f"[CQ:image,file=file:///{pic_path}/IMG_20211216_100109.jpg]今年多高了？",
            f"{nickname}，可否不要闹了？"
        ]
        send_msg = MessageSegment.reply(
            event.message_id)+Message(random.choice(reply_list))
    return send_msg


async def repeat_users(onCmdRepeat: Type[Matcher], event: MessageEvent, userWords):
    nickname = (await UserInfo.get_userInfo(event.user_id))["nickname"]
    random_value = random.randint(0, 10)
    userWords = Replace(userWords).replace("我", f"{nickname}")
    if 0 <= random_value <= 3:
        await onCmdRepeat.finish(userWords)
    elif 3 < random_value <= 6:
        await onCmdRepeat.send(userWords)
        await asyncio.sleep(1.5)
        await onCmdRepeat.finish(Message(random.choice(dailyChat_dict.学词警告())))
    else:
        await onCmdRepeat.finish(Message(random.choice(dailyChat_dict.学词警告())))


async def zl_eat(eat: Type[Matcher], bot: Bot, event: MessageEvent, food: Message):
    user_id = event.user_id
    nickname = (await UserInfo.get_userInfo(user_id))["nickname"]
    food_text = food.extract_plain_text()
    match_dict: dict = {
        ".*吗.*":
        [f"那有劳{nickname}来一份吧，多谢。",
         f"我暂时不觉饥渴，{nickname}自便吧。"
         ],
        "(.*)(了吗|饭|什么|啥|哪)(.*)": [
            f"嗯...听说{nickname}喜食桃子，那么我们去吃桂酒酿桃如何？",
            f"{nickname}若能吃辣，我想万民堂水煮鱼不错。",
            "文火慢炖腌笃鲜，如何？",
            "黄金蟹如何？",
            f"琉璃亭新推出了文思豆腐，{nickname}要一起去吗？",
            f"唔，一位须弥的朋友给我带了...嗯，应该是叫“QQㄋㄟㄋㄟ好喝到咩噗茶”？或许{nickname}会喜欢。",
            "今天香菱掌勺，吃翡玉什锦袋吧。",
            "今日吃的是「文火慢炖腌笃鲜」。火腿用的是月海亭盛宴标准的火腿部位，竹笋则是轻策庄笋节紧密的春笋。",
            "今日吃的是万民堂水煮鱼。此时正是绝云椒收获的好季节，可不能错过尝鲜。",
            "今日吃的是甘雨送来的「四方和平」，劳她费心了。",
            "嗯....公子在万民堂炫耀了几番厨艺，做了「极致一钓」......但幸好往生堂来了委托，我离开得很及时。",
            "今日吃的是魈送来的「美梦」。那孩子......",
            "胡堂主做了......呃，似乎叫「幽幽大行军」的食品，唉。好在我的身体不同于常人。",
            "偶遇了香菱小姐，尝了她做的新菜，似乎叫....「大红莲麻辣火史莱姆」?",
            "与凝光洽谈时，有幸尝到了她做的「乾坤摩拉肉」。",
            "玉衡星亲手制作了「绝地求生烤鱼」，微焦的鱼皮包裹着香酥的鱼肉，程度恰到好处，着实美味。",
            f"{nickname}稍后一起去琉璃亭吗，今天公子会请客。",
            "这么一说，确实到吃饭的时间了。",
            "嗯，已经吃过了。",
            "坦诚而言，我今天没有这个打算。胡堂主掌勺...唉。",
            "正好，一同去万民堂，如何？",
            "暂定新月轩，这次我来请客吧。",
            "时节正好，理应出去走走，等一桌好菜。",
            "这家「三碗不过港」也是璃月的百年老字号了，且不提其他吃食味道如何，食肆中的酒酿圆子，可是不少璃月人常点的小吃。",
            f"酒酿圆子，捏成的芝麻团子加入特制的米酒，形成这般独特的滋味，名虽带酒，却并无多少酒味。不论孩童老叟，都可食用。{nickname}，不如你也来尝尝？"
        ],
        "(.*)(海鲜|大便|粑粑|测试|鱼|🐟|虫|蟑)(.*)": [
            f"[CQ:image,file=file:///{face_path}/1653722464376.png]不用，你留着吧。",
            f"[CQ:image,file=file:///{face_path}/1653722464376.png]我不饿。",
            f"[CQ:image,file=file:///{face_path}/1653722464376.png]谢谢，不必。",
            f"[CQ:image,file=file:///{face_path}/1653722464385.jpg]"
        ],
        "(.*)(先生|钟离|我|你|@|丙|帝君|石|客卿|刻晴|魈|达达利亚|公子|若陀)(.*)": [
            "这怎么可能呢？",
            f"旅者对食物的概念，着实新颖。",
            "......在我看来，这个并非食物",
            "这个......可以吃吗？"
        ],
        "(.*)醋(.*)": [
            f"[CQ:image,file=file:///{face_path}/177561472ca84c75.jpg]没有。",
            f"[CQ:image,file=file:///{face_path}/20220312_135409.jpg]没有。"
        ]
    }
    msg = random.choice([
        f"要请我品尝{food_text}？嗯，谢谢{nickname}，有劳",
        f"嗯...{food_text}，味道很不错",
        f"{food_text}，嗯...奇妙的口感",
        f"(细细品尝{food_text})",
        "多谢好意，不过我现在不饿",
        f"{food_text}给你吃吧，我暂且不饿",
        f"嗯.....{nickname}先尝一口{food_text}，如何？",
        f"{food_text}......嗯，着实美味，多谢款待。",
        "盛情难却，那我便不推辞了。"
    ])
    for pattern in match_dict.keys():
        if re.match(pattern, food_text, re.U):
            msg = random.choice(match_dict[pattern])
    return (MessageSegment.reply(event.message_id)+Message(msg))
