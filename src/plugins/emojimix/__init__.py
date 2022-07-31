import re

from nonebot import export, on_regex
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import RegexDict

from emoji.unicode_codes import UNICODE_EMOJI

from .data_source import mix_emoji

Export = export()
Export.plugin_name = "emoji合成器"
Export.plugin_command = "😎+😁"
Export.plugin_usage = "娱乐插件，将两个emoj合二为一"
Export.default_status = True


emojis = filter(lambda e: len(e) == 1, UNICODE_EMOJI["en"])
pattern = "(" + "|".join(re.escape(e) for e in emojis) + ")"
emojimix = on_regex(
    rf"^\s*(?P<code1>{pattern})\s*\+\s*(?P<code2>{pattern})\s*$",
    block=True,
    priority=13,
)


@emojimix.handle()
async def _(msg: dict = RegexDict()):
    emoji_code1 = msg["code1"]
    emoji_code2 = msg["code2"]
    result = await mix_emoji(emoji_code1, emoji_code2)
    if isinstance(result, str):
        await emojimix.finish(result)
    else:
        await emojimix.finish(MessageSegment.image(result))
