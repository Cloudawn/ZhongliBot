import asyncio
import random

from configs.path_config import DATA_PATH, IMAGE_PATH
from nonebot import on_message, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent, MessageEvent,
                                         MessageSegment)
from nonebot.exception import FinishedException
from nonebot.rule import to_me
from src.utils.function import MessageEvent_to_text

# from .gifts import (date_with_users, momo, repeat_users, repeat_zhongli,
#                     zl_eat, zl_sign, zl_sing_song)
from .stories import (story_bishui, story_contract, story_fulong,
                      story_geobutterfly, story_hanwu, story_qianyan_army,
                      story_qinxu, story_spear, story_stone_bird, story_sword,
                      story_tianheng, zl_send_story)

# 这个插件是用来查看礼物文案、礼物背包，以及听钟离讲故事的
# 钟离部分文案（包括故事、早晚安、进群欢迎）来自lof同人作者 [@阿辰不会写刀](https://whz0508.lofter.com)，禁止抄袭或无授权更改引用。

zl_gifts = on_message(priority=32, block=True)
zl_story = on_regex("(.*)(故事|我.*听.*故事)(.*)",
                    rule=to_me(), priority=9, block=True)

sleep = on_regex("(.*我.*睡觉.*)",
                 rule=to_me(), priority=9, block=True)


