import httpx
from nonebot.log import logger
async def httpx_covid_city(msg):
    try:
        header = {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
        r = await httpx.AsyncClient().get(url="https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf",headers=header)
        r = r.json()
        x = r["data"]["diseaseh5Shelf"]["areaTree"][0]["children"]
        for i in range(len(x)):
            if x[i]["name"] == str(msg):
                logger.success(f"{msg}疫情数据成功")
                return f'—{msg}的疫情数据—\n⏱时间:{x[i]["total"]["mtime"]}\n🏥累计确诊:{x[i]["total"]["confirm"]}\n🆕现存确诊:{x[i]["total"]["nowConfirm"]}\n💀死亡新增:{x[i]["today"]["dead_add"]}\n☠死亡人数:{x[i]["total"]["dead"]}\n👤治愈人数:{x[i]["total"]["heal"]}\n✈新增境外输入:{x[i]["today"]["abroad_confirm_add"]}\n🏙新增本地输入:{x[i]["today"]["local_confirm_add"]}'
            else:
                for o in range(len(x[i]["children"]) - 1):
                    if x[i]["children"][o]["name"] == str(msg):
                        logger.success(f"{msg}疫情数据成功")
                        return f'—{msg}的疫情数据—\n⏱时间:{x[i]["children"][o]["total"]["mtime"]}\n🏥累计确诊:{x[i]["children"][o]["total"]["confirm"]}\n🆕现存确诊:{x[i]["children"][o]["total"]["nowConfirm"]}\n☠死亡人数:{x[i]["children"][o]["total"]["dead"]}\n👤治愈人数:{x[i]["total"]["heal"]}\n🏙新增本地输入:{x[i]["children"][o]["today"]["local_confirm_add"]}'
    except(httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
            return logger.error(f'查询{msg}地区出现错误 网络错误')
    except(KeyError):
            return  logger.error(f"查询{msg}地区出现错误 数据解析错误")