import asyncio

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg, ArgPlainText, CommandArg, RawCommand
from nonebot.rule import to_me
from src.modules.user_info import UserInfo

from .drawer import get_img, get_taskId, get_token

drawer = on_command(
    "画画", aliases={"绘画", "油画", "水彩画", "中国画"}, priority=5)


@drawer.handle()
async def handle_first_receive(matcher: Matcher, event: MessageEvent, command=RawCommand(), args=CommandArg()):
    nickname = (await UserInfo.get_userInfo(event.user_id))["nickname"]
    print("#############")
    print(command)  # 匹配结果
    print(args)
    print("##############")
    if command != '画画':
        style = command
        text = args
        await matcher.send(f'创作主题为「{text}」的{style}......嗯，我也略知一二。请稍等两分钟吧。')
        access_token = await get_token()
        print(access_token)
        taskId = await get_taskId(access_token, text, style)
        print(taskId)
        await asyncio.sleep(60)  # sleep
        images = await get_img(access_token, taskId)
        print(images)
        msg = Message(f'主题为「{text}」的{style}，{nickname}觉得如何？') \
            + MessageSegment.image(images[0]['image']) \
            + MessageSegment.image(images[1]['image']) \
            + MessageSegment.image(images[2]['image'])
        print("#################")
        print(msg)
        print("#################")
        await matcher.finish(msg)

    else:
        await matcher.finish(f'"油画", "水彩画", "中国画", {nickname}想要哪一种呢？\n（请给定明确意象，如：油画 江上落日与晚霞）')
