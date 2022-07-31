from .group_admin import cancle_admin as cancle_admin
from .group_admin import set_admin as set_admin
from .member_manage import cancle_shut_up as cancle_shut_up
from .member_manage import kik_out as kik_out
from .member_manage import set_shut_up as set_shut_up
from .welcome import group_request as group_request
from .welcome import group_welcome as group_welcome

'''
群成员管理，实现的功能有：
* 设置管理员，撤销管理员
* 禁言某人（指令：禁言@xx 60），数字单位为秒
* 解禁某人（指令：解禁@xx）
* 踢出某人（指令：踢出@xx）
* 提示有人申请入群
* 进群欢迎
'''