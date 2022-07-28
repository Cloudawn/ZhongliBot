import random
from typing import Dict, Tuple

from tortoise import fields
from tortoise.models import Model
from src.utils.log import logger


class UserAttr(Model):
    '''用户面板属性'''
    id = fields.IntField(pk=True, generated=True)
    # group_id = fields.IntField()
    # '''所属QQ群号'''
    user_id = fields.IntField()
    '''用户QQ号'''
    user_name = fields.CharField(max_length=255, default="")
    '''用户昵称'''
    Version = fields.CharField(max_length=2, default="无")
    '''神之眼属性'''
    Level = fields.IntField(default=1)
    '''等级'''
    AscendLev = fields.IntField(default=0)
    '''突破等级'''
    Max_EXP = fields.IntField(default=7000)
    '''当前等级上限经验值'''
    Current_EXP = fields.IntField(default=0)
    '''当前经验值'''
    Atk = fields.IntField(default=18)
    '''攻击力'''
    elemen_Mastery = fields.IntField(default=0)
    '''元素精通'''
    Max_HP = fields.IntField(default=912)
    '''最大血量'''
    Current_HP = fields.IntField(default=912)
    '''当前血量'''
    Crti_Rate = fields.FloatField(default=5)
    '''暴击率'''
    Crti_DMg = fields.IntField(default=50)
    '''暴击伤害'''
    Speed = fields.IntField(default=5)
    '''速度'''
    Def = fields.IntField(default=51)
    '''防御值'''

    class Meta:
        table = "user_attr"
        table_description = "管理用户面板属性"

    @classmethod
    async def get_or_creat(cls, **kwargs) -> Tuple["UserAttr", bool]:
        """查询数据库是否存,没有就创建"""
        user = await cls.filter(**kwargs).first()
        if user is None:
            user = await cls.create(**kwargs)
            return user, True
        else:
            return user, False

    @classmethod
    async def user_init(cls, user_id: int) -> "UserAttr":
        '''用户注册，刷新昵称'''
        user, _ = await cls.get_or_creat(user_id=user_id)
        return user

    @classmethod
    async def add_exp(cls,
                      user_id: int
                      ) -> Dict[str, int]:
        """
        获取经验值

        参数:
            user_id (int): QQ号

        返回值:
            dict[str,int]：返回数据字典,
            today_exp: 今日签到所获经验
        """

        record, _ = await cls.get_or_creat(user_id=user_id)
        print(dir(record))
        # 计算经验值
        today_exp = random.randint(5000, 6000)
        record.Current_EXP += today_exp
        data = {
            "today_exp": today_exp
        }
        await record.save(update_fields=["Current_EXP"])
        await cls.auto_LevupGrade(user_id=user_id)
        return data

    @classmethod
    async def auto_AttrUpGrade(cls, user_id: int):
        """
        用户升级后，提升对应属性

        参数: 

        user_id: 用户QQ

        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        lev = v.Level
        if 1 <= lev <= 20:
            v.Atk += 1
            v.Max_HP += 65
            v.Def += 5
            v.Speed += 1
        elif 21 <= lev <= 40:
            v.Atk += 3
            v.Max_HP += 163
            v.Def += 10
            v.Speed += 1
        elif 41 <= lev <= 50:
            v.Atk += 3
            v.Max_HP += 77
            v.Def += 5
            v.Speed += random.randint(0, 1)
        elif 51 <= lev <= 60:
            v.Atk += 2
            v.Max_HP += 77
            v.Def += 5
            v.Speed += random.randint(0, 1)
        elif 61 <= lev <= 70:
            v.Atk += 1
            v.Max_HP += 77
            v.Def += 5
            v.Speed += random.randint(0, 1)
        elif 71 <= lev <= 80:
            v.Atk += 2
            v.Max_HP += 77
            v.Def += 5
            v.Speed += random.randint(0, 1)
        elif 81 <= lev <= 90:
            v.Atk += 3
            v.Max_HP += 77
            v.Def += 6
            v.Speed += random.randint(1, 2)
        v.Current_HP = v.Max_HP
        v.Crti_Rate += random.random()
        await v.save(update_fields=["Atk", "Max_HP", "Current_HP", "Crti_Rate", "Speed", "Def"])

    @classmethod
    async def auto_LevupGrade(cls, user_id: int):
        """
        自动升级

        参数: 

        user_id: 用户QQ

        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        lev = v.Level
        ascendLev = v.AscendLev
        current_exp = v.Current_EXP
        max_exp = v.Max_EXP
        upgradable_dict = {
            "0": lev in range(1, 20),
            "1": lev in range(20, 40),
            "2": lev in range(40, 50),
            "3": lev in range(50, 60),
            "4": lev in range(60, 70),
            "5": lev in range(70, 80),
            "6": lev in range(80, 90)}
        if current_exp >= max_exp and upgradable_dict.get(str(ascendLev)):
            if 1 <= lev < 20:
                v.Max_EXP = 7000
                v.Current_EXP -= 7000
            elif 20 <= lev < 40:
                v.Max_EXP = 10000
                v.Current_EXP -= 10000
            elif 40 <= lev < 50:
                v.Max_EXP = 14000
                v.Current_EXP -= 14000
            elif 50 <= lev < 60:
                v.Max_EXP = 80000
                v.Current_EXP -= 80000
            elif 60 <= lev < 70:
                v.Max_EXP = 110000
                v.Current_EXP -= 110000
            elif 70 <= lev < 80:
                v.Max_EXP = 148000
                v.Current_EXP -= 148000
            elif 80 <= lev < 90:
                v.Max_EXP = 324000
                v.Current_EXP -= 324000
            logger.debug(
                f"<g>{user_id}升级成功</g>"
            )
            v.Level += 1
            if v.Current_EXP < 0:
                v.Current_EXP = 0
            await v.save(update_fields=["Level", "Max_EXP", "Current_EXP"])
            await cls.auto_AttrUpGrade(user_id)
        else:
            logger.debug(
                f"<y>{user_id}升级失败，可能等级不足/等级已达上限/未突破</y>"
            )

    @classmethod
    async def Ascend(cls, user_id: int, gold, reduce_gold: int) -> bool:
        """
        提升突破等级

        参数: 

        * user_id: 用户QQ
        * gold：当前原石
        * reduce_gold: 所需原石 

        """
        logger.debug(
            f"<g>{user_id}请求突破</g>"
        )
        v, _ = await cls.get_or_creat(user_id=user_id)
        lev = v.Level
        ascend_lev = v.AscendLev
        gold_enough: bool = gold >= reduce_gold
        lev_correct: bool = 20 <= lev and ascend_lev == 0 or 40 <= lev and ascend_lev == 1 or 50 <= lev and ascend_lev == 2 or 60 <= lev and ascend_lev == 3 or 70 <= lev and ascend_lev == 4 or 80 <= lev and ascend_lev == 5 or 90 <= lev and ascend_lev == 6
        can_ascend: bool = gold_enough and lev_correct
        if can_ascend:
            if 20 <= lev and ascend_lev == 0:
                v.Atk += 13
                v.Max_HP += 1100
                v.Def += 43
                v.Speed += 5
                # v.Max_EXP += 10000
            elif 40 <= lev and ascend_lev == 1:
                v.Atk += 12
                v.Max_HP += 500
                v.Def += 30
                v.Speed += 4
                # v.Max_EXP += 14000
            elif 50 <= lev and ascend_lev == 2:
                v.Atk += 6
                v.Max_HP += 650
                v.Def += 40
                v.Speed += 3
                # v.Max_EXP += 80000
            elif 60 <= lev and ascend_lev == 3:
                v.Atk += 10
                v.Max_HP += 300
                v.Def += 30
                v.Speed += 2
                # v.Max_EXP += 110000
            elif 70 <= lev and ascend_lev == 4:
                v.Atk += 10
                v.Max_HP += 480
                v.Def += 30
                v.Speed += 2
                # v.Max_EXP += 1480000
            elif 80 <= lev and ascend_lev == 5:
                v.Atk += 10
                v.Max_HP += 400
                v.Def += 30
                v.Speed += 3
                # v.Max_EXP += 324000
            # elif 90 <= lev and ascend_lev == 6:
            #     v.Atk += 20
            #     v.Max_HP += 700
            #     v.Def += 50
            #     v.Speed += 4
            logger.debug(
                f"<g>{user_id}突破成功</g>"
            )
            v.AscendLev += 1
            v.Current_EXP = 0
            v.Current_HP = v.Max_HP
            v.Crti_Rate += 1+random.random()
            await v.save(update_fields=["AscendLev", "Atk", "Max_HP", "Current_EXP", "Current_HP", "Crti_Rate", "Speed", "Def"])
            return can_ascend
        else:
            logger.debug(
                f"<y>{user_id}突破失败</y>"
            )
            return can_ascend
        ...

    @classmethod
    async def get_userAttr(cls, user_id: int):
        """查询用户面板详情。

            参数:
                user_id (int): QQ号

            返回值:
                返回
                * dict[str,int]：返回数据字典
                * ``"user_id"``：用户QQ
                * ``"version"``：神之眼属性
                * ``"level"``：等级
                * ``"ascrendLev"``：突破等级
                * ``"atk"``：攻击力
                * ``"maxHP"``：最大血量
                * ``"crtHP"``：当前血量
                * ``"maxEXP"``：当前等级上限经验值
                * ``"crtEXP"``：当前经验值
                * ``"eleMas"``：元素精通
                * ``"critRate"``：暴击率
                * ``"critDmg"``：暴击伤害
                * ``"speed"``：速度
                * ``"def"``：防御
        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        data = {
            "user_id": v.user_id,
            "version": v.Version,
            "level": v.Level,
            "ascrendLev": v.AscendLev,
            "atk": v.Atk,
            "maxHP": v.Max_HP,
            "crtHP": v.Current_HP,
            "maxEXP": v.Max_EXP,
            "crtEXP": v.Current_EXP,
            "eleMas": v.elemen_Mastery,
            "critRate": v.Crti_Rate,
            "critDmg": v.Crti_DMg,
            "speed": v.Speed,
            "def": v.Def
        }
        return data

    @classmethod
    async def change_version(cls, user_id: int):
        """
        更改神之眼属性

        参数:
            * user_id (int): QQ号

        返回值:
            无返回值
        """
        v, _ = await cls.get_or_creat(user_id=user_id)
        version = random.choice(['雷','火','风','岩','水','冰','草'])
        v.Version = version
        await v.save(update_fields=["Version"])
        return version