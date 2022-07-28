
import random
import re
import time
from calendar import month
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

pic_root_path = f"{config.bot_path}resources/image"
face_path = f"{config.bot_path}resources/image/zlface"
record_path = f"{config.bot_path}resources/record"


async def set_nickname(SetNickname: Type[Matcher], theName, event) -> NoReturn:
    """
    设置用户昵称

    参数：
    * SetNickname: Type[Matcher]
    * theName: 你要设置的昵称
    * event: MessageEvent
    """
    user_id = event.user_id
    name_list = ['钟离', '岩王帝君', '帝君', '钟离先生',
                 '摩拉克斯', '岩王爷', '先生', '离离', '岩神', '岩之神', '丙实']
    data = await UserInfo.get_userInfo(user_id=user_id)
    fri_lev = data["friendly_lev"]
    if theName in name_list:
        send_msg = "意想不到的巧合，旅者是认真的吗？"
        await SetNickname.finish(Message(send_msg))
    name_bool = re.match(
        r'(?i)(.*)(爸|爹|爷|主人|主子|霸霸|达令|宝贝|老婆|老公|老攻|身下|妻|夫|父|官人|爱人|亲爱的|最爱的|外敷|哈斯本|88|wifu|mom|mother|dad|father|grandma|grandpa|love|wife|master)(.*)', str(theName), re.U)
    if name_bool:
        img = [f"[CQ:image,file=file:///{face_path}/-2abbde1d74d75bdb.jpg]",
               f"[CQ:image,file=file:///{face_path}/2db6226a985c2802.jpg]",
               f"[CQ:image,file=file:///{face_path}/微微皱眉.png]"]
        change_value = random.randint(-3, -1)
        await UserInfo.change_frendly(user_id=user_id, change_value=change_value)
        send_msg_list = [f"{theName}？这不合适。",
                         f"{theName}？这可不是一个恰当的称呼......",
                         f"{theName}......其他人也是这样称呼旅者的？",
                         "旅者，别闹了。",
                         "这个点，旅者还未睡醒吗？",
                         f"[CQ:image,file=file:///{face_path}/-6a180a329400175d.jpg]",
                         f"[CQ:image,file=file:///{face_path}/IMG_20220211_180748.jpg]旅者喝点茶，醒醒酒吧。"
                         f"[CQ:image,file=file:///{face_path}/60737a43fdb36a8b.jpg]这样的玩笑，稍欠妥当。"]
        send_msg = random.choice(send_msg_list)+f"\n好感度{change_value}点"
        await SetNickname.finish(Message(random.choice(img)+send_msg))
    if len(theName) > 6:
        send_msg = f"[CQ:image,file=file:///{face_path}/-c760dfdb17238c3.jpg]这么长的名字？那继续称呼旅者似乎也不错......"
        await SetNickname.finish(Message(send_msg))
    if fri_lev <= 1:
        await SetNickname.finish(f"{theName}，是一个好名字。\n（好感等级不足，无法记录昵称。）")
    else:
        await UserInfo.set_username(user_id, theName)
        img = [f"[CQ:image,file=file:///{face_path}/-3fce50624840ebaf.jpg]",
               f"[CQ:image,file=file:///{face_path}/-1148845f9c2f78e1.jpg]",
               f"[CQ:image,file=file:///{face_path}/IMG_20220309_213126.jpg]"]
        send_msg = random.choice(img)+random.choice(
            [
                f"{theName}，以后请多指教。",
                f"{theName}......嗯，是个好名字。",
                f"那么，以后我便以{theName}相称了。",
                f"{theName}？是个不错的名字，我已记下了。",
                f"{theName}......？这个名字，似曾相识。大概是因为我记性太好了吧。",
            ]
        )
        await SetNickname.finish(Message(send_msg))


async def get_nickname(GetNickname: Type[Matcher], bot, event):
    """
    获取用户昵称

    参数：
    * GetNickname: Type[Matcher]
    * bot(Bot): 你要设置的昵称
    * event: MessageEvent

    """
    user_id = event.user_id
    name = await UserInfo.get_userInfo(user_id=user_id)
    name = name.get("nickname")
    if name == "旅者" or name == "" or name is None:
        send_msg = random.choice(dailyChat_dict.stranger())
        send_msg += "\n（钟离似乎还不清楚你的昵称）"
    else:
        send_msg = (
            random.choice(
                [
                    f"怎么了，{name}？",
                    f"我的记性很好，{name}。",
                    f"{name}忘记了自己的名字？",
                    f"{name}，我当然记得你。",
                    f"哪怕是磐岩也会磨损......但我不会忘记你，{name}。",
                    f"[CQ:image,file=file:///{face_path}//IMG_20220131_093220.jpg]{name}是谁呢？",
                    f"[CQ:image,file=file:///{face_path}//与你相识.jpg]我有一位友人，唤作{name}......会是你吗？",
                    f"{name}，这位是我的友人，耳明目慧，机敏过人，绝不会放过视线内任何一个宝箱。",
                    f"{name}为人慷慨，多次为我垫付账单，不胜感激。",
                    f"前段时间有幸认识{name}，见多识广，博学多才。"
                ]
            )
        )
    return send_msg
