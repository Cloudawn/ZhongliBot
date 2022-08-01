import asyncio
# try:
#     import ujson as json
# except ModuleNotFoundError:
import json
import os
import random
import re

from data.Get_dict import dailyChat_dict
from nonebot import on_message, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (GROUP_MEMBER, Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import (MessageEvent_to_text, Replace,
                                custom_forward_msg)
# from nonebot.internal.matcher import Matcher
from src.utils.log import logger
from src.utils.rule import all_nickname

from ..utils import join_list
from .DailyChat import (I_pain, calm_down, comfort, dance, go_with_me, help_me,
                        hungry, judge_me, kick_me, miss_U, neineinei,
                        say_afternoon, say_evening, say_hello, say_morning,
                        say_night, say_noon, weather, zai_ma, zl_hows_it_going,
                        zl_sing)
from .LoveDate import date_with_zl, hand_in_hand, hug, kiss, treat_user
from .Q_A import (I_want, answer_are_you, answer_be_your, answer_can_u,
                  answer_have, answer_judge, answer_like, answer_MA,
                  answer_think, answer_will_u)
from .SpecialDay import (BegAttention, Lantern_Ftvl, ToUser_HappyBirthday,
                         Tozl_HappyBirthday, ZhuYue_Ftvl)

# 钟离部分文案（包括故事、早晚安、进群欢迎）来自lof同人作者 [@阿辰不会写刀](https://whz0508.lofter.com)，禁止抄袭或无授权更改引用。

BotNickname = config.nickname  # 是一个列表
NICKNAME = "钟离"

onMsg_AllNickname = on_message(priority=30, rule=all_nickname, block=False)
onRe_AllNickname = on_regex(
    r'(.*)我请你|(请|我?.*给)(.*)(先生|钟离|帝君|离离)(吃|喝|买|付钱|付款|付账)(.*)|(听戏|散步|赏花|遛鸟|说书|喝茶)(.*)',
    priority=26, rule=all_nickname, block=True)

face_path = f"{config.bot_path}resources/image/zlface"


@onRe_AllNickname.handle()
async def onRe_AllNickname_handle(bot: Bot, event: MessageEvent, matcher: Matcher):
    event_msg = await MessageEvent_to_text(event)
    msg = await date_with_zl(onMsg_AllNickname, event, matcher, event_msg)
    await onRe_AllNickname.finish(msg)


@onMsg_AllNickname.handle()
async def AllNickname_handle(bot: Bot, event: MessageEvent, matcher: Matcher):
    logger.debug("进入onMsg_AllNickname")
    event_msg = await MessageEvent_to_text(event)
    user_id = event.user_id
    name = await UserInfo.get_userInfo(user_id=user_id)
    name = name.get("nickname")
    send_msg: Message = Message()
    block_bool = False
    nickname = (await UserInfo.get_userInfo(user_id))["nickname"]
    match list(event_msg):
        case["？"]:
            send_msg = await zai_ma(onMsg_AllNickname, event)
        case[*list_str] if "涨价" in join_list(list_str) or "奸商" in join_list(list_str):
            send_msg = random.choice(dailyChat_dict.奸商())
        case _ if re.match(r'你?是?(谁|哪位)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.自我介绍())
        case _ if re.match(r'(.*)(石珀|岩石之心)(.*)', event_msg, re.U):
            send_msg = Message("石珀乃极纯的岩元素凝成的珍稀晶石，常与其他矿物伴生，通体金光，光彩夺目。")
        case _ if re.match(r'(.*夜泊石.*)', event_msg, re.U):
            send_msg = Message(
                "夜泊石乃稀有的特质矿石，在静谧的暗夜里会幽幽地发光。据称是天地间奔流的元素在异变中凝聚成的珍奇宝石。")
        case[*list_str] if "🤤" in join_list(list_str) or "🥵" in join_list(list_str):
            send_msg = random.choice(dailyChat_dict.流汗())
        case _ if re.match(r'(.*)(喊我老公|喊我老婆)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.call_wife())
        case _ if re.match(r'(.*)(成精)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                ['确实。', '说笑了', '没有的事，怎么会呢。', '不无可能。']))
        case _ if re.match(r'(^早$|早啊)|((.*)(早上好|早安|日安|晨愉|上午好)(.*))', event_msg, re.U):
            send_msg = await say_morning(onMsg_AllNickname, event)
        case [*list_str] if "负责" in join_list(list_str):
            send_msg = Message("负责？何故说出这种话？")
        case _ if re.match(r'(.*)(下午好)(.*)', event_msg, re.U):
            send_msg = await say_afternoon(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(中午好|晌午好|午好)(.*)', event_msg, re.U):
            send_msg = await say_noon(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(晚上好|夜美|晚好)(.*)', event_msg, re.U):
            send_msg = await say_evening(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(晚安|夜安)(.*)', event_msg, re.U):
            send_msg = await say_night(onMsg_AllNickname, event)
        case _ if re.match(r'^((好|你好|您好|欢迎)|(在吗|在不在))(!|呀|啊|？)?$', event_msg, re.U):
            send_msg = await say_hello(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(谢谢|多谢|感谢)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.谢谢先生())
        case[*list_str] if "品种" in join_list(list_str):
            send_msg = Message("我以凡人「钟离」的身份游走于这世间。")
        case _ if re.match(r'(.*)我(.*)(下班|下课|放学|回来)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.我回来())
        case _ if re.match(r'(.*)(对不起|我错了|原谅我)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.对不起())
        case _ if re.match(r'(.*)(掉线|坏了|坏掉了|想下班|摸鱼)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.钟离不上班())
        case _ if re.match(r'(.*)我(不.*理你)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.不理你())
        case _ if re.match(r'(.*)我(.*)(难受|不舒服|难受|痛|疼|受伤|肿|发烧|感冒|生病)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.我难受())
        case _ if re.match(r'(.*)我(.*)(你.*粉丝)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.我是钟离粉丝())
        # case _ if re.match(r'我(生日|生辰|诞辰)', event_msg, re.U):
        #     send_msg = Message(MessageSegment.reply(
        #         event.message_id)+f"旅者哪一天生日？")
        case _ if re.match(r'(.*)我今天(生日|生辰|诞辰)(.*)|(.*)今天(.*)我(.*)(生日|生辰|诞辰)(.*)', event_msg, re.U):
            send_msg = await ToUser_HappyBirthday(onMsg_AllNickname)
        case _ if re.match(r'.*(生日|生辰|诞辰).*快乐.*', event_msg, re.U):
            send_msg = await Tozl_HappyBirthday(onMsg_AllNickname)
        case[*list_str] if re.match(r'(.*)(元宵|大年)(.*)(好|快乐)(.*)', event_msg, re.U):
            send_msg = await Lantern_Ftvl(event, onMsg_AllNickname)
        case[*list_str] if re.match(r'(.*)(不说话|不回我|理我|看看我)(.*)', event_msg, re.U):
            send_msg = await BegAttention(onMsg_AllNickname)
        case _ if re.match(r'(.*)你?没事(吧|啊)？?(.*)', event_msg, re.M | re.I):
            send_msg = Message(random.choice(["嗯，没事", "没事", "......没事。"]))
        case _ if re.match(r'(.*)(欺负我|痛捅)(.*)', event_msg, re.M | re.I):
            send_msg = await I_pain(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)什么意思(.*)', event_msg, re.M | re.I):
            send_msg = random.choice(dailyChat_dict.什么意思())
        case _ if re.match(r'(.*我不(.*)(喜欢|心悦|爱)|.*我(恨|讨厌))你(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.讨厌先生()))
        case _ if re.match(r'(.*)(不喜欢|讨厌)(.*)(什么|哪|谁)(.*)', event_msg, re.U):
            send_msg = Message(MessageSegment.record(
                f"file:///{config.bot_path}resources/record/zlau/讨厌触手.mp3"))
        case _ if re.match(r'(.*)(结婚|嫁|娶|领证|爱人|喜欢的人)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.钟离不结婚())
        case _ if re.match(r'(.*)(喜欢|爱|欣悦|心里有|贴贴)(.*)吗?', event_msg, re.U):
            pattern = re.match(r'(.*)(喜欢|爱|欣悦|心里有|贴贴)(.*)吗?', event_msg, re.U)
            assert pattern is not None
            mat_tar = pattern.group(3).replace("我", f"{nickname}")
            send_msg = await answer_like(event, event_msg, mat_tar)
        case _ if re.match(r'(.*)(色色|涩图|涩涩|瑟瑟|色图)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.色色())
        case _ if re.match(r'(.*)(请我吃|给我买|请客)(.*)', event_msg, re.U):
            send_msg = await treat_user(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(呆毛|呆在|发呆)(.*)', event_msg, re.U):
            raise FinishedException
        case _ if re.match(r'(.*)(((我.*被你.*气|把我.*气|气到我)|我(.*)(得罪|惹)你))(.*)', event_msg, re.U):
            send_msg = MessageSegment.reply(
                event.message_id) + Message(random.choice(dailyChat_dict.我生气()))
        case _ if re.match(r'(.*)(不.*聪明|呆|傻|笨|不.*智能|智障)(.*)', event_msg, re.U):
            send_msg = MessageSegment.reply(
                event.message_id) + Message(random.choice(dailyChat_dict.钟离笨()))
        case _ if re.match(r'(.*)(帮我)(.*)', event_msg, re.U):
            pattern = re.match(r'(.*)(帮我)(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await help_me(event, match_target=pattern.group(3))
        case _ if re.match(r'(.*)(?i)(爹|爸|妈|daddy|mommy)(.*)', event_msg, re.U):
            send_msg = MessageSegment.reply(
                event.message_id) + random.choice(dailyChat_dict.钟离爹咪())
        case _ if re.match(r'(.*)(牵手|牵我的手)(.*)', event_msg, re.U):
            send_msg = await hand_in_hand(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(抱抱|抱我)(.*)', event_msg, re.U):
            send_msg = await hug(event)
        case _ if re.match(r'(.*)逐月.*(快乐|安康)(.*)', event_msg, re.U):
            send_msg = await ZhuYue_Ftvl(onMsg_AllNickname=onMsg_AllNickname, event=event)
        case _ if re.match(r'(.*)(谢谢|感谢)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.谢谢先生())
        case _ if re.match(r'(.*)我(.*)(累|好忙|辛苦|疲)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.我好累()))
        case _ if re.match(r'(.*)(夸我|觉得我怎么样|我.*什么样.*人)(.*)', event_msg, re.U):
            send_msg = await judge_me(onMsg_AllNickname, event, user_id)
        case _ if re.match(r'(.*)(往生堂|职业|什么工作)(.*)', event_msg, re.U):
            record_path = f"{config.bot_path}resources/record/职业"
            record_list = os.listdir(record_path)
            await onMsg_AllNickname.finish(MessageSegment.record(f"file:///{record_path}/{random.choice(record_list)}"))
        case _ if re.match(r'(.*)(来我.*壶|来我.*家|做客)(.*)', event_msg, re.U):
            record_path = f"{config.bot_path}resources/record/来我壶"
            record_list = os.listdir(record_path)
            await onMsg_AllNickname.finish(MessageSegment.record(f"file:///{record_path}/{random.choice(record_list)}"))
        case _ if re.match(r'(.*)带我走(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.take_me())
        case _ if re.match(r'(.*)(快快|速速)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                ["这么心急？", "很着急吗？", "所幸来日方长，不必急于一时。"]))
        case _ if re.match(r'(.*)(不能|不可以)(.*)啊(!|！)?', event_msg, re.U):
            send_msg = Message(random.choice(
                ["有何不可？愿闻其详。", "若旅者觉得不妥，那便依你吧。", "可是哪有不妥？"]))
        case _ if re.match(r'(.*)(做什么|干什么|干嘛|干啥|在做啥|我.*聊.*天)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.做什么())
        case _ if re.match(r'(.*)((近来|最近|近日|过)(.*)(做|干|怎么|如何|怎样)|好久不见)(.*)', event_msg, re.U):
            send_msg = await zl_hows_it_going(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(我们去|和我|带我|跟我|我.*一起)(.*)', event_msg, re.U):
            send_msg = await go_with_me(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)(跳.*舞|来一段)(.*)', event_msg, re.U):
            send_msg = await dance(onMsg_AllNickname, event)
        case[*list_str] if "想你" in join_list(list_str):
            send_msg = await miss_U(onMsg_AllNickname, event)
        case[*list_str] if "为什么" in join_list(list_str):
            if random.randint(0, 10) > 6:
                send_msg = random.choice(dailyChat_dict.钟离为什么())
        case[*list_str] if "怎么办" in join_list(list_str):
            if random.randint(0, 10) > 6:
                send_msg = random.choice(dailyChat_dict.钟离怎么办())
        case _ if re.match(r'(.*)(都怪|^坏$|坏坏|坏蛋|太坏|好凶|太凶|^坏！$|坏人)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.钟离坏())
        case _ if re.match(r'(.*)(天气|气候|温度|季节)(.*)', event_msg, re.U):
            send_msg = await weather(event)
        case _ if re.match(r'(.*)(表演一下|异世相遇)(.*)', event_msg, re.U):
            send_msg = await neineinei(onMsg_AllNickname)
        case _ if re.match(r'(.*)(亲亲|亲吻|亲一口)(.*)', event_msg, re.U):
            send_msg = await kiss(event)
        case _ if re.match(r'(.*)(心情|生气|生你.*气|不高兴)(.*)', event_msg, re.U):
            record_path = f"{config.bot_path}resources/record/语气"
            record_list = os.listdir(record_path)
            send_msg = Message(MessageSegment.record(
                f"file:///{record_path}/{random.choice(record_list)}"))
        case _ if re.match(r'(.*)(骂我|凶我)(.*)', event_msg, re.U):
            record_path = f"{config.bot_path}resources/record/凶"
            record_list = os.listdir(record_path)
            send_msg = Message(MessageSegment.record(
                f"file:///{record_path}/{random.choice(record_list)}"))
        case _ if re.match(r'(.*)我(.*(不|没)(.*)(谦虚|虚心)|自恋|自信|自知之明)(.*)', event_msg, re.U):
            raise FinishedException
        case _ if re.match(r'(.*)((不|没)(.*)(谦虚|虚心)|自恋|自信|自知之明)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.钟离不谦虚())
        case _ if re.match(r'(.*)(唱歌|唱戏)(.*)', event_msg, re.U):
            send_msg = await zl_sing(event)
        case _ if re.match(r'(.*)(脱衣服|衣服脱)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.脱衣服())
        case _ if re.match(r'.*大病.*', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.ill_joke())
        case _ if re.match(r'(.*)(真|好|太|实在|这么|如此|有点|很|变)(.*)(聪明|博学|博文|棒|谦虚|自谦|智能|厉害|棒)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.自谦())
        case _ if re.match(r'(.*)(厕|卫生间)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.toilet())
        case _ if re.match(r'，?你?(真|好|太|实在|这么|如此|有点|很|变|当然)(.*)(好看|美|帅|漂亮)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(dailyChat_dict.beautiful()))
        case _ if re.match(r'，?你?(真|好|太|实在|这么|如此|有点|很|变|当然)(.*辣.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                ["辣？", "辣...？应该如何理解？", "非常新颖的形容，有趣。", "哦？"]))
        case _ if re.match(r'(.*)(真|好|太|实在|这么|如此|有点|很|当然)(.*)(乖|温柔|温油)(.*)', event_msg, re.U):
            send_msg = Message(random.choice([f"[CQ:image,file=file:///{face_path}/20220322_231830.jpg]",
                                              f"[CQ:image,file=file:///{face_path}/乖.jpg]"]))
        case _ if re.match(r'(.*)(我(知道).*)|(知道了.*)', event_msg, re.U):
            raise FinishedException
        case _ if re.match(r'(.*)(知道.*|了解.*)(什么.*|哪些.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                ["不多。", "所知不多，略懂一二罢了。", "才疏学浅，了解不多。", "只是凡事略知一二罢了。"]))
        case _ if re.match(r'(.*)(知道|了解)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                ["略懂门道。", "略知一二。", "有所耳闻。", "嗯。", "是的。", "略有耳闻。", "稍有了解罢了。", "我只是凡事略知一二罢了。", "嗯......", "所知不多。", "了解，但不多。", "嗯......知道。"]))
        case _ if re.match(r'(.*)(辛苦|劳累|磨损)(.*)', event_msg, re.U):
            send_msg = Message(random.choice(
                ["磨损得多了，即便是磐石，也会偶感疲惫......", "职责所在，无需挂怀。", "区区小事，不必挂怀。", "再滚烫的热血，历经千年也会冷却；再坚硬的魂灵，历经万年也会消磨。此为「磨损」。"]))
        case _ if re.match(r'(.*)(再见|拜拜|回见)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.goodbye())
        case _ if re.match(r'(.*)(踩我|踢我|揍我)(.*)', event_msg, re.U):
            send_msg = await kick_me(onMsg_AllNickname, event)
        case _ if re.match(r'(.*)我(.*饿|.*渴)(.*)', event_msg, re.U):
            send_msg = await hungry(onMsg_AllNickname, event)
        case _ if re.match(r'我.*(是|当|做).*(钟离|先生|帝君).*的狗.*|(.*我是.*狗.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.Im_dog())
        case _ if re.match(r'(.*)(哭哭|安慰我)(.*)', event_msg, re.U):
            send_msg = await comfort(event)
        case _ if re.match(r'(.*)(幸福|快乐)(.*)', event_msg, re.U):
            send_msg = random.choice(dailyChat_dict.be_happy())
        case _ if re.match(r'(.*)(做你的|做我的)！?(.*)', event_msg, re.U):
            pattern = re.match(r'(.*)(做你的|做我的)！?(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_be_your(event, match_target=pattern.group(3))
        case _ if re.match(r'你?(觉得|认为)(.*)', event_msg, re.U):
            pattern = re.match(r'(.*)(觉得|认为)(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_think(user_id, match_target=pattern.group(3))
        case _ if re.match(r'你?(会|会不会)(.*)', event_msg, re.U):
            pattern = re.match(r'你?(会|会不会)(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_will_u(event, match_target=pattern.group(2).replace("我", f"{nickname}"))
        case _ if re.match(r'(你|我)?(可以|可否|可不可以)(.*)', event_msg, re.U):
            pattern = re.match(r'(你|我)?(可以|可否|可不可以)(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_can_u(event, match_target=pattern.group(3))
        case _ if re.match(r'(.*)是(.*)', event_msg, re.U):
            pattern = re.match(r'(.*)是(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_are_you(event, match_target=event_msg)
        case _ if re.match(r'(.*)有(.*)吗(.*)', event_msg, re.U):
            pattern = re.match(r'(.*)有(.*)吗(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_have(event, match_target=pattern.group(2))
        case _ if re.match(r'(.*)(吗|嘛|是吧|是吗|好不好)(？|！)?', event_msg, re.U):
            pattern = re.match(r'(.*)(吗|嘛|是吧|是吗|好不好)(？|！|。)?', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_MA(user_id, match_target=pattern.group(1).replace("我", f"{nickname}"))
        case _ if re.match(r'(.*)(我想|我想要|我很想|我非常想|我真想)(.*)', event_msg, re.U):
            pattern = re.match(
                r'(.*)(我想|我想要|我很想|我非常想|我真想)(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await I_want(event, match_target=pattern.group(3).replace("我", f"{nickname}"))
        case _ if re.match(r'(.*)(如何|怎么样)(.*)', event_msg, re.U):
            pattern = re.match(
                r'(.*)(如何|怎么样)(.*)', event_msg, re.U)
            assert pattern is not None
            send_msg = await answer_judge(event, match_target=pattern.group(1))
        case _ if re.match(r'(.*？！.*)', event_msg, re.U):
            send_msg = await calm_down(onMsg_AllNickname, matcher)
        case _:
            block_bool = True
    if block_bool:
        # send_msg = Message("onMsg_AllNickname没抓住")
        logger.debug("<blue>onMsg_AllNickname处理失败，进入onMsg_not_tome</blue>")
    else:
        matcher.stop_propagation()
        send_msg = Replace(send_msg).replace("旅者", f"{name}")
    try:
        await onMsg_AllNickname.finish(Message(send_msg))
    except ActionFailed:
        logger.debug("<y>onMsg_Allnicname消息为空</y>")
