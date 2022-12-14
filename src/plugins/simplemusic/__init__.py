import traceback

from nonebot import export, on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.typing import T_Handler

from .data_source import Source, sources

Export = export()
Export.plugin_name = "点歌"
Export.plugin_command = "点歌/qq点歌/网易点歌/酷我点歌/酷狗点歌/咪咕点歌/b站点歌 + 关键词"
Export.plugin_usage = "点歌，默认为qq点歌，支持qq、网易、酷我、酷狗、咪咕、b站音频区"
Export.default_status = True


def create_matchers():
    def create_handler(source: Source) -> T_Handler:
        async def handler(matcher: Matcher, msg: Message = CommandArg()):
            keyword = msg.extract_plain_text().strip()
            if keyword:
                try:
                    res = await source.func(keyword)
                except:
                    logger.warning(traceback.format_exc())
                    await matcher.finish("出错了，请稍后再试")

                if res:
                    await matcher.finish(res)

        return handler

    for source in sources:
        matcher = on_command(
            source.keywords[0],
            aliases=set(source.keywords),
            block=True,
            priority=12,
        )
        matcher.append_handler(create_handler(source))


create_matchers()
