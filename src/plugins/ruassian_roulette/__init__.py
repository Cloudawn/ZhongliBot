import asyncio
import math
import random
import time
from random import shuffle
from typing import Dict, List, Tuple, Union

from nonebot import on_command
from nonebot.adapters.onebot.v11 import (GROUP, Bot, GroupMessageEvent,
                                         Message, MessageSegment)
from nonebot.exception import ActionFailed, FinishedException
from nonebot.params import ArgStr, Command, CommandArg
# from
from nonebot.typing import T_State
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.function import (get_message_at, get_userName, is_number,
                                state_get_key)
from src.utils.log import logger
from src.utils.scheduler import scheduler

# from .module import PlayerInfo
from .utils import alive_txt, die_txt, gent_menu, gun, plck, random_bullet

face_path = f"{config.bot_path}resources/image/zlface"

russian = on_command(
    "多人模式", aliases={"装弹", "乱斗模式"}, permission=GROUP, priority=5, block=True
)


shot = on_command(
    "开枪", aliases={"咔", "嘭", "嘣"}, permission=GROUP, priority=5, block=True
)

money = on_command(
    "经典模式", aliases={"经典轮盘", "单人模式"}, permission=GROUP, priority=5, block=True
)

rs_player = {}
THE_PLAYER: Dict[str, str] = {}
die_player: List[str] = []
alive_player: List[str] = []


@russian.handle()
async def _(event: GroupMessageEvent):
    if plck.check_mode(event.group_id):
        await russian.finish("此类游戏玩得太勤，可不是好事。\n(游戏冷却中)")
    else:
        plck.lock(event.group_id)


@russian.got("bullet_num", prompt="想要填入几颗子弹？(发送数字1~6即可)")
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State, bullet_num: str = ArgStr("bullet_num")
):
    global rs_player
    if bullet_num in ["取消", "算了"]:
        await russian.finish("全身而退，此乃上策。")
    try:
        if rs_player[event.group_id][1] != 0:
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
    user_money = (await UserInfo.get_userInfo(event.user_id))["all_gold"]
    if bullet_num < 0 or bullet_num > 6:
        await russian.reject("子弹数量必须大于0小于7。")
    if (await UserInfo.get_userInfo(event.self_id))["all_gold"] < money:
        await shot.finish("（钟离身无分文，无法坐庄。）")
    if money > user_money:
        await russian.finish("你......钱够了吗？", at_sender=True)

    player_name = event.sender.card or event.sender.nickname

    rs_player[event.group_id] = {
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
        "time": time.time(),
    }
    await russian.send(
        Message(
            ("咔 " * bullet_num)[:-1] +
            f"，[CQ:image,file=file:///{face_path}/IMG_20220211_174222.jpg]装填完毕。\n"
            f"第一枪中弹概率：{str(float(bullet_num) / 6.0 * 100)[:5]}%\n→开枪"
        )
    )
    THE_PLAYER.clear()


