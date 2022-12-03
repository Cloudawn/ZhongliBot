import os
import random
import re

import filetype
from nonebot import export, on_command, on_regex, require
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from src.utils import aiorequests
from src.utils.config import config
from src.utils.function import logger
from src.utils.limiter import DailyNumberLimiter

require("nonebot_plugin_imageutils")

Export = export()
Export.plugin_name = "今天吃什么"
Export.plugin_command = "早上吃什么，晚上吃什么，中午吃什么，今天吃什么"
Export.default_status = True


_lmt = DailyNumberLimiter(5)
imgpath = f"{config.bot_path}resources/foods"

today_food = on_regex(
    r'^(今天|[早中午晚][上饭餐午]|夜宵)吃(什么|啥|点啥)', priority=28, block=True)

addFoodMatcher = on_command("添菜", aliases={"加菜", "添菜 "}, permission=SUPERUSER)


@today_food.handle()
async def net_ease_cloud_word(bot, event: MessageEvent):
    uid = event.user_id
    if not _lmt.check(uid):
        await today_food.finish('这是今天的第几顿？佳肴虽好，切莫贪食', at_sender=True)

    food = random.choice(os.listdir(imgpath))
    name = food.split('.')
    to_eat = f'去吃{name[0]}，如何？\n'
    try:
        foodimg = Message(f'[CQ:image,file=file:///{imgpath}/{food}]')
        # foodimg = Message(MessageSegment.image(
        #     f"file:///{imgpath}/{random.choice(pic_list)}"))
    except Exception as e:
        logger.error(f'{type(e)}')
    _lmt.increase(uid)
    await today_food.finish(to_eat+foodimg, at_sender=True)


async def download_async(url: str, name: str):
    resp = await aiorequests.get(url, stream=True)
    if resp.status_code == 404:
        raise ValueError('')
    content = await resp.content
    try:
        extension = filetype.guess_mime(content).split('/')[1]
    except:
        raise ValueError('')
    abs_path = os.path.join(imgpath, f'{name}.{extension}')
    with open(abs_path, 'wb') as f:
        f.write(content)


@addFoodMatcher.handle()
async def add_food(bot, event: MessageEvent, arg: Message = CommandArg()):
    food = arg.extract_plain_text().strip()
    food_path = f"{imgpath}/food"
    logger.error(f"食物路径是{food_path}")
    ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(event.message))
    if not food:
        await addFoodMatcher.finish('菜名是？\n示例：添菜腌笃鲜[图片]')
    if not ret:
        await addFoodMatcher.finish('可有配图？\n示例：添菜腌笃鲜[图片]', at_sender=True)
    try:
        url = ret.group(2)
        await download_async(url, food)
        await addFoodMatcher.finish(f'已在菜单中添加「{food}」')
    except AttributeError:
        await addFoodMatcher.finish('想要添加什么呢？')
    except ValueError:
        await addFoodMatcher.finish(f'菜单中已经有「{food}」了')
