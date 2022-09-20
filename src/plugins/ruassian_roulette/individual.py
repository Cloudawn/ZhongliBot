from src.utils.scheduler import the_scheduler
import asyncio
import random

from nonebot import on_command,on_fullmatch
from nonebot.adapters.onebot.v11 import (GROUP, Bot, GroupMessageEvent,
                                         Message, MessageSegment)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.typing import T_State
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import state_get_key
from src.utils.log import logger

from .utils import (GAMBLER_SELF, alive_txt, die_txt, gent_menu, gun, plck)

money = on_command(
    "经典模式", aliases={"经典轮盘", "单人模式"}, permission=GROUP, priority=5, block=True
)


face_path = f"{config.bot_path}resources/image/zlface"



@money.handle()
async def _(event: GroupMessageEvent):
    global GAMBLER_SELF
    if (await UserInfo.get_userInfo(event.self_id))["all_mora"] <= 0:
        await money.finish("（钟离身无分文，无法坐庄）")
    if plck.check_mode(event.group_id):
        logger.debug(f"<g>群{event.group_id}</g>已锁")
        raise FinishedException
    else:
        nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
        GAMBLER_SELF.get_or_set(event.user_id, {
            "play_times": 0,
            "earning": 0,
            "losing": 0
        })
        if GAMBLER_SELF[event.user_id]["play_times"] > 5:
            await money.finish(
                random.choice([
                    f"这类游戏，{nickname}今日已多次参与，这可不妙。",
                    f"{nickname}，上头了吗？",
                    f"{nickname}今日玩了这么多次，可是上瘾了？"
                ]
                ),
                at_sender=True)
        if GAMBLER_SELF[event.user_id]["earning"] >= 200000:  # 每天最多只能赢走20w
            await money.finish(
                Message(
                    random.choice([
                        f"[CQ:image,file=file:///{face_path}/1659200320503.jpg]说起来，钟某还有要事在身......",
                        f"[CQ:image,file=file:///{face_path}/-1789b2b2cf6f6096.png]......（从你这输掉太多，钟离陷入了犹豫）"
                    ]
                    )
                ),
                at_sender=True)
        plck.lock(event.group_id)


@money.got("principal", "旅者想投多少摩拉呢？")
async def _(event: GroupMessageEvent, state: T_State, principal: str = state_get_key("principal")):
    data = (await UserInfo.get_userInfo(event.user_id))
    nickname = data["nickname"]
    GAMBLER_SELF.get_or_set(event.user_id, {
        "play_times": 0,
        "earning": 0,
        "losing": 0
    })
    try:
        state["principal"] = int(principal)
        print("赌注是：", state["principal"])
        if data["all_mora"] < state["principal"]:
            await money.finish(f"{nickname}，你......有带钱吗？")
        elif state["principal"] > 50000:
            await money.reject(Message(f"{nickname}豪掷千金？这可不行......堂主若得知，怕是会将钟某抬回去了。"))
        elif state["principal"] > 5000:
            await money.send(Message(f"{nickname}，勇气可嘉。"))
            await asyncio.sleep(0.5)
        elif state["principal"] < 50:
            await money.send(Message(f"{nickname}未免过于谨慎了。不过，也并非坏事。"))
            await asyncio.sleep(0.5)
        elif state["principal"] <= 0:
            await money.reject(f"这个数字，{nickname}是认真的吗？")
    except ValueError:
        await money.reject(f"{nickname}需输入数字。")

    # 生成赌注回报列表
    state['magn_list'] = gent_menu(state['principal'])
    # 子弹上膛
    state['gun'] = gun(1)
    await UserInfo.change_mora(event.user_id, -state["principal"])


@money.got("next", Message(f"咔。[CQ:image,file=file:///{face_path}/IMG_20220211_174222.jpg]这位朋友，准备好了吗？\"\n→【是|否】\""))
async def _(event: GroupMessageEvent, state: T_State, next_value: str = state_get_key("next")):
    at_msg = MessageSegment.at(event.user_id)
    data = (await UserInfo.get_userInfo(event.user_id))
    nickname = data["nickname"]
    if "继续" == next_value or "是" in next_value or "开枪" in next_value:
        gun_state, gun_index = next(state['gun'])
        if gun_state:
            next_value = state['magn_list'][gun_index + 1]
            await money.reject(Message(at_msg + alive_txt +
                                       f"下一枪奖励： {next_value}" +
                                       f"\n是否继续？"))
        else:
            plck.unlock(event.group_id)
            await money.send(at_msg + die_txt)
            await UserInfo.change_mora(event.self_id, state["principal"])
            GAMBLER_SELF[event.user_id]["play_times"] += 1
            logger.debug(
                f'群{event.group_id}用户{event.user_id}玩了<y>{GAMBLER_SELF[event.user_id]["play_times"]}</y>次')
            await money.finish(Message(f"[CQ:image,file=file:///{face_path}/20220313_010132.jpg]{nickname}的本金和奖励，钟某便笑纳了。"))
    elif "不继续" == next_value or "否" in next_value or "放弃" in next_value:
        # 游戏结束
        GAMBLER_SELF[event.user_id]["play_times"] += 1
        zl_mora = (await UserInfo.get_userInfo(event.self_id))['all_mora']
        await money.send(at_msg + "见好就收，也不失为明智的选择。")
        plck.unlock(event.group_id)
        await asyncio.sleep(0.5)
        salary = 0
        # 结算用户总奖励
        for m in state['magn_list'][:next(state['gun'])[1]]:
            salary += m
        # 钟离余额不足
        if zl_mora < salary:
            salary = zl_mora
            await money.send('(你赢走了钟离所有本金。)')
            await money.send(Message(f'[CQ:image,file=file:///{face_path}/lofter_1642691099736.jpg]以普遍理性而论，我确实没钱了。'))
        else:
            await money.send(at_msg + f"{nickname}最终获得了 {salary} 摩拉。")
            GAMBLER_SELF[event.user_id]["earning"] += salary
        await UserInfo.change_mora(event.self_id, -salary)
        await UserInfo.change_mora(event.user_id, salary)
        logger.debug(
            f'群{event.group_id}用户{event.user_id}玩了<y>{GAMBLER_SELF[event.user_id]["play_times"]}</y>次')
        raise FinishedException
    else:
        await money.reject(f"{nickname}继续还是不继续呢？")
