import re

from nonebot import export, on_command
from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent
from nonebot.params import Arg, CommandArg, T_State
from src.modules.user_info import UserInfo

from .data_source import (delete_exchange_info, get_address, get_exchange_info,
                          get_goods, save_exchange_info)

Export = export()
Export.plugin_name = "米游币商品兑换"
Export.plugin_command = "myb 跟随Bot的指引录入兑换计划, myb_info 查看当前的兑换计划, myb_delete 删除你的所有兑换计划"
Export.plugin_usage = "录入米游币兑换计划，Bot会在对应时间自动帮你抢兑商品"
Export.default_status = True

'''
__plugin_meta__ = PluginMetadata(
    name="米游币商品自动兑换插件",
    description="录入米游币兑换计划，Bot会在对应时间自动帮你抢兑商品",
    usage=(
        "myb 跟随Bot的指引录入兑换计划\n"
        "myb_info 查看当前的兑换计划\n"
        "myb_delete 删除你的所有兑换计划\n"
    ),
    extra={
        "author":  "惜月 <277073121@qq.com>",
        "version": "1.0.0",
    },
)
'''
myb_exchange = on_command(
    'myb', aliases={'米游币兑换', '米游币商品兑换', '米游社商品兑换'}, priority=4, block=True)

myb_info = on_command('myb_info', aliases={
                      '米游币兑换信息', '米游币兑换计划'}, priority=4, block=True)

myb_delete = on_command('myb_delete', aliases={
                        '米游币兑换删除', '米游币兑换取消'}, priority=4, block=True)


@myb_exchange.handle()
async def _(event: PrivateMessageEvent, state: T_State, msg: Message = CommandArg()):
    if msg:
        msg = msg.extract_plain_text().strip()
        if '虚拟' in msg:
            state['商品类型'] = '虚拟'
        elif '实体' in msg:
            state['商品类型'] = '实体'
            state['uid'] = None


@myb_exchange.got('商品类型', prompt='请给出要抢的商品类型(虚拟|实体)，例如原石属于虚拟')
async def _(event: PrivateMessageEvent, state: T_State, type: Message = Arg('商品类型')):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    type = type.extract_plain_text().strip()
    if '虚拟' in type:
        state['商品类型'] = '虚拟'
        print(state)
    elif '实体' in type:
        state['商品类型'] = '实体'
        state['uid'] = None
    else:
        await myb_exchange.reject(f'请{nickname}给出要抢的商品类型(虚拟|实体)，例如原石属于虚拟')


@myb_exchange.got('uid', prompt='虚拟商品要兑换到的游戏uid是？')
async def _(event: PrivateMessageEvent, state: T_State, uid: Message = Arg('uid')):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    uid = uid.extract_plain_text().strip()
    find_uid = re.search(r'(?P<uid>(1|2|5)\d{8})', uid)
    if find_uid:
        state['uid'] = find_uid.group('uid')
    else:
        await myb_exchange.reject(f'{nickname}，这不是有效的uid')


@myb_exchange.got('cookie', prompt=f'还请旅者告知米游币cookie，cookie获取方式详见：\ndocs.qq.com/doc/DQ3JLWk1vQVllZ2Z1')
async def _(event: PrivateMessageEvent, state: T_State, cookie: Message = Arg('cookie')):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    cookie = cookie.extract_plain_text().strip()
    address = await get_address(cookie)
    if address is None:
        await myb_exchange.reject(f'此cookie无效，请{nickname}检查是否以按照正常方法获取')
    elif len(address) == 0:
        await myb_exchange.finish(f'{nickname}的账号还没有填写收货地址，请先去填写收货地址')
    else:
        state['cookie'] = cookie
        if len(address) == 1:
            state['address_id'] = address[0]
        else:
            state['address_list'] = address
        if state['商品类型'] == '虚拟':
            if 'login_ticket' not in cookie and 'stoken' not in cookie:
                await myb_exchange.reject(f'{nickname}的cookie中没有login_ticket字段，请尝试退出后重新登录，再次获取cookie')


