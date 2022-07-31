import random
import time
from hashlib import md5

import httpx
from nonebot import export, on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.log import logger
from nonebot.params import CommandArg

Export = export()
Export.plugin_name = "多语种翻译"
Export.plugin_command = "翻译中 | 翻译英"
Export.plugin_usage = "将外语和中文互译，支持英译、德语、法语、日语等"
Export.default_status = True

fy_zh = on_command("翻译中", aliases={"翻译中文"})


@fy_zh.handle()
async def _(foo: Message = CommandArg()):
    await fy_zh.finish(await fanyi(msg=foo, n="zh-CH"))

fy_en = on_command("翻译英", aliases={"翻译英文"})


@fy_en.handle()
async def _(foo: Message = CommandArg()):
    await fy_en.finish(await fanyi(msg=foo, n="en"))


async def fanyi(msg, n):
    try:
        lts = int(time.time() * 1000)
        salt = str(lts) + str(random.randint(0, 9))
        sign = md5(("fanyideskweb" + str(msg) + str(salt) +
                   "Ygy_4c=r#e#4EX^NUGUc5").encode()).hexdigest()
        header = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
                  'Referer': 'https://fanyi.youdao.com/',
                  'Cookie': 'OUTFOX_SEARCH_USER_ID=-807799036@10.110.96.159; OUTFOX_SEARCH_USER_ID_NCOO=659977799.288254; JSESSIONID=aaaAQ7LuqvrpF7puSFWcy; fanyi-ad-id=305838; fanyi-ad-closed=1; ___rl__test__cookies=1652228559425/',
                  }
        post_data = f'i={msg}&from=AUTO&to={n}&smartresult=dict&client=fanyideskweb&salt={salt}&sign={sign}&lts={lts}&bv=579f97fa966a5b4ed6b4eaabfc7637e8&doctype=json&version=2.1&keyfrom=fanyi.web&action=FY_BY_REALTlME'
        r = await httpx.AsyncClient().post(url='https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule', data=post_data, headers=header)
        r = r.json()
    except (httpx.NetworkError, httpx.ConnectError, KeyError):
        logger.error("查询翻译失败 原因：网络错误")
        return '查询失败'
    else:
        return f'原文:{r["translateResult"][0][0]["src"]}\n翻译:{r["translateResult"][0][0]["tgt"]}'
