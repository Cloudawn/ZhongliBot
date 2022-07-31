import random
from datetime import date
from email.policy import default
from typing import Dict, Tuple

from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from tortoise import fields
from tortoise.models import Model


class UserInfo(Model):
    '''用户表'''
    # id = fields.IntField(pk=True, generated=True)
    id = fields.UUIDField(pk=True)
    # group_id = fields.IntField()
    # '''所属QQ群号'''
    user_id = fields.IntField()
    '''用户QQ号'''
    user_name = fields.CharField(max_length=255, default="旅者")
    '''用户昵称'''
    gold = fields.IntField(default=0)
    '''用户原石'''
    mora = fields.IntField(default=0)
    '''用户摩拉'''
    friendly = fields.IntField(default=0)
    '''好感度'''
    friendly_max = fields.IntField(default=50)
    '''当前好感等级最大好感度'''
    friendly_lev = fields.IntField(default=1)
    '''好感度等级'''
    lucky = fields.IntField(default=1)
    '''今日运势'''
    sign_times = fields.IntField(default=0)
    '''累计签到次数'''
    last_sign = fields.DateField(default=date(1970, 1, 1))
    '''上次签到日期'''
    last_date_sign = fields.DateField(default=date(1970, 1, 1))
    '''上次约会日期'''

    class Meta:
        table = "user_info"
        table_description = "管理用户"

    @classmethod
    async def get_or_creat(cls, **kwargs) -> Tuple["UserInfo", bool]:
        """查询数据库是否存在用户QQ号,没有就创建"""
        user = await cls.filter(**kwargs).first()
        if user is None:
            user = await cls.create(**kwargs)
            return user, True
        else:
            return user, False

    @classmethod
    async def user_init(cls, user_id: int) -> "UserInfo":
        '''用户注册，刷新昵称'''
        user, _ = await cls.get_or_creat(user_id=user_id)
        return user

    @classmethod
    async def sign_in(cls,
                      user_id: int,
                      lucky_min: int,
                      lucky_max: int,
                      friendly_add: int,
                      gold_base: int,
                      lucky_gold: int
                      ) -> Dict[str, int]:
        '''
        :说明
            设置签到

        :参数
            * user_id：用户QQ
            * lucky_min：最小运势
            * lucky_max：最大运势
            * friendly_add：签到获取的好友度系数
            * gold_base：原石底薪
            * lucky_gold：幸运值影响因子

        :返回
            * dict[str,int]：返回数据字典
            * ``"today_lucky"``：今日运势
            * ``"today_gold"``：今日原石
            * ``"all_gold"``：总原石
            * ``"all_mora"``：总摩拉
            * ``"all_friendly"``：好友度
            * ``"sign_times"``：签到次数
        '''
        record = await cls.filter(user_id=user_id).first()
        if record is None:
            record = await cls.user_init(user_id=user_id)
        print(record)
        # 设置签到日期
        today = date.today()
        record.last_sign = today
        # 计算运势
        today_lucky = random.randint(lucky_min, lucky_max)
        record.lucky = today_lucky
        # 计算原石和摩拉
        today_gold = gold_base+lucky_gold*today_lucky
        record.gold += today_gold
        all_gold = record.gold
        today_mora = random.randint(1000, 2000)
        record.mora += today_mora
        all_mora = record.mora
        # 计算好友度
        today_friendy = today_lucky*friendly_add
        record.friendly += today_friendy
        # 累计签到次数
        record.sign_times += 1
        data = {
            "today_lucky": today_lucky,
            "today_gold": today_gold,
            "today_mora": today_mora,
            "all_gold": all_gold,
            "all_mora": all_mora,
            "all_friendly": record.friendly,
            "sign_times": record.sign_times
        }
        await record.save(update_fields=["last_sign", "lucky", "gold", "friendly", "sign_times", "mora"])
        return data

    @classmethod
    async def get_last_sign(cls, user_id: int):
        '''获取上次签到时间'''
        record = await cls.filter(user_id=user_id).first()
        if record is None:
            return None
        else:
            return record.last_sign

    @classmethod
    async def delete_group(cls):
        '''删除群'''
        # await cls.filter(group_id=group_id).delete()

    @classmethod
    async def set_username(cls, user_id: int, nickname: str):
        """定制昵称"""
        v, _ = await cls.get_or_creat(user_id=user_id)
        v.user_name = nickname
        await v.save(update_fields=["user_name"])

    @classmethod
    async def get_userInfo(cls, user_id: int):
        """查询用户详情，包含用户QQ，原石，摩拉，好感，最大好感，好感等级，上次好感签到日期，昵称。

        参数:
            user_id (int): QQ号

        返回值:
            * dict[str,int]：返回数据字典
            * ``"user_id"``：用户QQ
            * ``"nickname"``：用户昵称
            * ``"all_gold"``：总原石
            * ``all_mora``: 总摩拉,
            * ``"all_friendly"``：总好感度
            * ``"friendly_lev"``：好感度等级
            * ``"max_friendly"``：当前好感等级最大好感度
            * ``"last_date_sign"``：上次好感签到日期
        其他：
            0级好感: 0,
            1级好感: 50,
            2级好感: 150,
            3级好感: 300,
            4级好感: 500,
            5级好感: 1000
        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        data = {
            "user_id": v.user_id,
            "all_gold": v.gold,
            "all_mora": v.mora,
            "all_friendly": v.friendly,
            "friendly_lev": v.friendly_lev,
            "max_friendly": v.friendly_max,
            "nickname": v.user_name,
            "last_date_sign": v.last_date_sign
        }
        return data

    @classmethod
    async def change_frendly_lev(cls, user_id: int):
        """更改好感等级（提升或下降）

        参数:
            * user_id (int): QQ号

        返回值:
            无返回值
        """
        friendly_dict = {
            "0": 0,
            "1": 50,
            "2": 150,
            "3": 300,
            "4": 500,
            "5": 1000
        }  # 每一好感等级对应的最大好感值，最高好感等级为5
        v, _ = await cls.get_or_creat(user_id=user_id)
        lev = v.friendly_lev
        if v.friendly < 0 and v.friendly_lev >= 0:
            v.friendly_lev -= 1
        if v.friendly >= v.friendly_max and lev < 5:
            v.friendly_lev += 1
        v.friendly_max = friendly_dict[str(v.friendly_lev)]
        await v.save(update_fields=["friendly_lev", "friendly_max"])

    @classmethod
    async def change_gold(cls, user_id: int, change_value: int):
        """更改原石

        参数:
            * user_id (int): QQ号
            * change_value(int): 原石改变的值，正数为加，负数为减

        返回值:
            无返回值
        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        v.gold += change_value
        await v.save(update_fields=["gold"])

    @classmethod
    async def change_mora(cls, user_id: int, change_value: int):
        """更改摩拉

        参数:
            * user_id (int): QQ号
            * change_value(int): 摩拉改变的值，正数为加，负数为减

        返回值:
            无返回值
        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        v.mora += change_value
        await v.save(update_fields=["mora"])

    @classmethod
    async def change_frendly(cls, user_id: int, change_value: int):
        """
        更改好感度

        参数:
            * user_id (int): QQ号
            * change_value(int): 好感度改变的值，正数为加，负数为减

        返回值:
            无返回值
        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        v.friendly += change_value
        await v.save(update_fields=["friendly"])
        await cls.change_frendly_lev(user_id)

    @classmethod
    async def date_sign_in(cls, user_id: int):
        """好感签到，获取好感值

        参数:
            user_id (int): QQ号

        返回值:
            所获取的好感值
        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        v.last_date_sign = date.today()
        friendly = random.randint(10, 20)  # 删了一次数据，每日获取高感度增加，作为补偿
        v.friendly += friendly
        await v.save(update_fields=["last_date_sign", "friendly"])
        await cls.change_frendly_lev(user_id)
        return friendly
