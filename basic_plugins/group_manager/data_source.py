from pathlib import Path
from typing import List, Literal, Optional

from httpx import AsyncClient
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo
from src.modules.search_record import SearchRecord
from src.modules.user_info import UserInfo
from src.utils.config import config

from .model import ImageHandler


async def get_main_server(server: str) -> Optional[str]:
    '''获取主服务器'''
    params = {
        "name": server
    }
    url = "https://www.jx3api.com/app/server"
    async with AsyncClient() as client:
        try:
            req = await client.get(url=url, params=params)
            req_json = req.json()
            if req_json['code'] == 200:
                return req_json['data']['server']
            return None
        except Exception:
            return None


async def bind_server(group_id: int, server: str):
    '''绑定服务器'''
    await GroupInfo.bind_server(group_id, server)


async def set_activity(group_id: int, activity: int):
    '''设置活跃值'''
    await GroupInfo.set_activity(group_id, activity)


async def set_status(group_id: int, status: bool):
    '''设置机器人开关'''
    await GroupInfo.set_status(group_id, status)


async def get_notice_status(group_id: int, notice_type: Literal["welcome_status", "goodnight_status", "someoneleft_status"]) -> bool:
    '''获取通知状态'''
    return await GroupInfo.get_config_status(group_id, notice_type)


async def _message_encoder(message: Message, path: Path) -> List[dict]:
    '''将message编码成json格式，将图片保存本地'''
    req_data = []
    index = 0
    for one in message:
        if one.type == "image":
            url = one.data['url']
            file_name = path/f"{str(index)}.image"
            flag = await ImageHandler.save_image(file_name, url)
            if flag:
                index += 1
                data = {
                    "type": "image",
                    "data": str(file_name)
                }
                req_data.append(data)
            continue

        if one.type == "text":
            data = {
                "type": "text",
                "data": one.data['text']
            }
            req_data.append(data)
            continue

        if one.type == "face":
            data = {
                "type": "face",
                "data": one.data['id']
            }
            req_data.append(data)
            continue

    return req_data


async def get_robot_status(group_id: int) -> bool:
    '''获取机器人开关'''
    return await GroupInfo.get_bot_status(group_id)
