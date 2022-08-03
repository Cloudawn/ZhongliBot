from nonebot.log import logger
import httpx
async def search_city(foo):
    try:
        a = str(foo).split(",")
        b = await httpx.AsyncClient().get(
            f"https://interface.sina.cn/news/ncp/data.d.json?mod=risk_level&areaname={a[0]}|{a[1]}|%E5%85%A8%E9%83%A8",
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"})
        b = b.json()
        c = [f"————{a[0]}{a[1]}的风险地区————\n"]
        if b["data"]["middleNum"] != 0:
            for i in range(len(b["data"]["middle"])):
                c.append(str("🍁") + str(i + 1) + str(
                    f',地址:{b["data"]["middle"][i]["area_name"]},具体位置:{b["data"]["middle"][i]["communitys"]}') + "\n")

        if b["data"]["highNum"] != 0:
            c.append("\n以下是高风险地区\n")
            for i in range(len(b["data"]["high"])):
                c.append(str("🍁") + str(i + 1) + str(
                    f',地址:{b["data"]["high"][i]["area_name"]},具体位置:{b["data"]["high"][i]["communitys"]}') + "\n")
        logger.success("查风险获取成功！")
        return c
    except(httpx.ConnectError, httpx.NetworkError):
        logger.error("网络错误")
        return "查询失败，请检查网络"
