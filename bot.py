#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
# Custom your logger
#
from nonebot.log import default_format, logger

from src.utils.database import database_close, database_init

logger.add("log/{time:YYY-MM-DD}.Log",
           rotation="00:00",
           retention="1 year",
           level="DEBUG",
           format=default_format,
           encoding="utf-8"
           )

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 开启数据库
driver.on_startup(database_init)

# 关闭数据库
driver.on_shutdown(database_close)

nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_builtin_plugins("echo")
# nonebot.load_plugins("plugins")
nonebot.load_plugins("src")
nonebot.load_plugins("basic_plugins")
# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning(
        "Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
