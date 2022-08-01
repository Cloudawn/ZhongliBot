from nonebot import on_command, on_request
from nonebot.adapters.onebot.v11 import (PRIVATE_FRIEND, Bot,
                                         FriendRequestEvent, GroupRequestEvent,
                                         Message, MessageSegment)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import _get_qq_img
from src.utils.rule import only_admin_private_message, only_passive

request_matcher = on_request(rule=only_passive, priority=1, block=False)


@request_matcher.handle()
async def friend_request(bot: Bot, event: FriendRequestEvent):
    user_info = await UserInfo.get_userInfo(event.user_id)
    qq_head = await _get_qq_img(event.user_id)
    head_msg = MessageSegment.image(qq_head)
    friendly = user_info.get('all_friendly')
    friendly_lev = user_info.get('friendly_lev')
    stranger_info = await bot.get_stranger_info(user_id=event.user_id)
    message_1 = f"{event.user_id} 希望与我结交，阁下意下如何？"
    message_2 = head_msg + \
        f"姓名：  {stranger_info['nickname']}\nqq等级：{stranger_info['level']}\n好感度 ：{friendly}\n好感等级：{friendly_lev}\n验证消息：{event.comment}"
    message_3 = "同意请回复"+f"\n /同意好友 {event.flag}"
    await bot.send_private_msg(user_id=config.admin_number, message=message_1)
    await bot.send_private_msg(user_id=config.admin_number, message=message_2)
    await bot.send_private_msg(user_id=config.admin_number, message=message_3)
    raise FinishedException


@request_matcher.handle()
async def group_request(bot: Bot, event: GroupRequestEvent):
    user_info = await UserInfo.get_userInfo(event.user_id)
    qq_head = await _get_qq_img(event.user_id)
    head_msg = MessageSegment.image(qq_head)
    friendly = user_info.get('all_friendly')
    friendly_lev = user_info.get('friendly_lev')
    stranger_info = await bot.get_stranger_info(user_id=event.user_id)
    message_1 = f"{event.user_id} 邀请我加入群: {event.group_id}，阁下意下如何？"
    message_2 = head_msg + \
        f"邀请人： {stranger_info['nickname']}\nqq等级：{stranger_info['level']}\n好感度 ：{friendly}\n好感等级：{friendly_lev}"
    message_3 = "同意请回复"+f"\n /同意入群 {event.flag}"
    await bot.send_private_msg(user_id=config.admin_number, message=message_1)
    await bot.send_private_msg(user_id=config.admin_number, message=message_2)
    await bot.send_private_msg(user_id=config.admin_number, message=message_3)
    raise FinishedException


approve_friend = on_command(
    "同意好友", rule=only_admin_private_message, priority=2, block=True
)


@approve_friend.handle()
async def _(bot: Bot, matcher: Matcher, args: Message = CommandArg()):
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
            matcher.stop_propagation()
            await approve_friend.finish("同意成功")
    else:
        await approve_friend.finish("输入错误，请重新复制")


approve_group = on_command(
    "同意入群", rule=only_admin_private_message, priority=2, block=True
)


@approve_group.handle()
async def _(bot: Bot, matcher: Matcher, args: Message = CommandArg()):
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
            matcher.stop_propagation()
            await approve_group.finish("同意成功")
    else:
        await approve_group.finish("输入错误，请重新复制")
