import random
from datetime import date
from email.policy import default
from typing import Dict, Tuple

from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from tortoise import fields
from tortoise.models import Model

class UserBag(Model):
    '''用户背包'''
    id = fields.UUIDField(pk=True)
    user_id = fields.IntField()
    '''用户QQ号'''
    user_gift_bag = fields.JSONField()
    '''礼物背包'''
    user_adventure_bag = fields.JSONField()
    '''冒险背包'''