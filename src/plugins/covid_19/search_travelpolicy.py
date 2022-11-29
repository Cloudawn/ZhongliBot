from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.internal.matcher import Matcher
from src.utils import aiorequests
from src.utils.config import config
from src.utils.limiter import FreqLimiter

freq_limiter = FreqLimiter(5)  # 5秒查询冷却

# from src.utils.function import custom_forward_msg


async def get_policy(_from, to):
    url_city_list = 'https://r.inews.qq.com/api/trackmap/citylist?'
    city_list_raw = await aiorequests.get(url_city_list)
    city_list = await city_list_raw.json()
    msg = ""
    if city_list['status'] == 0 and city_list['message'] == "success":
        for province in city_list['result']:
            for city in province['list']:
                if _from == city['name']:
                    _from_id = city['id']
                if to == city['name']:
                    to_id = city['id']
    else:
        msg += "城市列表请求错误"
        return msg

    try:
        url_get_policy = f"https://r.inews.qq.com/api/trackmap/citypolicy?&city_id={_from_id},{to_id}"
    except UnboundLocalError:
        msg += "城市名错误"
        return msg

    policy_raw = await aiorequests.get(url_get_policy)
    policy = await policy_raw.json()
    if policy['status'] == 0 and policy['message'] == "success":
        data_leave = policy['result']['data'][0]
        data_to = policy['result']['data'][1]
        if _from == to and data_leave['leave_policy'].strip() == data_to['back_policy'].strip():
            msg += f"{_from}出入政策：\n"
            msg += f"{data_to['back_policy'].strip()}（于{data_to['back_policy_date']}更新）"
            msg += "\n"
        else:
            msg += f"{_from}离开政策：\n{data_leave['leave_policy'].strip()}（于{data_leave['leave_policy_date']}更新）"
            msg += "\n"
            msg += f"{to}进入政策：\n{data_to['back_policy'].strip()}（于{data_to['back_policy_date']}更新）"
            msg += "\n"
        msg += f"{to}酒店政策：\n{data_to['stay_info'].strip()}"
        msg += "\n"
        msg += "免责声明：以上所有数据来源于https://news.qq.com/hdh5/sftravel.htm#/"
    else:
        msg += "政策请求错误"
    return msg


def render_forward_msg(msg_list: list, uid, name):
    forward_msg = []
    for msg in msg_list:
        forward_msg.append({
            "type": "node",
            "data": {
                "name": str(name),
                "uin": str(uid),
                "content": msg
            }
        })
    return forward_msg


async def travelpolicy(search_policy: Matcher, event: GroupMessageEvent, bot: Bot, place: str):
    # 冷却器检查
    if not freq_limiter.check(event.user_id):
        await search_policy.send(f"出行政策查询冷却中，请{freq_limiter.left_time(event.user_id)}秒后再试", at_sender=True)
        return

    if len(place.split()) == 0:
        msg = "\n请按照\n出行政策 出发地 目的地\n或\n出行政策 城市名\n的格式输入"
        await search_policy.finish(msg)
    elif len(place.split()) == 1:
        _from = to = place.split()[0]
    elif len(place.split()) == 2:
        _from, to = place.split()
        if _from == to:
            msg = "原地徘徊？"
            await search_policy.send(msg)
    else:
        msg = "目前仅支持两个城市。"
        await search_policy.send(msg)
        return

    msg = await get_policy(_from, to)
    freq_limiter.start_cd(event.user_id)
    if "错误" in msg:
        return msg
    li = []
    for i in msg.split("\n"):
        i = i.strip()
        li.append(i)
    bot_name = config.nickname[0]
    forward_msg = render_forward_msg(li, event.self_id, bot_name)
    msg = forward_msg
    return msg