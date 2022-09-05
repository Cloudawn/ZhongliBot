import os
import random
import time
from datetime import date

from nonebot.adapters.onebot.v11 import (GroupMessageEvent, Message,
                                         MessageSegment)
from scipy import rand
from src.modules.group_info import GroupInfo
from src.modules.user_attr import UserAttr
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import Replace
from src.utils.log import logger

from .config import FRIENDLY_ADD, GOLD_BASE, LUCKY_GOLD, LUCKY_MAX, LUCKY_MIN

img_path = f"{config.bot_path}resources/image/sign_img"
record_path = f"{config.bot_path}resources/record"


def get_msg():
    msg_dict = {"签到成功":
                ["又见面了，旅者。", "嗯，已将旅者的名字记录下来了。",
                 "旅者来了吗？嗯，去那里写下名字吧。",
                 "我这有一壶刚沏好的龙井，旅者离开之前，不妨品尝一下吧。",
                 "旅者今日看起来心情不错，发生了什么趣事吗？",
                 "把名字签在这吧，旅者。",
                 "旅者，终于来了吗？去写下名字吧。",
                 "旅者来了？时间正好。",
                 "是旅者？今日来得很准时。",
                 "等候多时，这边来吧，旅者"
                 ],
                "很晚了": ["已是深夜，旅者早些休息。",
                        "这个时间还未入睡吗......年轻人身子骨虽硬朗，但也应注意作息规律。",
                        "时候不早，休息吧。"],
                "起早了": [
                    "早......今日这么早？可是有委托？晨光熹微，也好，我同你一起前去。",
                    "是不是第一次看见这样的璃月港？尚未到起床的时候。随我到别处坐坐，静候片刻，一同去吃新月轩的早茶吧",
                    "今日起的这么早？不错，时间正好，去万民堂吃早茶吧。这个点，排队的人还不算多。",
                    "今日也起的这么早，很不错。不知昨晚睡得如何？"
                ],
                "中午好": [
                    "工作了一上午，歇息一会吧。",
                    "午好，吃虎岩有家不错的店，一起去吗",
                    "午好，旅者。",
                    "中午好。最近天气多变，务必注意身体。",
                    "晚上有田先生的说书，《海云山覆雨记》，一起去听吗？",
                    "嗯……已经这个时候了么？也好，一同出去吧。听说新月轩今日上了新菜……"
                ],
                "下午好": [
                    "下午好。晚上去三碗不过港吗？店主改进了「酒酿圆子」的配方，值得尝鲜。",
                    "下午好，稍后一起去吃晚饭吗？",
                    "下午好。接下来想要去哪？",
                    "午后的阳光很美，驻足欣赏片刻吧。"
                ],
                "晚上好": [
                    "晚上好",
                    "夜色正好，旅者如果得空，不如随我在璃月城走走。",
                    "晚上好。稍后有云先生的戏，一起去看看吧。",
                    "月夜花朝，璃月的夜里，灯火映天光。嗯......美不胜收。",
                    "这个时候，璃月的港湾里船皆收帆，白日里人来人往的码头上不见一人，兴许能看见几只偷鱼吃的猫四处窜逃。",
                    "晚上好，旅者。"
                ]
                }
    if 4 > int(time.strftime("%H")) >= 0:
        msg_txt = msg_dict["很晚了"]
    elif 4 <= int(time.strftime("%H")) < 8:
        msg_txt = msg_dict["起早了"]
    elif 11 <= int(time.strftime("%H")) <= 13:
        msg_txt = msg_dict["中午好"]
    elif 13 < int(time.strftime("%H")) <= 18:
        msg_txt = msg_dict["下午好"]
    elif 18 < int(time.strftime("%H")) < 24:
        msg_txt = msg_dict["晚上好"]
    else:
        msg_txt = msg_dict["签到成功"]
    msg_txt = random.choice(msg_txt)
    return msg_txt


async def get_sign_in(user_id: int, event: GroupMessageEvent) -> Message:
    '''
    :说明
        用户签到

    :参数
        * user_id：用户QQ
        * group_id：QQ群号

    :返回
        * Message：机器人返回消息
    '''
    msg = Message(MessageSegment.reply(event.message_id))
    # 获取上次签到日期
    last_sign = await UserInfo.get_last_sign(user_id)
    # 判断是否已签到
    today = date.today()
    if today == last_sign:
        logger.debug(
            f"<g>{user_id}</g> | 签到插件 | 签到失败"
        )
        msg += MessageSegment.text('你已完成今日的签到,现在去休息吧。')
        return msg
    if 4 > int(time.strftime("%H")) >= 0:
        msg_txt = get_msg()
        msg_txt += "\n（时间太晚，明日再来签到吧。）"
        return msg_txt
    # 签到配图
    pic_list = os.listdir(img_path)
    msg_head = MessageSegment.image(
        f"file:///{img_path}/{random.choice(pic_list)}")

    data_name = await UserInfo.get_userInfo(user_id=event.user_id)
    nickname = data_name.get("nickname")
    gold_for_zl = random.randint(500, 700)
    zl_gold = (await UserInfo.get_userInfo(user_id=event.self_id))['all_gold']
    if zl_gold <= 100000:
        gold_for_zl = random.randint(20000, 40000)  # 给钟离发救济款
    await UserInfo.change_gold(event.self_id, gold_for_zl)
    await UserInfo.change_mora(event.self_id, gold_for_zl)

    if random.randint(0, 100) >= 99 and (await UserAttr.get_userAttr(user_id=event.user_id))["version"] == "无":
        version = await UserAttr.change_version(event.user_id)
        msg_txt = f'一枚{version}神之眼掉落在你的手边。'
        msg_txt += Message(
            f"[CQ:image,file=file:///{config.bot_path}resources/image/钟离自拍/{random.choice(['-1ffd8655055b96f9','-20e234d03682f4ba','20275a9eb8f34659'])}.jpg]你得到了岩神的注视。")
        return msg_txt

    data = await UserInfo.sign_in(
        user_id=user_id,
        # group_id=group_id,
        lucky_min=LUCKY_MIN,
        lucky_max=LUCKY_MAX,
        friendly_add=FRIENDLY_ADD,
        gold_base=GOLD_BASE,
        lucky_gold=LUCKY_GOLD)

    await UserAttr.add_exp(user_id=user_id)

    msg_txt = get_msg()
    msg_txt += f'\n原石+{data.get("today_gold")}（总{data.get("all_gold")}）'
    msg_txt += f'\n摩拉+{data.get("today_mora")}（总{data.get("all_mora")}）'
    msg_txt = Replace(msg_txt).replace("旅者", f"{nickname}")
    msg += msg_head+MessageSegment.text(msg_txt)
    return msg


async def reset_sign_nums():
    '''重置签到人数'''
    await GroupInfo.reset_sign_nums()
