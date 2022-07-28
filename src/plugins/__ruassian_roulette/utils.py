import math
import random
import time
from random import choice, shuffle
from time import time as nowtime
from typing import Dict, List, Tuple, Union

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from src.utils.log import logger

# MONEY_GROUP: Dict[str, Tuple[bool, int]] = {}

die_txt = Message(random.choice(
    [
        '"嘭！"你死亡了。',
        '"嘭！"，你的意识沉入黑暗。',
        '"嘭！"你的耳膜嗡嗡作响，视野坠入黑暗。',
        '"嘭！" '
    ]
))

alive_txt = Message(

    random.choice(
        [
            "你活了下来。",
            "你扣下了扳机，枪声没有响起。",
            '"咔"。\n一滴冷汗流下，你还活着。',
            "黑洞洞的枪口抵着你的额头，好在你还活着。"
        ]
    )

)

weight = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
# weight = [1, 1, 1, 1, 0, 0, 2, 3, 3, 0, 4, 5]
gun_clip = [0] * 6


def gun(bullet_max: int = 1):
    assert 1 <= bullet_max < 6, "子弹数量错误"
    # 权重
    choice_list: list = []
    for _ in range(bullet_max):
        while True:
            bullet_index = choice(weight)
            if bullet_index not in choice_list:
                break
        gun_clip[bullet_index] = 1
        choice_list.append(bullet_index)
    # # 随机排列
    print(gun_clip)
    # 开枪

    for index, bullet in enumerate(gun_clip):
        yield (bullet != 1, index)


def random_bullet(num: int) -> list:
    bullet_lst = [0, 0, 0, 0, 0, 0, 0]
    for i in random.sample([0, 1, 2, 3, 4, 5, 6], num):
        bullet_lst[i] = 1
    return bullet_lst


# 倍率生成
def gent_menu(x: int) -> List[int]:
    # 倍率底数
    def log(x: int) -> float:
        return round(math.log(x, 500), 4)
    magn_list = [0.3, 0.5, 1, 4, 20, 400]
    return [int(i * x * log(x)) for i in magn_list]


# def gun(bullet_max: int):
#     assert 1 <= bullet_max <= 6, "子弹数量错误"
#     # 组合列表
#     gun_clip = [0] * (6-bullet_max) + [1] * bullet_max
#     # 随机排列
#     shuffle(gun_clip)
#     # 开枪
#     print("子弹序列：", gun_clip)
#     for index, bullet in enumerate(gun_clip):
#         yield (bullet != 1, index)


class PluginsLock:
    def __init__(self) -> None:
        self._dict: Dict[str, Tuple[bool, int]] = {}

    def check_mode(self, group_id: int) -> bool:
        """返回当前群号是否有锁"""
        self_type, self_time = self._dict.get(str(group_id), (False, 0))
        logger.debug(
            f"PluginsLock | self_type: {self_type} self_time: {self_time}")
        # 无锁
        if not self_type:
            return False
        # 超时
        elif self_time <= nowtime():
            return False
        # 已锁
        else:
            return True

    def lock(self, group: int):
        self._dict[str(group)] = (True, int(nowtime()) + 120)

    def unlock(self, group: int):
        del self._dict[str(group)]

    # def lock_single(self, user_id:int):
    #     """
    #     多人模式开启后，锁单人模式
    #     """
    #     self._dict[str(user_id)] = (True, int(nowtime()) + 65)

    # def unlock_single(self,user_id:int):
    #     """
    #     多人模式结束，解锁单人模式
    #     """
    #     del self._dict[str(user_id)]


plck = PluginsLock()
