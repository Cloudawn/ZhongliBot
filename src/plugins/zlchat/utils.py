import json
from cgitb import text
from typing import Any, List, Optional, Tuple, Type, Union

from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.log import logger

def list_for_message(reason: Message) -> Tuple[str, list[str]]:
    """传入Message，拆解成纯文本合集和图片链接

    Args:
        reason (Message): Message

    Returns:
        tuple[str, list[str]]: 纯文本, 保存好的链接
    """
    reason_text = ""
    reason_image = []
    for value in reason:
        match value.type:
            case "text":
                reason_text += " " + value.data["text"]
            case "image":
                reason_image.append(value.data["url"])
    logger.debug(f"reason_text: {[reason_text]}")
    logger.debug(f"reason_image: {reason_image}")

    return reason_text, reason_image

def inspect_msg(msgs: Message,case_type:list = ["text","image"]) -> bool:
    """
    :说明: `inspect_msg`
    > 判断消息类型

    :参数:
      * `msg: Message`: 消息

    :返回:
      - `bool`: 是否只有只有列表内的消息
    """

    for i in msgs:
        if i.type not in case_type:
            return False
    return True


def format_msg(msg: Message) -> Tuple[str, list[str]]:
    """输入消息，检查格式，返回数字和详细富文本

    Args:
        msg (Message): 命令后提取的消息

    Returns:
        list[str, str | Message, str | Message]: 检查结果，纯数字，富文本
    """
    if inspect_msg(msg):
        ...
        if len(msg) >= 2:
            # 有两种以上的消息说明是图文混合的
            return list_for_message(msg)
        else:
            # 只有一种消息
            if msg[0].type == "text":
                return (msg[0].data["text"],[])
            else:
                return ("",[msg[0].data["file"]])
    else:
        raise TypeError("输入不合法")

def join_list(in_list):
    return "".join(in_list)

def get_message_text(data: Union[str, Message]) -> str:
    """
    说明：
        获取消息中 纯文本 的信息
    参数：
        :param data: event.json()
    """
    result = ""

    if isinstance(data, str):
        json_data = json.loads(data)
        for msg in json_data["message"]:
            if msg["type"] == "text":
                result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result

def get_message_img(data: Union[str, Message]) -> List[str]:
    """
    说明：
        获取消息中所有的 图片 的链接
    参数：
        :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        json_data = json.loads(data)
        for msg in json_data["message"]:
            if msg["type"] == "image":
                img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list










class NoFindError(Exception):
    def __init__(self, message: str):
        self.text = f"字符串中没有字符:{message}"


class NoStartStr(NoFindError):
    def __init__(self, message: str):
        self.text = f"字符串中没有起始字符:{message}"


class NoEndStr(NoFindError):
    def __init__(self, message: str):
        self.text = f"字符串中没有结束字符:{message}"


def GetMiddleStr(content: str, startStr: str, endStr: str) -> str:
    # 获取起始字符串坐标
    startIndex = content.find(startStr)
    if startIndex >= 0:
        # 起始坐标+字符串长度等于起始字符串结束位置
        startIndex += len(startStr)
    else:
        # 查不到返回-1
        raise NoStartStr(startStr)

    # 获取结束字符串坐标
    endIndex = content.find(endStr)

    if endIndex >= 0:
        # 裁切字符串
        return content[startIndex:endIndex]
    else:
        # 查不到返回-1
        raise NoEndStr(endStr)


if __name__ == '__main__':
    try:
        print(GetMiddleStr('我请你吃牛肉面吧', '我请你吃', '吧'))
    except NoFindError as e:
        print(e.args)
