import asyncio
import random
import time
from typing import Dict, List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import (GROUP, Bot, GroupMessageEvent,
                                         Message, MessageSegment)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.params import ArgStr
# from
from nonebot.typing import T_State
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import get_userName, is_number
from src.utils.log import logger

# from .module import PlayerInfo
from .utils import (GAMBLER, GAMBLER_GROUP, GAMBLER_SELF, alive_txt, die_txt,
                    plck, random_bullet)

face_path = f"{config.bot_path}resources/image/zlface"

russian = on_command(
    "多人模式", aliases={"装弹", "乱斗模式"}, permission=GROUP, priority=5, block=True
)


shot = on_command(
    "开枪", aliases={"咔", "嘭", "嘣"}, permission=GROUP, priority=5, block=True
)


player_qq: List[int] = []
die_player: List[str] = []
alive_player: List[str] = []


@russian.handle()
async def _(event: GroupMessageEvent):
    if plck.check_mode(event.group_id):
        logger.debug(f"<g>群{event.group_id}</g>已锁")
        await russian.finish("游戏进行或冷却中...")
    else:
        plck.lock(event.group_id)


@russian.got("bullet_num", prompt="想要填入几颗子弹？(发送数字1~6即可)")
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State, bullet_num: str = ArgStr("bullet_num")
):
    global GAMBLER
    if bullet_num in ["取消", "算了"]:
        plck.unlock(event.group_id)
        await russian.finish("全身而退，此乃上策。")
    try:
        if GAMBLER_GROUP[event.group_id][1] != 0:
            await russian.finish("俄罗斯轮盘正在进行中。", at_sender=True)
    except KeyError:
        pass
    if not is_number(bullet_num):
        await russian.reject_arg("bullet_num", "输入数字1~6即可，取消可回复 “取消”")
    bullet_num = int(bullet_num)
    if bullet_num < 1 or bullet_num > 6:
        await russian.reject_arg("bullet_num", "子弹数量必须大于0小于7。")
    at_ = state["at"] if state.get("at") else []
    money_pool = state["money_pool"] if state.get("money_pool") else 50
    money = state["money"] if state.get("money") else 50
    user_money = (await UserInfo.get_userInfo(event.user_id))["all_mora"]
    if bullet_num < 0 or bullet_num > 6:
        await russian.reject("子弹数量必须大于0小于7。")
    if (await UserInfo.get_userInfo(event.self_id))["all_mora"] < money:
        plck.unlock(event.group_id)
        await shot.finish("（钟离身无分文，无法坐庄。）")
    if money > user_money:
        plck.unlock(event.group_id)
        await russian.finish("你......钱够了吗？", at_sender=True)

    player_name = event.sender.card or event.sender.nickname

    GAMBLER_GROUP.get_or_set(event.group_id, {
        1: event.user_id,
        "player": player_name,
        2: 0,
        "at": at_,
        "next": event.user_id,
        "money": money,
        "bullet": random_bullet(bullet_num),
        "bullet_num": bullet_num,
        "null_bullet_num": 7 - bullet_num,
        "money_pool": money_pool,
        "index": 0,
        "time": time.time()
    })

    await russian.send(
        Message(
            ("咔 " * bullet_num)[:-1] +
            f"，[CQ:image,file=file:///{face_path}/IMG_20220211_174222.jpg]装填完毕。\n"
            f"第一枪中弹概率：{str(float(bullet_num) / 6.0 * 100)[:5]}%\n→开枪"
        )
    )


