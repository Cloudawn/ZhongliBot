from nonebot import  on_command
from nonebot.params import CommandArg
from . import domestic,foreign
from nonebot.adapters.onebot.v11 import Message

search_covid_19 = on_command("疫情",aliases={"查询疫情"})
@search_covid_19.handle()
async def _(foo:Message=CommandArg()):
    await search_covid_19.finish(await domestic.httpx_covid_city(msg=str(foo)))

search_covid = on_command("海外疫情")
@search_covid.handle()
async def _(foo:Message=CommandArg()):
    await search_covid.finish(await foreign.httpx_covid_city(msg=str(foo)))
