from nonebot import export, on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

from . import domestic, foreign,search_city

Export = export()
Export.plugin_name = "疫情查询"
Export.plugin_command = "疫情xx | 海外疫情xx|查风险xxx"
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
async def _(foo:Message=CommandArg()):
    await search_danger.finish(await search_city.search_city(foo=str(foo)))
