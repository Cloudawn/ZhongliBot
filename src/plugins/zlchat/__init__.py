from nonebot import export

from .onCmd import _touch as _touch
from .onCmd import onCmdRepeat as onCmdRepeat
from .onMsg_AllNicname import onMsg_AllNickname as onMsg_AllNickname
from .onMsg_not_tome import onMsg_NotTome as onMsg_NotTome
from .onMsg_tome import onMsg_tome as onMsg_tome
from .onNotice import poke as poke

# 钟离部分文案（包括故事、早晚安、进群欢迎）来自lof同人作者 [@阿辰不会写刀](https://whz0508.lofter.com)，禁止抄袭或无授权更改引用。

Export = export()
Export.plugin_name = "钟离聊天"
Export.plugin_command = "tooooo many"
Export.plugin_usage = "使用本地词库，和钟离进行简单聊天对话"
Export.default_status = True
