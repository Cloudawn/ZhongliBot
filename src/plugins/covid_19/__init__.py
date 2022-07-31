from nonebot import  on_command
from nonebot.params import CommandArg
from . import domestic
from nonebot.adapters.onebot.v11 import Message

search_covid_19 = on_command("查询疫情",aliases={"疫情地区"})
@search_covid_19.handle()
async def _(foo:Message=CommandArg()):
    await search_covid_19.finish(await domestic.httpx_covid_city(msg=str(foo)))