@ shot.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State,):
    global GAMBLER
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    random_value = random.randint(0, 100)
    increase_value = random.randint(500, 600)

    GAMBLER.get_or_set(f"{event.group_id}_{event.user_id}", {
        "live_status": 0
    })

    GAMBLER_SELF.get_or_set(event.user_id, {
        "play_times": 0,
        "earning": 0,
        "losing": 0
    })

    try:
        if time.time() - GAMBLER_GROUP[event.group_id]["time"] > 60:
            plck.unlock(event.group_id)
            await shot.send("时间已到，进入结算......")
            await final_end(bot, event, money=0, alive_num=100, die_num=100, player_qq=player_qq)
            logger.debug(f'群{event.group_id}<y>俄罗斯轮盘进入结算</y>')
            return
    except KeyError:
        plck.unlock(event.group_id)
        await shot.finish("俄罗斯轮盘未开始。\n→【多人模式】", at_sender=True)
    if GAMBLER_GROUP[event.group_id][1] == 0:
        plck.unlock(event.group_id)
        await shot.finish("俄罗斯轮盘未开始。\n→【多人模式】", at_sender=True)
    if GAMBLER[f"{event.group_id}_{event.user_id}"]['live_status'] == 1:
        await shot.finish("死者是无法开枪的。", at_sender=True)
    if (await UserInfo.get_userInfo(event.self_id))["all_mora"] <= 0:
        await shot.send("（钟离没钱了，进入结算...）")
        await final_end(bot, event, GAMBLER_GROUP[event.group_id]["money_pool"], alive_num=1000, die_num=1000, player_qq=player_qq)
    if (await UserInfo.get_userInfo(event.user_id))["all_mora"] <= 0:
        await shot.finish("你......钱够了吗？", at_sender=True)
    if GAMBLER_SELF[event.user_id]["play_times"] > 5:
        await shot.finish(
            random.choice([
                f"这类游戏，{nickname}今日已多次参与，这可不妙。",
                f"{nickname}，上头了吗？",
                f"{nickname}今日玩了这么多次，可是上瘾了？"
            ]
            ),
            at_sender=True)
    if GAMBLER_SELF[event.user_id]["earning"] - GAMBLER_SELF[event.user_id]["losing"] >= 200000:  # 每天最多只能赢走20w
        await shot.finish(
            Message(
                random.choice([
                    f"[CQ:image,file=file:///{face_path}/1659200320503.jpg]说起来，钟某还有要事在身......",
                    f"[CQ:image,file=file:///{face_path}/-1789b2b2cf6f6096.png]......（从你这输掉太多，钟离陷入了犹豫）"
                ]
                )
            ),
            at_sender=True)
    try:
        if event.user_id not in player_qq:
            player_qq.append(event.user_id)  # 将玩家qq添加进玩家名单中
        logger.debug(f'<Y>玩家名单：{player_qq}</Y>')
        player_name: str = await get_userName(bot, event, event.user_id)
        if int(GAMBLER_GROUP[event.group_id]["bullet_num"]) > 0:  # 子弹没有空
            if random_value >= ((GAMBLER_GROUP[event.group_id]["bullet_num"])) / float(
                    GAMBLER_GROUP[event.group_id]["null_bullet_num"] - 1 + GAMBLER_GROUP[event.group_id]["bullet_num"]) * 100:  # 概率上没死
                await shot.send(
                    Message(
                        MessageSegment.reply(event.message_id) +
                        alive_txt
                    )
                    + f"\n下枪中弹概率"
                    f'：{str(float((GAMBLER_GROUP[event.group_id]["bullet_num"])) / float(GAMBLER_GROUP[event.group_id]["null_bullet_num"] - 1 + GAMBLER_GROUP[event.group_id]["bullet_num"]) * 100)[:5]}%\n'
                    f'''还剩 {GAMBLER_GROUP[event.group_id]["bullet_num"]} 发子弹，下枪奖励：{GAMBLER_GROUP[event.group_id]["money_pool"]+ increase_value}摩拉。'''
                )

                GAMBLER_GROUP[event.group_id]["null_bullet_num"] -= 1
                GAMBLER_GROUP[event.group_id]["time"] = time.time()
                GAMBLER_GROUP[event.group_id]["index"] += 1
                GAMBLER_SELF[event.user_id]["earning"] += GAMBLER_GROUP[event.group_id]["money_pool"]
                if player_name not in alive_player:
                    alive_player.append(f'''{player_name}''')

            else:
                await shot.send(
                    Message(MessageSegment.reply(event.message_id) +
                            die_txt
                            + f'''\n{player_name}扣除{GAMBLER_GROUP[event.group_id]["money_pool"]}摩拉。\n还剩 {GAMBLER_GROUP[event.group_id]["bullet_num"] -1} 发子弹，下枪奖励：{GAMBLER_GROUP[event.group_id]["money_pool"]+increase_value}摩拉。''',
                            )
                )
                GAMBLER_GROUP[event.group_id]["bullet_num"] -= 1
                GAMBLER[f"{event.group_id}_{event.user_id}"]['live_status'] = 1
                GAMBLER_SELF[event.user_id]["losing"] += GAMBLER_GROUP[event.group_id]["money_pool"]
                logger.debug(
                    f'''<Y>{event.user_id}状态是{GAMBLER[f"{event.group_id}_{event.user_id}"]['live_status']}</Y>''')
                if player_name not in die_player:
                    die_player.append(f"{player_name}【死亡】")
                if player_name in alive_player:
                    alive_player.remove(player_name)
                die_player_str = "\n".join(die_player)
                alive_player_str = "\n".join(set(alive_player))
                # try:
                #     await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
                # except:
                #     ActionFailed
                await asyncio.sleep(0.5)
                await shot.send(f"{alive_player_str}\n——————\n{die_player_str}")
                if GAMBLER_GROUP[event.group_id]["bullet_num"] == 0:
                    await final_end(bot, event, GAMBLER_GROUP[event.group_id]["money_pool"], len(alive_player), len(die_player), player_qq)
        try:
            GAMBLER_GROUP[event.group_id]["money_pool"] += increase_value
        except KeyError:
            pass

    except ZeroDivisionError:
        await shot.send(
            Message(MessageSegment.reply(event.message_id)+die_txt
                    + f'\n{player_name}扣除{GAMBLER_GROUP[event.group_id]["money_pool"]}摩拉。\n还剩 {GAMBLER_GROUP[event.group_id]["bullet_num"] -1} 发子弹。',
                    )
        )
        GAMBLER[f"{event.group_id}_{event.user_id}"]['live_status'] = 1
        GAMBLER_SELF[event.user_id]["losing"] += GAMBLER_GROUP[event.group_id]["money_pool"]
        if player_name in alive_player:
            alive_player.remove(player_name)
        if player_name not in die_player:
            die_player.append(f"{player_name}(X)")
        die_player_str = "\n".join(die_player)
        alive_player_str = "\n".join(set(alive_player))
        try:
            await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
        except ActionFailed:
            pass
        await asyncio.sleep(0.5)
        await shot.send(f"{alive_player_str}\n——————\n{die_player_str}")
        if GAMBLER_GROUP[event.group_id]["bullet_num"] == 0:
            await final_end(bot, event, GAMBLER_GROUP[event.group_id]["money_pool"], len(alive_player), len(die_player), player_qq)


