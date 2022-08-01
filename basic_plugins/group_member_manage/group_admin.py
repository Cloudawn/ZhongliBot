
# from nonebot.adapters import
from nonebot import on_command, on_keyword, on_notice, on_regex
from nonebot.adapters.onebot.v11 import (Bot, GroupAdminNoticeEvent,
                                         GroupMessageEvent, Message,
                                         MessageSegment)
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.permission import SUPERUSER
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import get_message_at, get_owner_id, get_userName
from src.utils.log import logger

set_admin = on_command("设置管理", priority=5, block=True,
                       permission=SUPERUSER | GROUP_OWNER)
cancle_admin = on_command("取消管理", priority=5, block=True,
                          permission=SUPERUSER | GROUP_OWNER)


admin_changed = on_notice(priority=1, block=False)


@admin_changed.handle()
async def _(bot: Bot, event: GroupAdminNoticeEvent):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    if event.sub_type == "set":
        if event.user_id == event.self_id:
            owner_id = await get_owner_id(bot, event)
            at = MessageSegment.at(owner_id)
            await admin_changed.send(at + '一份新的契约？......')
            msg = at + '......原来如此，管理此处吗？略有心得，交给我吧。'
            logger.info(f'钟离被设置为群<y>{event.group_id}</y>管理员')
        else:
            at = MessageSegment.at(event.user_id)
            msg = at + f'{nickname}成为了这里的管理者？很不错。今后也受你照顾了。'
            logger.info(
                f'<y>{event.user_id}</y>被设置为群<y>{event.group_id}</y>管理员')
    elif event.sub_type == "unset":
        if event.user_id == event.self_id:
            owner_id = await get_owner_id(bot, event)
            msg = Message('卸职以后，也算乐得清闲。')
            logger.info(f'钟离在群<y>{event.group_id}</y>丢了官')
    else:
        raise FinishedException
    await admin_changed.finish(msg)


@set_admin.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
        admin_name = await get_userName(bot, event, user_id)
        user_data = await bot.get_group_member_info(group_id=event.group_id, user_id=user_id)
        zl_data = await bot.get_group_member_info(group_id=event.group_id, user_id=event.self_id)
        if zl_data["role"] != "owner":
            owner_id = await get_owner_id(bot, event)
            owner_name = await get_userName(bot, event, owner_id)
            msg = f"按理来说，只有「群主」{owner_name}有权任命管理。"
        elif user_data["role"] != "admin":
            await bot.set_group_admin(group_id=event.group_id, user_id=user_id, enable=True)
            msg = f"已设置【{admin_name}】为群管理。"
        else:
            msg = f"【{admin_name}】已经是群管理了。"
    else:
        msg = "设置哪一位为管理呢？"
    await set_admin.finish(msg)


@cancle_admin.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    user_id = get_message_at(event.json())
    if user_id:
        user_id = user_id[0]
        admin_name = await get_userName(bot, event, user_id)
        user_data = await bot.get_group_member_info(group_id=event.group_id, user_id=user_id)
        zl_data = await bot.get_group_member_info(group_id=event.group_id, user_id=event.self_id)
        if zl_data["role"] != "owner":
            owner_id = await get_owner_id(bot, event)
            owner_name = await get_userName(bot, event, owner_id)
            msg = f"按理来说，只有「群主」{owner_name}有权取消管理。"
        elif user_data["role"] != "admin":
            msg = f"【{admin_name}】不是群管理。"
        else:
            await bot.set_group_admin(group_id=event.group_id, user_id=user_id, enable=False)
            msg = f"已取消【{admin_name}】群管理。"
    else:
        msg = "设置哪一位为管理呢？"
    await cancle_admin.finish(msg)
