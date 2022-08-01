from nonebot import on_command, on_message, on_request
from nonebot.adapters.onebot.v11 import (PRIVATE_FRIEND, Bot,
                                         FriendRequestEvent,
                                         GroupDecreaseNoticeEvent,
                                         GroupRequestEvent, Message,
                                         MessageEvent, NoticeEvent)
from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot.params import Arg, ArgPlainText, CommandArg, State
from nonebot.typing import T_State
from src.utils.config import config
from src.utils.rule import only_admin_private_message, only_passive

request_matcher = on_request(rule=only_passive, priority=1, block=False)


@request_matcher.handle()
async def friend_request(bot: Bot, event: FriendRequestEvent):
    message = f"收到 {event.user_id} 添加好友的请求"+"\n同意请回复"+f"\n/同意好友 {event.flag}"
    await bot.send_private_msg(user_id=config.admin_number, message=message)


@request_matcher.handle()
async def group_request(bot: Bot, event: GroupRequestEvent):
    message = f"收到 来自 {event.user_id} 邀请加入群: {event.group_id} 的请求" + \
        "\n同意请回复"+f"\n/同意入群 {event.flag}"
    await bot.send_private_msg(user_id=config.admin_number, message=message)


approve_friend = on_command(
    "同意好友", rule=only_admin_private_message, priority=2, block=True
)


@approve_friend.handle()
async def _(bot: Bot, args: Message = CommandArg()):
    flag = args.extract_plain_text()
    print(flag)
    if flag:
        try:
            await bot.call_api(
                api='set_friend_add_request',
                flag=flag,
                approve=True
            )
        except ActionFailed:
            await approve_friend.finish("同意失败，请求已超时")
        else:
            await approve_friend.finish("同意成功")
    else:
        await approve_friend.finish("输入错误，请重新复制")


approve_group = on_command(
    "同意入群", rule=only_admin_private_message, priority=2, block=True
)


@approve_group.handle()
async def _(bot: Bot, args: Message = CommandArg()):
    flag = args.extract_plain_text()
    if flag:
        try:
            await bot.call_api(
                api='set_group_add_request',
                sub_type="invite",
                flag=flag,
                approve=True
            )
        except ActionFailed as e:
            print(e)
            await approve_group.finish("同意失败，请求已超时")
        else:
            await approve_group.finish("同意成功")
    else:
        await approve_group.finish("输入错误，请重新复制")
