from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import require

from .log import logger

the_scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
"""
异步定时器，用于创建定时任务，使用方法：
```
from src.utils.scheduler import scheduler

@scheduler.scheduled_job('cron', hour=0, minute=0)
async def _():
    pass
```
"""


def start_scheduler():
    if not the_scheduler.running:
        the_scheduler.start()
        logger.info("<g>定时器模块已开启。</g>")