@myb_exchange.got('address_id', prompt='回复任意文字继续，接下来选择你的收货地址的ID')
async def _(event: PrivateMessageEvent, state: T_State, address_id: Message = Arg('address_id')):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    address_id = address_id.extract_plain_text().strip()
    flag = False
    for add in state['address_list']:
        if address_id == add['id']:
            state['address_id'] = add
            flag = True
            break
    if not flag:
        address_list = ''
        for add in state['address_list']:
            address_list += f'ID：{add["id"]}，{add["地址"]}\n'
        await myb_exchange.reject(f'{nickname}要选择的收货地址ID是？\n{address_list}')


@myb_exchange.got('game', prompt='目标商品所属游戏是？\n崩坏3|原神|崩坏学园2|未定事件簿|米游社')
async def _(event: PrivateMessageEvent, state: T_State, game: Message = Arg('game')):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    game = game.extract_plain_text().strip()
    if game in ['崩坏3', 'bh3', '崩崩崩', '三崩子']:
        state['goods_list'] = await get_goods('崩坏3')
    elif game in ['原神', 'ys']:
        state['goods_list'] = await get_goods('原神')
    elif game in ['崩坏学园2', 'bh2', '二崩子', '崩坏学院2', '崩崩']:
        state['goods_list'] = await get_goods('崩坏学园2')
    elif game in ['未定事件簿', 'wdsjb', '未定']:
        state['goods_list'] = await get_goods('未定事件簿')
    elif game in ['米游社', 'mys']:
        state['goods_list'] = await get_goods('米游社')
    else:
        await myb_exchange.reject(f'请{nickname}给出要抢的商品所属游戏名称，有崩坏3|原神|崩坏学园2|未定事件簿|米游社')


@myb_exchange.got('goods_search', prompt='还请旅者给出目标商品名，或者其含有的关键词')
async def _(event: PrivateMessageEvent, state: T_State, goods_search: Message = Arg('goods_search')):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    goods_search = goods_search.extract_plain_text().strip()
    match_goods = []
    for good in state['goods_list']:
        if goods_search in good['name']:
            match_goods.append(good)
    if len(match_goods) == 1:
        state['goods'] = match_goods[0]
        save_exchange_info(event.user_id, state)
        await myb_exchange.finish(f'兑换计划录入成功，届时将告知{nickname}结果，发送 myb_info 可以再次确认兑换信息，发送 myb_delete 可以取消兑换计划。')
    elif len(match_goods) > 1:
        state['goods_search_result'] = match_goods
    else:
        await myb_exchange.reject('没有相关可兑换的商品，请重新输入')


@myb_exchange.got('goods', prompt='回复任意文字继续，接下来请选择旅者想要目标商品ID')
async def _(event: PrivateMessageEvent, state: T_State, msg: Message = Arg('goods')):
    nickname = (await UserInfo.get_userInfo(event.user_id))['nickname']
    msg = msg.extract_plain_text().strip()
    for good in state['goods_search_result']:
        if msg == good['id']:
            state['goods'] = good
            save_exchange_info(event.user_id, state)
            await myb_exchange.finish(f'兑换计划录入成功，届时将告知{nickname}结果，发送 myb_info 可以再次确认兑换信息，发送 myb_delete 可以取消兑换计划。')
    good_str = ''
    for good in state['goods_search_result']:
        good_str += f'ID：{good["id"]}, 商品名：{good["name"]}\n'
    await myb_exchange.reject('请选择商品ID：\n'+good_str)


@myb_info.handle()
async def _(event: PrivateMessageEvent):
    info = get_exchange_info(str(event.user_id))
    await myb_info.finish(info)


@myb_delete.handle()
async def _(event: PrivateMessageEvent):
    delete_exchange_info(str(event.user_id))
    await myb_delete.finish('米游币兑换计划已全部取消')