@ shot.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State,):
    global THE_PLAYER
    global rs_player
    random_value = random.randint(0, 100)
    increase_value = random.randint(500, 600)
    user_group_key = f"{event.group_id}_{event.user_id}"
    state['gun'] = gun(rs_player[event.group_id]["bullet_num"])
    state['magn_list'] = gent_menu(500)
    # user_key = f"{event.user_id}"
    try:
        if time.time() - rs_player[event.group_id]["time"] > 60:
            await shot.send("时间已到，进入结算......")
            await final_end(bot, event, money=0, alive_num=100, die_num=100)
            return
    except KeyError:
        await shot.finish("俄罗斯轮盘未开始。\n→【多人模式】", at_sender=True)
    if rs_player[event.group_id][1] == 0:
        await shot.finish("俄罗斯轮盘未开始。\n→【多人模式】", at_sender=True)
    if THE_PLAYER.get(user_group_key, "unknonw") == "die":
        await shot.finish("死者是无法开枪的。", at_sender=True)
    if (await UserInfo.get_userInfo(event.self_id))["all_gold"] <= 0:
        await shot.finish("（钟离身无分文，无法坐庄。）")
    if (await UserInfo.get_userInfo(event.user_id))["all_gold"] <= 0:
        await shot.finish("你......钱够了吗？", at_sender=True)
    try:
        player_name: str = await get_userName(bot, event, event.user_id)
        logger.debug(f"<r>{await get_userName(bot, event, event.user_id)}</r>")

        if int(rs_player[event.group_id]["bullet_num"]) > 0:  # 子弹没有空
            if random_value >= ((rs_player[event.group_id]["bullet_num"])) / float(
                    rs_player[event.group_id]["null_bullet_num"] - 1 + rs_player[event.group_id]["bullet_num"]) * 100:  # 概率上没死
                await shot.send(
                    Message(
                        MessageSegment.reply(event.message_id) +
                        alive_txt
                    )
                    + f"\n下枪中弹概率"
                    f'：{str(float((rs_player[event.group_id]["bullet_num"])) / float(rs_player[event.group_id]["null_bullet_num"] - 1 + rs_player[event.group_id]["bullet_num"]) * 100)[:5]}%\n'
                    f'''还剩 {rs_player[event.group_id]["bullet_num"]} 发子弹，下枪奖励：{rs_player[event.group_id]["money_pool"]+ increase_value}原石。'''
                )

                rs_player[event.group_id]["null_bullet_num"] -= 1
                rs_player[event.group_id]["time"] = time.time()
                rs_player[event.group_id]["index"] += 1
                THE_PLAYER[user_group_key] = "alive"
                await UserInfo.change_gold(event.self_id, -(rs_player[event.group_id]["money_pool"]))
                await UserInfo.change_gold(event.user_id, rs_player[event.group_id]["money_pool"])
                if player_name not in alive_player:
                    alive_player.append(f'''{player_name}''')

            else:
                await shot.send(
                    Message(MessageSegment.reply(event.message_id) +
                            die_txt
                            + f'''\n{player_name}扣除{rs_player[event.group_id]["money_pool"]}原石。\n还剩 {rs_player[event.group_id]["bullet_num"] -1} 发子弹，下枪奖励：{rs_player[event.group_id]["money_pool"]+increase_value}原石。''',
                            )
                )
                rs_player[event.group_id]["bullet_num"] -= 1

                # die_player.append(f"{await get_userName(bot, event, event.user_id)}(X)")
                if player_name not in die_player:
                    die_player.append(f"{player_name}【死亡】")
                if player_name in alive_player:
                    alive_player.remove(player_name)
                die_player_str = "\n".join(die_player)
                alive_player_str = "\n".join(set(alive_player))
                THE_PLAYER[user_group_key] = "die"
                await UserInfo.change_gold(event.self_id, (rs_player[event.group_id]["money_pool"]))
                await UserInfo.change_gold(event.user_id, -(rs_player[event.group_id]["money_pool"]))
                # try:
                #     await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
                # except:
                #     ActionFailed
                await asyncio.sleep(0.5)
                await shot.send(f"{alive_player_str}\n——————\n{die_player_str}")
                if rs_player[event.group_id]["bullet_num"] == 0:
                    await final_end(bot, event, rs_player[event.group_id]["money_pool"], len(alive_player), len(die_player))

        rs_player[event.group_id]["money_pool"] += increase_value
        # state['magn_list'] = gent_menu(state['principal'])
        # state['gun'] = gun(1)
        # gun_state = next(gun(1))
    except ZeroDivisionError:
        await shot.send(
            Message(MessageSegment.reply(event.message_id)+die_txt
                    + f'\n{player_name}扣除{rs_player[event.group_id]["money_pool"]}原石。\n还剩 {rs_player[event.group_id]["bullet_num"] -1} 发子弹。',
                    )
        )
        if player_name in alive_player:
            alive_player.remove(player_name)
        if player_name not in die_player:
            die_player.append(f"{player_name}(X)")
        die_player_str = "\n".join(die_player)
        alive_player_str = "\n".join(set(alive_player))
        THE_PLAYER[user_group_key] = "die"
        await UserInfo.change_gold(event.self_id, (rs_player[event.group_id]["money_pool"]))
        await UserInfo.change_gold(event.user_id, -(rs_player[event.group_id]["money_pool"]))
        try:
            await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
        except:
            ActionFailed
        await asyncio.sleep(0.5)
        await shot.send(f"{alive_player_str}\n——————\n{die_player_str}")
        if rs_player[event.group_id]["bullet_num"] == 0:
            await final_end(bot, event, rs_player[event.group_id]["money_pool"], len(alive_player), len(die_player))


