import json
import random
from pathlib import Path
from typing import List, Optional, Type, Union

import nonebot
from httpx import AsyncClient
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent, Message,
                                         MessageEvent, MessageSegment)
from nonebot.internal.matcher import Matcher
from nonebot.matcher import Matcher, matchers
from nonebot.params import Arg, Depends
from src.utils.log import logger

from .config import SYSTEM_PROXY, config

IMAGE_PATH = f"{config.bot_path}resources/image"

client = AsyncClient()
'''异步请求客户端'''


async def MessageEvent_to_text(event: MessageEvent) -> str:
    msg = event.get_message()  # 获取message方法
    msg_to_text = msg.extract_plain_text()  # message提取为text
    return msg_to_text


async def _get_qq_img(user_id: int) -> bytes:
    '''
    :说明
        获取QQ头像

    :参数
        * user_id：用户QQ

    :返回
        * bytes：头像数据
    '''
    num = random.randrange(1, 4)
    url = f'http://q{num}.qlogo.cn/g'
    params = {
        'b': 'qq',
        'nk': user_id,
        's': 100
    }
    resp = await client.get(url, params=params)
    return resp.content


async def get_userName(bot: Bot, event: GroupMessageEvent, user_id: int):
    """
    查询用户群昵称

    参数: Bot, GroupMessageEvent

    """
    nickname = await bot.call_api(
        api="get_group_member_info",
        group_id=event.group_id,
        user_id=user_id,
    )
    return nickname['nickname'] if nickname['card'] == "" else nickname['card']


def Replace(send_msg: Message | str) -> str:
    """
    替换即将发送消息中的某个词

    参数: 
    * send_msg( Message | Str): 回复内容

    """
    if type(send_msg) == Message:
        send_msg = str(send_msg)
    try:
        assert type(send_msg) is str
    except AssertionError:
        logger.debug("<r>Replace替换失败，消息可能为空。</r>")
        send_msg = ""
    return send_msg


class res_path:
    def __getattr__(self, name: str):
        return f"{config.bot_path}" + name


async def get_owner_id(bot: Bot, event: GroupMessageEvent):
    """
    获取群主qq
    """
    member_list = await bot.get_group_member_list(group_id=event.group_id)
    for owner in member_list:
        if owner["role"] == "owner":
            return owner["user_id"]


async def get_admin_id(bot: Bot, event: GroupMessageEvent):
    """
    获取管理员qq列表，返回list
    """
    admin_list = []
    member_list = await bot.get_group_member_list(group_id=event.group_id)
    for admin in member_list:
        if admin["role"] == "admin":
            admin_list.append(admin["user_id"])
    return admin_list


def custom_forward_msg(
    msg_list: List[str], uin: Union[int, str], name: str = "钟离"
) -> List[dict]:
    """
    生成自定义合并消息
    :param msg_list: 消息列表
    :param uin: 发送者 QQ
    :param name: 自定义名称
    """
    uin = int(uin)
    mes_list = []
    for _message in msg_list:
        data = {
            "type": "node",
            "data": {
                "name": name,
                "uin": f"{uin}",
                "content": _message,
            },
        }
        mes_list.append(data)
    return mes_list


def get_message_at(data: Union[str, Message]) -> List[int]:
    """
    说明：
        获取消息中所有的 at 对象的 qq
    参数：
        :param data: event.json()
    """
    qq_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                qq_list.append(int(msg["data"]["qq"]))
    else:
        for seg in data:
            if seg.type == "image":
                qq_list.append(seg.data["url"])
    return qq_list


obj = res_path()
print(obj.file_name)


def is_number(s: str) -> bool:
    """
    说明:
        检测 s 是否为数字
    参数:
        :param s: 文本
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def state_get_key(key: str) -> str:
    # 安全的在state拉屎
    def _get_key(value=Arg(key)) -> str:
        if isinstance(value, str):
            return value
        elif isinstance(value, Message):
            return value.extract_plain_text()
        else:
            return str(value)
    return Depends(_get_key)


def MsgText(data: str):
    """
    返回消息文本段内容(即去除 cq 码后的内容)
    :param data: event.json()
    :return: str
    """
    try:
        data = json.loads(data)
        # 过滤出类型为 text 的【并且过滤内容为空的】
        msg_text_list = filter(lambda x: x["type"] == "text" and x["data"]["text"].replace(" ", "") != "",
                               data["message"])
        # 拼接成字符串并且去除两端空格
        msg_text = " ".join(
            map(lambda x: x["data"]["text"].strip(), msg_text_list)).strip()
        return msg_text
    except:
        return ""


def get_bot() -> Optional[Bot]:
    """
    说明:
        获取 bot 对象
    """
    try:
        return list(nonebot.get_bots().values())[0]
    except IndexError:
        return None


def get_message_img(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有的 图片 的链接
    参数:
        :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "image":
                img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list



def image(
        file: Union[str, Path, bytes] = None,
        path: str = None,
        b64: str = None,
) -> Union[MessageSegment, str]:
    """
    说明:
        生成一个 MessageSegment.image 消息
        生成顺序：绝对路径(abspath) > base64(b64) > img_name
    参数:
        :param file: 图片文件名称，默认在 resource/img 目录下
        :param path: 图片所在路径，默认在 resource/img 目录下
        :param b64: 图片base64
    """
    if isinstance(file, Path):
        if file.exists():
            return MessageSegment.image(file)
        logger.warning(f"图片 {file.absolute()}缺失...")
        return ""
    elif isinstance(file, bytes):
        return MessageSegment.image(file)
    elif b64:
        return MessageSegment.image(b64 if "base64://" in b64 else "base64://" + b64)
    else:
        if file.startswith("http"):
            return MessageSegment.image(file)
        if len(file.split(".")) == 1:
            file += ".jpg"
        if (file := IMAGE_PATH / path / file if path else IMAGE_PATH / file).exists():
            return MessageSegment.image(file)
        else:
            logger.warning(f"图片 {file} 缺失...")
            return ""


def get_local_proxy():
    """
    说明:
        获取 config.py 中设置的代理
    """
    return SYSTEM_PROXY if SYSTEM_PROXY else None


def get_matchers() -> List[Type[Matcher]]:
    """
    获取所有插件
    """
    _matchers = []
    for i in matchers.keys():
        for matcher in matchers[i]:
            _matchers.append(matcher)
    return _matchers
