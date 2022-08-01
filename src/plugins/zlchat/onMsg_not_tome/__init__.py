import asyncio
import os
import random
import re

from nonebot import on_message, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent, Message,
                                         MessageEvent, MessageSegment)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import MessageEvent_to_text, Replace
from src.utils.log import logger

from data.Get_dict import dailyChat_dict


face_path = f"{config.bot_path}resources/image/zlface"

onMsg_NotTome = on_message(priority=31, block=True)


@onMsg_NotTome.handle()
async def onMsg_NotTome_handle(bot: Bot, event: MessageEvent, matcher: Matcher):
    logger.debug("进入onMsg_onMsg_NotTome")
    event_msg = await MessageEvent_to_text(event)
    user_id = event.user_id
    name = await UserInfo.get_userInfo(user_id=user_id)
    name = name.get("nickname")
    msg: Message = Message()
    nickname = (await UserInfo.get_userInfo(user_id))["nickname"]
    match list(event_msg):
        case["草"]:
            if 98 < random.randint(0, 100):
                msg = random.choice(dailyChat_dict.草())
        case _ if re.match(r'帝君|摩拉克斯|岩王帝君|为了岩王帝君.*', event_msg, re.U):
            msg = random.choice(dailyChat_dict.morax())
        case _ if re.match(r'(.*)(吗|嘛|是吧|是吗)(？|！)?', event_msg, re.U):
            if 95 < random.randint(0, 100):
                msg = random.choice(dailyChat_dict.是吧())
        case _ if re.match(r'(.*)(绝了|真厉害|确实|胚子|真棒)(.*)', event_msg, re.U):
            if 95 < random.randint(0, 100):
                record_path = f"{config.bot_path}resources/record/yes"
                record_list = os.listdir(record_path)
                msg = Message(MessageSegment.record(
                    f"file:///{record_path}/{random.choice(record_list)}"))
                await onMsg_NotTome.finish(msg)
        case _ if re.match(r'(.*)(哈哈哈哈哈哈|好耶)(.*)', event_msg, re.U):
            if 95 < random.randint(0, 100):
                record_path = f"{config.bot_path}resources/record"
                msg = Message(random.choice(
                    ["这么开心？", f"[CQ:image,file=file:///{face_path}/-316a8fded5aa688b.jpg]",
                     f"[CQ:record,file=file:///{record_path}/haha.mp3]"]))
        case ["芜", "湖"]:
            if 95 < random.randint(0, 100):
                await onMsg_NotTome.send("wu...hu....？这声音.....哦，没什么，只是让我想到过去的一种鸟，也是这样的叫声。")
                await asyncio.sleep(2)
                msg = Message("现在嘛……看不见了，大抵是在魔神战争中消亡了。")
        case _ if re.match(r'(.*)老年.*表情(.*)', event_msg, re.U):
            if 65 < random.randint(0, 100):
                msg = Message(random.choice([
                    f"[CQ:image,file=file:///{face_path}/-86488060.jpg]这有何不妥吗？",
                    "这类表情虽然质朴，却很真诚，我认为很合适。",
                    "这类表情......不适合使用吗？"]))
        case _ if re.match(r'.*(?i)(msr|陌生人)', event_msg, re.U):
            msg = Message(random.choice(
                ["看来，这位朋友运气不错。", "这无缘无故的攀比之心，是从何而来啊？", "嗯，品质尚佳。", "心态很重要。", "不要急，放宽心。"]))
        case _ if re.match(r'(.*)(歪了|怎么不强化)(.*)', event_msg, re.U):
            if 85 < random.randint(0, 100):
                msg = Message(random.choice([
                    "人生难免有不顺意之处。走吧，我们出去散散心。",
                    "万事万物皆有平衡，时来运转，下一次会有好运的。",
                    "投机取巧，而非明码标价。如此契约，真算得上公平么？"
                ]))
        case _ if re.match(r'(.*)(?i)(救命|sos)(.*)', event_msg, re.U):
            if 95 < random.randint(0, 100):
                record_path = f"{config.bot_path}resources/record/先生劝架"
                msg = Message(
                    f"[CQ:record,file=file:///{record_path}/这可不妙.mp3]")
        case _ if re.match(r'(.*)(嘶哈|斯哈)(.*)', event_msg, re.U):
            if 70 < random.randint(0, 100):
                msg = Message(random.choice([
                    f"{nickname}的喘息声很厉害，要去不卜庐吗？",
                    f"好重的喘气...{nickname}请在这边躺下，我想检查一下你的胸口",
                    f"嗯...{nickname}呼吸不畅吗？",
                    "这么重的喘息...莫非是业障侵蚀？"
                ]))
        case _ if re.match(r'(.*不.*吃辣.*)', event_msg, re.U):
            if 30 < random.randint(0, 100):
                msg = Message(random.choice([
                    "那吃水晶虾饺吧。",
                    "啊，抱歉。忘记这位不喜辛辣了，是我不周。",
                    "那便吃酒酿圆子吧。",
                    "那便吃翡翠白玉汤吧，较为清淡。",
                    "那便吃莲花稣吧。"
                ]))
        case _ if re.match(r'(.*)(诶嘿|欸嘿|誒嘿|哎嘿)(.*)', event_msg, re.U):
            if 80 < random.randint(0, 100):
                msg = Message(random.choice([
                    "可别给那位酒鬼诗人教坏了。",
                    "那个诗人究竟教了你什么？",
                    "风神这么说，你也便跟着学了去？"
                ]))
        case _ if re.match(r'(.*)魈(.*)(矮|个子不高|小个子)(.*)', event_msg, re.U):
            msg = Message(MessageSegment.reply(event.message_id)+random.choice([
                "你倒是不怕被他怪罪。",
                "心直口快，可不体现在这种时候。",
                "一副化身而已，倒不必如此在意。你这说话习惯，可不能再继续下去了。",
                "说话也是有讲究的，你这样......下不为例。",
                f"{nickname}身长几许？"
            ]))
        case _:
            logger.debug("<y>zlchat全部处理完成，聊天事件结束。</y>")
    try:
        await onMsg_NotTome.finish(Message(msg))
    except ActionFailed:
        raise FinishedException