async def final_end(bot: Bot, event: GroupMessageEvent, money: int, alive_num: int, die_num: int, player_qq: list):
    global GAMBLER
    msg = '——今日收益总表——'
    for qq in player_qq:
        earning = GAMBLER_SELF[qq]["earning"] - GAMBLER_SELF[qq]["losing"]
        GAMBLER_SELF[qq]["play_times"] += 1
        msg += f'''\n{await get_userName(bot, event, qq)}：{earning} 摩拉'''
        await UserInfo.change_mora(event.self_id, -earning)
        await UserInfo.change_mora(qq, earning)
    await bot.send(event, Message(msg))
    await asyncio.sleep(0.5)
    if alive_num == 0 and die_num > 0:
        await bot.send(event, Message(f'[CQ:image,file=file:///{face_path}/{random.choice(["睥睨.jpg","睥睨2.jpg"])}]可惜，无人生还。'))

    elif alive_num == 1000 and die_num == 1000:  # 钟离没钱，强行结算
        await bot.send(event, Message('以普遍理性而论，我确实没钱了。'))
    else:
        await bot.send(event, Message(f"[CQ:image,file=file:///{face_path}/20220207_100411.jpg]方才的剧目，可有吓到大家？"))
    alive_player.clear()
    die_player.clear()
    player_qq.clear()
    GAMBLER_GROUP.clear()
    GAMBLER.clear()
    logger.debug(f'GAMBLER是<Y>{GAMBLER}</Y>,GAMBLER_GROUP是<Y>{GAMBLER_GROUP}</Y>')
    plck.unlock(event.group_id)