@zl_gifts.handle()
async def _(bot: Bot, event: MessageEvent):
    event_msg = await MessageEvent_to_text(event)
    re_dict = zl_send_story()
    match list(event_msg):
        case ["手", "制", "莲", "蓉", "月", "饼"]:
            await zl_gifts.send("钟离亲手制作的月饼，也是一种典型的璃月传统月饼。外皮棕红有光，图案典雅优美，馅心味道与质地兼具，甜咸适宜，有着蓉沙类馅细腻润滑、甜中带咸的特点。与其说是一道甜品，更像是一件艺术品。")
            await zl_gifts.finish("毕竟是为你准备的，总归要讲究些。")
        case ["手", "制", "潮", "式", "月", "饼"]:
            await zl_gifts.send("钟离亲手制作的月饼，有着美丽的玫瑰状起酥，皮酥馅细，甜不腻口。此月饼对技巧考验极大，揉面、擀皮、烘烤、回油、晾晒，每一步皆需谨慎入微，不可马虎丝毫。好在，对于细致的璃月人来说，这并非难事。")
            await zl_gifts.finish("“小饼如嚼月，中有酥与饴”。月饼虽小，但也有诸多讲究。更何况，这是赠与你的，多少需花点功夫。")
        case ["手", "制", "冰", "皮", "月", "饼"]:
            await zl_gifts.send("钟离亲手制作的月饼，外皮洁白如雪，花纹优雅别致，口感冰凉滑爽，令人唇齿留香。这种月饼近年来出现，颇受年轻人喜爱。为制作此饼，钟离专程前往了万民堂，向香菱讨教学习。至于中途闹出哪些笑话，在此便不作详谈了。")
            await zl_gifts.finish("“此时暑气未消，吃些清凉的食物有益于降火。此种以冰品为馅的月饼，我还是第一次制作，不知，可否合你心意？")
        case ["琉", "璃", "百", "合", "的", "干", "花"]:
            await zl_gifts.send("生日快乐。这是曾在你出生那天盛开的，「琉璃百合」的干花。")
            await zl_gifts.finish("很久以前的璃月人会说，这种花承载着大地中的美好记忆与祈愿而盛开，我愿意相信，你的诞生也是同样的道理。")
        case ["山", "水", "玲", "珑", "对", "杯"]:
            await zl_gifts.finish("精采绝云间玉土烧制，杯体流畅优美，瓷面温润光泽，笔走飞泉流瀑，云霭翻腾，隽秀间又添苍劲。杯底镌有你的名字，字体沉稳优雅，却不失大气。")
        case ["关", "于", "璃", "月"]:
            await zl_gifts.finish("你可知晓……昔日，璃月港曾有驾朦鐘巨舰猎杀海兽者，被人们称为“船师”。在海洋被无常灾祸统治的时代，浮浪之人朝生暮死。")
        case ["关", "于", "寒", "武"]:
            await story_hanwu(zl_story=zl_gifts)
        case ["关", "于", "契", "约"]:
            await story_contract(zl_story=zl_gifts)
        case ["关", "于", "石", "鸢"]:
            await story_stone_bird(zl_story=zl_gifts)
        case ["靖", "世", "九", "柱"]:
            await zl_gifts.send("我记得那枚戒指，内刻“世间纷乱，众生皆苦”。")
            await asyncio.sleep(2)
            await zl_gifts.finish("在那个年代，曾有人如此说道：“既然你接过了这枚戒指，就要顾虑这天下苍生，继承我靖世所愿，守护璃月的八方太平。”")
        case ["关", "于", "磨", "损"]:
            await zl_gifts.finish("再滚烫的热血，历经千年也会冷却；再坚硬的魂灵，历经万年也会消磨。此为「磨损」。")
        case ["关", "于", "遗", "忘"]:
            await zl_gifts.finish("按照常理来说，帝君是不会遗忘的。但……若是遗忘了，也无妨。就算忘记什么，璃月也能记住一切。哪怕磐岩无法永固，可契约为恒长。")
        case ["千", "岩", "古", "剑"]:
            await story_sword(zl_story=zl_gifts)
        case ["千", "岩", "长", "枪"]:
            await story_spear(zl_story=zl_gifts)
        case ["关", "于", "千", "岩", "军"]:
            await story_qianyan_army(zl_story=zl_gifts)
        case ["关", "于", "岩", "神", "瞳"]:
            await zl_gifts.finish("岩神瞳不必刻意求取，顺其自然，力量……够用就足够了。")
        case ["关", "于", "岩", "晶", "蝶"]:
            await story_geobutterfly(zl_story=zl_gifts)
        case ["关", "于", "碧", "水", "原"]:
            await story_bishui(zl_story=zl_gifts)
        case ["关", "于", "天", "衡", "山"]:
            await story_tianheng(zl_story=zl_gifts)
        case ["关", "于", "伏", "龙", "树"]:
            await story_fulong(zl_story=zl_gifts)
        case ["关", "于", "青", "虚", "浦"]:
            await story_qinxu(zl_story=zl_gifts)
        case ["关", "于", "归", "离", "原"]:
            story_lsit = re_dict["归离"]
            say_story = random.choice(story_lsit)
            await say_story(zl_story=zl_gifts)
        case ["层", "岩", "巨", "渊"]:
            story_lsit = re_dict["层岩"]
            say_story = random.choice(story_lsit)
            await say_story(zl_story=zl_gifts)


@zl_story.handle()  # 钟离讲故事
async def _(event: MessageEvent):
    re_dict = zl_send_story()
    story_list = re_dict[random.choice(
        ["伏龙树",
         "青虚浦",
         "归离",
         "石鸢",
         "千岩军",
         "层岩",
         "伏龙树",
         "契约",
         "千岩古剑",
         "千岩长枪",
         "碧水原",
         "寒武",
         "天衡山",
         "语音故事",
         "岩晶蝶"])]
    say_story = random.choice(story_list)
    await say_story(zl_story)
    raise FinishedException


@sleep.handle()  # 精致睡眠8分钟
async def _(bot: Bot, event: GroupMessageEvent):
    re_dict = zl_send_story()
    story_list = re_dict[random.choice(
        ["伏龙树",
         "青虚浦",
         "归离",
         "石鸢",
         "千岩军",
         "层岩",
         "伏龙树",
         "契约",
         "千岩古剑",
         "千岩长枪",
         "碧水原",
         "寒武",
         "天衡山",
         "语音故事",
         "岩晶蝶"])]
    say_story = random.choice(story_list)
    await say_story(sleep)
    await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=3600*8)
    await sleep.finish(MessageSegment.reply(event.message_id)+"今天的故事就到这里，睡吧。")
