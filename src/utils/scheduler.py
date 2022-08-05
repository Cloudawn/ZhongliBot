from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import require

from .log import logger

the_scheduler = AsyncIOScheduler(
    timezone="Asia/Shanghai",
    job_defaults={'misfire_grace_time': 5 * 60}
)
"""
异步定时器，用于创建定时任务，使用方法：
```
from src.utils.scheduler import the_scheduler

@the_scheduler.scheduled_job('cron', hour=0, minute=0)
async def _():
    pass
```
"""



def start_scheduler():
    if not the_scheduler.running:
        the_scheduler.start()
        logger.info("<g>定时器模块已开启。</g>")
