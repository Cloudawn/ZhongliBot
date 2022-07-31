import httpx
from nonebot.log import logger
async def httpx_covid_city(msg):
    try:
        he = {"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
        get_data = await httpx.AsyncClient().get(url="https://interface.sina.cn/news/wap/fymap2020_data.d.json",headers=he)
        r = get_data.json()
        get_data = get_data.json()["data"]["worldlist"]
        for i in range(len(get_data)-1):
            if str(msg) == "中国":
                return f'—{msg}的疫情数据—\n⏱时间:{r["data"]["times"]}\n🏥累计确诊:{r["data"]["worldlist"][i]["value"]}\n🚑现存确诊:{r["data"]["worldlist"][i]["econNum"]}\n☠死亡人数:{r["data"]["worldlist"][i]["deathNum"]}\n👤治愈人数:{r["data"]["worldlist"][i]["cureNum"]}'
            if r["data"]["worldlist"][i]["name"] == str(msg):
                return f'—{msg}的疫情数据—\n⏱时间:{r["data"]["times"]}\n🏙新增确诊:{r["data"]["worldlist"][i]["conadd"]}\n🏥累计确诊:{r["data"]["worldlist"][i]["value"]}\n🚑现存确诊:{r["data"]["worldlist"][i]["econNum"]}\n☠死亡人数:{r["data"]["worldlist"][i]["deathNum"]}\n👤治愈人数:{r["data"]["worldlist"][i]["cureNum"]}'
    except(httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
            return logger.error(f'查询{msg}地区出现错误 网络错误')
    except(KeyError):
            return logger.error(f"查询{msg}地区出现错误 数据解析错误")
