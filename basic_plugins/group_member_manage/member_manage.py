import asyncio

from nonebot import on_command, on_keyword, on_regex
# from nonebot.adapters import
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from src.modules.user_info import UserInfo
from src.utils.function import (get_message_text, get_message_at, get_owner_id,
                                get_userName)

from .utils import banSb, plugin_config

cb_notice = plugin_config.callback_notice

set_shut_up = on_command("禁", aliases={"禁言"}, priority=5, block=True,
                         permission=GROUP_ADMIN | SUPERUSER | GROUP_OWNER)
cancle_shut_up = on_command(
    "解禁", priority=5, block=True, permission=GROUP_ADMIN | SUPERUSER | GROUP_OWNER)

kik_out = on_command(
    "踢出", priority=5, block=True, permission=GROUP_ADMIN | SUPERUSER | GROUP_OWNER)


@set_shut_up.handle()
async def shut_up(bot: Bot, event: GroupMessageEvent):
    nickname = (await UserInfo.get_userInfo(event.user_id))["nickname"]
    try:
        msg = get_message_text(event.json()).replace(" ", "").replace("禁", "")
        time = int("".join(
            map(str, list(map(lambda x: int(x), filter(lambda x: x.isdigit(), msg))))))
        # 提取消息中所有数字作为禁言时间
    except ValueError:
        time = None
    sb = get_message_at(event.json())
    gid = event.group_id
    if sb:
        baning = banSb(gid, ban_list=sb, time=time)
        try:
            async for baned in baning:
                if baned:
                    await baned
        except ActionFailed:
            at_owner = MessageSegment.at(await get_owner_id(bot, event))
            await set_shut_up.finish(at_owner+f"{await get_userName(bot,event,event.user_id)}希望{await get_userName(bot,event,sb[0])}接受食言之罚，阁下是否同意？")
        else:
            logger.info("禁言操作成功")
            if cb_notice:  # 迭代结束再通知
                if time is not None:
                    await set_shut_up.finish("契约既成，食言者，当受食言之罚。")
                else:
                    await set_shut_up.finish("（随机降下了一座天星）")
    else:
        await set_shut_up.finish(f'{nickname}，是谁要接受食岩之罚？')


@cancle_shut_up.handle()
async def end_shut_up(bot: Bot, event: GroupMessageEvent):
    sb = get_message_at(event.json())
    baning = banSb(gid=event.group_id, ban_list=sb, time=0)
    try:
        async for baned in baning:
            if baned:
                await baned
    except ActionFailed:
        at_owner = MessageSegment.at(await get_owner_id(bot, event))
        await set_shut_up.send("很遗憾，我对此无能为力。")
        await asyncio.sleep(0.6)
        await set_shut_up.finish(at_owner+f"{await get_userName(bot,event,event.user_id)}希望{await get_userName(bot,event,sb[0])}重获自由，阁下如何看待？")


@kik_out.handle()
async def _kik_out(bot: Bot, event: GroupMessageEvent):
    """
    /踢 @user 踢出某人
    """
    msg = str(event.get_message())
    sb = get_message_at(event.json())
    gid = event.group_id
    if sb:
        if 'all' not in sb:
            try:
                for qq in sb:
                    await bot.set_group_kick(
                        group_id=gid,
                        user_id=int(qq),
                        reject_add_request=False
                    )
            except ActionFailed:
                await kik_out.finish("很遗憾，我对此无能为力。")
            else:
                logger.info(f"踢人操作成功")
                if cb_notice:
                    await kik_out.finish(f"{await get_userName(bot,event,sb[0])}，再会。")
        else:
            await kik_out.finish(f"{await get_userName(bot,event,event.user_id)}希望所有人离开？")
