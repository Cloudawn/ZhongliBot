from nonebot import export, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg

from . import domestic, foreign, search_city
from .search_travelpolicy import travelpolicy

Export = export()
Export.plugin_name = "疫情查询"
Export.plugin_command = "疫情xx | 海外疫情xx|查风险xxx， 出行政策 北京，出行政策 北京 上海"
Export.plugin_usage = "查询疫情信息，新增、死亡等，风险地区"
Export.default_status = True

search_covid_19 = on_command("疫情", aliases={"查询疫情"})


@search_covid_19.handle()
async def _(foo: Message = CommandArg()):
    await search_covid_19.finish(await domestic.httpx_covid_city(msg=str(foo)))

search_covid = on_command("海外疫情")


@search_covid.handle()
async def _(foo: Message = CommandArg()):
    await search_covid.finish(await foreign.httpx_covid_city(msg=str(foo)))

search_danger = on_command("查风险")


@search_danger.handle()
async def _(foo: Message = CommandArg()):
    await search_danger.finish(await search_city.search_city(foo=str(foo)))

search_policy = on_command(
    "出行政策", priority=6, block=True)


@search_policy.handle()
async def _(search_policy: Matcher, event: GroupMessageEvent, bot: Bot, place: Message = CommandArg()):
    place_str = place.extract_plain_text()
    msg = await travelpolicy(search_policy, event, bot, place=place_str)
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=msg
    )
