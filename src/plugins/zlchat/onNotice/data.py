import asyncio
import time
from typing import Type

from nonebot.adapters.onebot.v11 import (Bot, GroupIncreaseNoticeEvent,
                                         GroupMessageEvent, Message,
                                         MessageSegment)
from nonebot.internal.matcher import Matcher
