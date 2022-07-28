from cgitb import text
from socket import MsgFlag
from nonebot.adapters.onebot.v11 import (FriendRequestEvent, GroupRequestEvent, MessageEvent,
                                         RequestEvent,
                                         PrivateMessageEvent)
from nonebot.internal.rule import Rule as Rule
# from nonebot.params import EventToMe
from src.utils.config import config
from src.utils.function import MessageEvent_to_text
# from typing_extensions import Literal, SupportsIndex

def only_passive(event: RequestEvent) -> bool:
    """只匹配被加好友和被邀请进群的事件。"""
    match event:
        case FriendRequestEvent():
            return True
        case GroupRequestEvent():
            return event.sub_type == "invite"
        case _:
            return False


def only_group_add(event: GroupRequestEvent) -> bool:
    """只匹配加群申请"""
    return event.sub_type == "add"


def only_admin_private_message(event: PrivateMessageEvent) -> bool:
    """只匹配Bot管理员私聊"""
    return str(event.user_id) == config.admin_number

def all_nickname(event: MessageEvent):
    """匹配消息中是否包含bot昵称，包含则返回True"""
    is_tome = event.is_tome()
    msg = event.get_message()
    text = msg.extract_plain_text()
    if is_tome:
        return True
    # nickname = ["钟离","帝君","先生","离离"]
    # for name in nickname:
    #     if name in text:
    #         return True
    # return False4
    return any(name in text for name in config.nickname) # 45行代码实现效果等价于41~44行，但更简洁高效
