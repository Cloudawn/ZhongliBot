

import os
import random
from typing import Type
from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent,
                                         Message, MessageEvent, MessageSegment,
                                         )

from src.modules.user_info import UserInfo
from src.utils.function import Replace
from src.utils.config import config
from data.Get_dict import dailyChat_dict

