# try:
#     import ujson as json
# except ModuleNotFoundError:
import asyncio
import os
import random
import re

from nonebot import on_command, on_message, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (GROUP_MEMBER, Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment,
                                         PrivateMessageEvent)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg, Depends
from nonebot.rule import to_me
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import MessageEvent_to_text, Replace
from src.utils.log import logger

from data.Get_dict import dailyChat_dict

from ..utils import join_list
from .data import (choose_between, husband, lift_up, no_money, repeat_zhongli,
                   say_overworked, wife, zl_sad)

BotNickname = config.nickname
face_path = f"{config.bot_path}resources/image/zlface"

onMsg_tome = on_message(priority=29, rule=to_me(), block=False)


@onMsg_tome.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    event_msg = await MessageEvent_to_text(event)
    user_id = event.user_id
    name = await UserInfo.get_userInfo(user_id=user_id)
    name = name.get("nickname")
    block_bool = False
    nickname = (await UserInfo.get_userInfo(user_id))["nickname"]
    send_msg: Message = Message()
    match list(event_msg):
        case[]:
            send_msg = random.choice(dailyChat_dict.钟离())
        case [*list_str] if "钟离钟离" in join_list(list_str) or "先生先生" in join_list(list_str) or "帝君帝君" in join_list(list_str):
            send_msg = await repeat_zhongli(onMsg_tome, event)
        case [*list_str] if "异梦溶媒" in join_list(list_str):
            send_msg = Message(
                "曾经人们相信灵魂和记忆也是有其质料的。如果曾经有人梦到过天堂，醒来后取出了一朵花，那它应该就是由此构成的。异梦溶媒可以溶解回忆中取得的东西，并且将其变成另一种梦。")
        case _ if re.match(r'(.*)(不(想|要)|帮我)?(上学|上班|上课|工作|作业)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.我不上班()))
        case _ if re.match(r'(.*)(摩拉克斯|岩王帝君)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(["岩之神，摩拉克斯......你曾见过他？", "", ""]))
        case _ if re.match(r'(.*)(魈|夜叉|三眼五显)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.关于魈()))
        case _ if re.match(r'(.*)(胡桃|堂主)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.关于胡桃()))
        case _ if re.match(r'(.*)(云堇|云先生)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.关于云堇()))
        case _ if re.match(r'(.*)(刻晴|玉衡星|阿晴)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.关于刻晴()))
        case _ if re.match(r'(.*)(凝光|天权星)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.关于凝光()))
        case _ if re.match(r'(.*)(甘雨|小美)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.关于甘雨()))
        case _ if re.match(r'(.*)(公子|达达利亚)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.AboutChilde()))
        case _ if re.match(r'(.*)(雷神|巴尔|雷电将军)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.关于雷神()))
        case _ if re.match(r'(.*)(温迪|巴巴托斯)(.*)', event_msg, re.U):
            await onMsg_tome.send("嘶。好浓的酒气。那个诗人刚刚来过吧，那个和风雅二字搭不上一点关系的酒鬼诗人。")
            await asyncio.sleep(1.5)
            await onMsg_tome.send(f"{nickname}这里…唔，被他诱骗着灌了酒话也说不清了么…{nickname}等一下，我去湖一壶「醒神茶」,只需三个时辰便好。")
            await asyncio.sleep(1.5)
            send_msg = Message("你等一下。")
        case _ if re.match(r'(.*)(盐神|赫乌莉亚|赫乌利亚)(.*)', event_msg, re.U):
            send_msg = Message(
                "赫乌莉亚吗？她曾是璃月的诸多魔神之一，是一位很温柔的神，执掌「盐」之权能。但在那个诸神厮杀的年代里，过度的温柔与退让，只会适得其反。")
        case _ if re.match(r'(.*)(若陀|陀子哥)(.*)', event_msg, re.U):
            record_path = f"{config.bot_path}resources/record/若陀"
            record_list = os.listdir(record_path)
            await onMsg_tome.send(MessageSegment.record(f"file:///{record_path}/{random.choice(record_list)}"))
            await asyncio.sleep(1.5)
            send_msg = Message(random.choice(dailyChat_dict.Retuo()))
        case _ if re.match(r'(.*)(自拍|照片|生活照|美照|美图)(.*)', event_msg, re.U):
            pic_path = f"{config.bot_path}resources/image/钟离自拍"
            pic_list = os.listdir(pic_path)
            send_msg = Message(MessageSegment.image(
                f"file:///{pic_path}/{random.choice(pic_list)}"))
        case _ if re.match(r'(.*)(旅途见闻|原神一图|画外旅照|旅行见闻|提瓦特见闻)(.*)', event_msg, re.U):
            pic_path = f"{config.bot_path}resources/image/原神一图"
            pic_list = os.listdir(pic_path)
            send_msg = Message(MessageSegment.image(
                f"file:///{pic_path}/{random.choice(pic_list)}"))
        case _ if re.match(r'(.*)(讲.*笑话|生草)(.*)', event_msg, re.U):
            pic_path = f"{config.bot_path}resources/image/gusha"
            pic_list = os.listdir(pic_path)
            send_msg = Message(MessageSegment.image(
                f"file:///{pic_path}/{random.choice(pic_list)}"))
        case _ if re.match(r'(.*)(我|他|她)摸鱼(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.我不上班()))
        case _ if re.match(r'(,?你?不(上学|上班|工作)|.*摸鱼)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.钟离不上班()))
        case _ if re.match(r'要?想?(.*)还是(.*)', event_msg, re.U):
            A_or_B = re.match(r'(.*)还是(.*)', event_msg, re.U)
            if A_or_B is None:
                send_msg = Message("还是什么？")
            else:
                assert A_or_B is not None
                c_1 = A_or_B.group(1)
                c_2 = A_or_B.group(2)
                send_msg = await choose_between(onMsg_tome, event, c_1, c_2)
        case [*list_str] if "加班" in join_list(list_str):
            send_msg = await say_overworked(onMsg_tome)
        case _ if re.match(r'(.*我)(.*)(老婆|老公|媳妇)(.*)(不|@|是)(.*)', event_msg, re.U):
            raise FinishedException
        case _ if re.match(r'(不)?(.*我)(.*)(老婆|老公|媳妇)(.*)', event_msg, re.U):
            raise FinishedException
        case _ if re.match(r'(.*)(?i)(老婆|妻子|外敷|娘子|wife)', event_msg, re.U):
            send_msg = await wife(onMsg_tome, event)
        case _ if re.match(r'(.*)(?i)(夫君|老公|丈夫|哈斯本|husband)', event_msg, re.U):
            send_msg = await husband(onMsg_tome, event)
        case[*list_str] if "举高高" in join_list(list_str):
            send_msg = await lift_up(onMsg_tome, event)
        case _ if re.match(r'(.*)我(.*)(上学|上班|工作|作业)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.我上班()))
        case _ if re.match(r'(.*)(可爱)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.可爱())
        case _ if re.match(r'(.*)(高冷|冷漠|冷淡)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.高冷()))
        case _ if re.match(r'冷(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.钟离冷()))
        case _ if re.match(r'(.*(天气|今|昨|上午|下午|我|感觉).*)冷(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.身体冷()))
        case _ if re.match(r'(.*(天气|今|昨|上午|下午|我|感觉).*)热(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.body_hot()))
        case _ if re.match(r'(.*)我(.*)(难过|伤心|悲伤|难受|不开心|不快乐|不高兴|郁闷|抑郁)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.不开心())
        case _ if re.match(r'(.*)(会|在)?(难过|伤心|悲伤|难受|不开心|不快乐|不高兴)(吗)?|(.*)(思考|想什么)(.*)', event_msg, re.U):
            send_msg = await zl_sad(onMsg_tome, event)
        case _ if re.match(r'(.*)我(.*)(心情不错|开心|高兴|快乐)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.开心())
        case _ if re.match(r'(.*)(劝架|说.*句话)(.*)', event_msg, re.U):
            record_path = f"{config.bot_path}resources/record/先生劝架"
            record_list = os.listdir(record_path)
            send_msg = Message(MessageSegment.record(
                f"file:///{record_path}/{random.choice(record_list)}"))
        case _ if re.match(r'(.*(天气|今|昨|上午|下午|我|感觉).*)暖和(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.天气暖和()))
        case _ if re.match(r'(.*)(暖和|温暖)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.暖和())
        case _ if re.match(r'(.*)(去哪|要去哪)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.where_to_go())
        case _ if re.match(r'(.*)(多少岁|年龄|芳龄|贵庚|岁数)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(["我在这世间，已度过六千余岁。",
                                              "大概六千余岁。活得太久的人，只能在记忆中寻访往昔的战友，过去的景色。",
                                              "如要细数，约六千一百零九吧。"]))
        case _ if re.match(r'(.*)(?i)(老师|教师|三三|sense)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.钟离老师())
        case _ if re.match(r'(.*)(喝酒|饮酒)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.钟离喝酒())
        case _ if re.match(r'(.*)(原神)(.*)', event_msg, re.U):
            await onMsg_tome.send("凡人的愿望足够强大，强大到获得神明的注视，便会获得「神之眼」，而「神之眼」的拥有者，则被称为「原神」。")
            send_msg = Message(
                "据说，「原神」拥有登上天空岛的资格。而对于凡人来说，「原神」则是那些获得神明青睐的强者。")
        case _ if re.match(r'(.*)(摩拉|钱|买单)(.*)', event_msg, re.U):
            send_msg = await no_money(event)
        case _ if re.match(r'(.*)有(.*深意)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.有何深意())
        case _ if re.match(r'(.*)(喷水)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                ["抱歉，我似乎不是这个品种的龙。", "呼风唤雨。", "84消毒。", "这个龙头形状的小标志是什么？"]))
        case _ if re.match(r'，?你?(.*)(做了什么|干了什么)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.where_went()))
        case _ if re.match(r'，?你?(在哪)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                [f"[CQ:image,file=file:///{face_path}/IMG_20210928_182836.jpg]怎的，{nickname}可是在明知故问？", f"[CQ:image,file=file:///{face_path}/-3b1881067b11fa59.jpg]大概在{nickname}面前。"]))
        case _:
            # 没抓住
            block_bool = True
    if block_bool:
        # send_msg = Message("onMsg_tome 没抓住")
        logger.debug("<blue>onMsg_tome处理失败，进入onMsg_AllNickname</blue>")
    else:
        matcher.stop_propagation()
        send_msg = Replace(send_msg).replace("旅者", f"{name}")
    try:
        await onMsg_tome.finish(Message(send_msg))
    except ActionFailed:
        logger.debug("<y>onMsg_tome消息为空</y>")

# __all__ = ["onMsg_tome"]