async def final_end(bot: Bot, event: GroupMessageEvent, money: int, alive_num: int, die_num: int):
    global rs_player
    global THE_PLAYER
    if alive_num == 0 and die_num > 0:
        await bot.send(event, Message(f'[CQ:image,file=file:///{face_path}/{random.choice(["睥睨.jpg","睥睨2.jpg"])}]可惜，无人生还。'))
    else:
        await asyncio.sleep(0.5)
        await bot.send(event, "奖励已实时结算。")
        await asyncio.sleep(1)
        await bot.send(event, Message(f"[CQ:image,file=file:///{face_path}/20220207_100411.jpg]方才的剧目，可有吓到大家？"))
    rs_player.clear()
    alive_player.clear()
    die_player.clear()
    THE_PLAYER.clear()
    plck.unlock(event.group_id)
    raise FinishedException
    # await PlayerInfo.delete_info(event.group_id)


@money.handle()
async def _(event: GroupMessageEvent):
    if (await UserInfo.get_userInfo(event.self_id))["all_gold"] <= 0:
        await money.finish("（钟离身无分文，无法坐庄）")
    if plck.check_mode(event.group_id):
        raise FinishedException
    else:
        plck.lock(event.group_id)


@money.got("principal", "旅者想投多少原石呢？")
async def _(event: GroupMessageEvent, state: T_State, principal: str = state_get_key("principal")):
    data = (await UserInfo.get_userInfo(event.user_id))
    nickname = data["nickname"]
    try:
        state["principal"] = int(principal)
        print("赌注是：", state["principal"])
        if data["all_gold"] < state["principal"]:
            await money.finish(f"{nickname}，你......有带钱吗？")
        elif state["principal"] > 30000:
            await money.reject(Message(f"{nickname}豪掷千金？这可不妙......堂主若得知，怕是会将钟某抬回去了。"))
        elif state["principal"] > 5000:
            await money.send(Message(f"{nickname}，勇气可嘉。"))
            await asyncio.sleep(0.5)
        elif state["principal"] < 50:
            await money.send(Message(f"{nickname}未免过于谨慎了。不过，也并非坏事。"))
            await asyncio.sleep(0.5)
        elif state["principal"] < 0:
            await money.reject(f"这个数字，{nickname}是认真的吗？")
    except ValueError:
        await money.reject(f"{nickname}需输入数字。")

    # 生成赌注回报列表
    state['magn_list'] = gent_menu(state['principal'])
    # 子弹上膛
    state['gun'] = gun(1)
    await UserInfo.change_gold(event.user_id, -state["principal"])
    # await money.send(f"第一枪收益为:{state['magn_list'][0]}")
    # await asyncio.sleep(1)


@money.got("next", Message(f"咔。[CQ:image,file=file:///{face_path}/IMG_20220211_174222.jpg]这位朋友，准备好了吗？\"\n→【是|否】\""))
async def _(event: GroupMessageEvent, state: T_State, next_value: str = state_get_key("next")):
    at_msg = MessageSegment.at(event.user_id)
    data = (await UserInfo.get_userInfo(event.user_id))
    nickname = data["nickname"]
    if "继续" == next_value or "是" in next_value or "开枪" in next_value:
        gun_state, gun_index = next(state['gun'])
        if gun_state:
            # if gun_index < 5:
            next_value = state['magn_list'][gun_index + 1]
            # else:
            #     next_value = "死!"
            await money.reject(at_msg + alive_txt +
                               f"下一枪奖励： {next_value}" +
                               f"\n是否继续？")
        else:
            plck.unlock(event.group_id)
            await money.send(at_msg + die_txt)
            await UserInfo.change_gold(event.self_id, state["principal"])
            await money.finish(Message(f"[CQ:image,file=file:///{face_path}/20220313_010132.jpg]{nickname}的本金和奖励，钟某便笑纳了。"))
    elif "不继续" == next_value or "否" in next_value or "放弃" in next_value:
        # 游戏结束
        zl_gold = (await UserInfo.get_userInfo(event.self_id))['all_gold']
        await money.send(at_msg + "见好就收，也不失为明智的选择。")
        plck.unlock(event.group_id)
        await asyncio.sleep(0.5)
        salary = 0
        for m in state['magn_list'][:next(state['gun'])[1]]:
            salary += m
        if zl_gold < salary:
            salary = zl_gold
            await money.send('(你赢走了钟离所有本金。)')
            await money.finish(Message(f'[CQ:image,file=file:///{face_path}/lofter_1642691099736.jpg]以普遍理性而论，我确实没钱了。'))
        else:
            await money.send(at_msg + f"{nickname}最终获得了 {salary} 原石。")
        await UserInfo.change_gold(event.self_id, -salary)
        await UserInfo.change_gold(event.user_id, salary)
        raise FinishedException
    else:
        await money.reject(f"{nickname}继续还是不继续呢？")
