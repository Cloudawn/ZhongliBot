<div align=center><img width="320" height="320" src="https://s2.loli.net/2022/07/28/ijPWQzoX1rCVOme.jpg"/></div>

![maven](https://img.shields.io/badge/python-3.10%2B-blue)
![maven](https://img.shields.io/badge/nonebot-2.0.0b4-yellow)
![maven](https://img.shields.io/badge/go--cqhttp-1.0.0-red)

 # 钟离Bot
 以原神钟离先生为原型创作的同人Q群吃桃机器人<br>
 ****
 
 ## 关于
  钟离先生他真的，我哭死。因为太喜欢钟离了，决定写一个钟离bot吃桃。<br>
 **本项目测试中...为测试自动更新插件匆匆开源，略微粗糙。**<br>
 **钟离部分文案（包括故事、早晚安、进群欢迎）、图片资源来自lof同人作者 [@阿辰不会写刀](https://whz0508.lofter.com)、 [@误曲公子可顾](https://wuqugongzikegu.lofter.com)、[@丙实](https://tuzimulang.lofter.com)、[@猫猫哭哭](https://moraxmywife.lofter.com)、[@品茗人](https://pinmingren.lofter.com/)、[@钟狐](https://huidanqing464.lofter.com)，禁止抄袭或无授权更改引用。**<br><br>
 
 
# 简单搭建教程
1. 新建文件夹，作为钟离先生的家；例如新建文件夹``WangShengTang``。
2. 下载[gocqhttp](https://docs.go-cqhttp.org/)并运行，gocq也可放在你新建的文件夹``WangShengTang``内。
3. 在``WangShengTang``执行``git clone https://github.com/Cloudawn/ZhongliBot.git``。若克隆失败，可挂一个梯子，或者下载源码手动解压（需要将文件夹名``ZhongliBot_main``更改为``ZhongliBot``）。
4. 进入文件夹``ZhongliBot``，执行``pip install -r requirements.txt``，然后执行``playwright install chromium``；推荐使用虚拟环境。
5. 下载[SQLite](https://www.sqlite.org/index.html)作为数据库。
6. 在``config_default.yml``文件内填写好bot配置，然后保存退出，config_default.yml重命名为``config.yml``。
7. ``db_default``文件夹重命名为``db``。
8. 一切准备就绪，在bot根目录``ZhongliBot``执行``nb run``，提示连接成功后，先生就跑起来啦！ <br>
 

# 已实现的功能
<details>
<summary>常用功能</summary>
 
- [x] 使用本地词库进行日常聊天
- [x] 以好感度作为分级的~~吃桃~~日常互动；如``亲亲``，``抱抱``，``贴贴``，``摸摸``
- [x] 富文本消息回复，包括语音/图片/图文/视频等~~所以resources很大~~
- [x] 昵称系统，使用``先生叫我xx``后，以后都会这样称呼你
- [x] 进群欢迎
- [x] 随机发送一张钟离照片
- [x] 色色禁言——不可以不敬仙师！
- [x] ``钟离讲故事``，随机发送一段文字或语音故事
- [x] ``钟离生草``，随机发送一张草元素含量丰富的图片
- [x] ``旅途见闻``，随机发送一张原神图片；男角色居多
 
</details>

<details>
<summary>娱乐功能</summary>
 
- [x] 头像表情包制作，来自[noneplugin/nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet)
- [x] 日常签到，获取升级经验值和原石
- [x] 个人面板，包括攻击、血量、双暴、速度等
- [x] 俄罗斯轮盘小游戏，包括 ``单人模式``和``多人模式``
- [x] coc跑团骰，.rxdy，抄的[abrahum/nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer)
- [x] emoj合成，抄的[noneplugin/nonebot-plugin-emojimix](https://github.com/noneplugin/nonebot-plugin-emojimix)
 
</details>

<details>
<summary>管理功能</summary>
 
### 群管理
- [x] 设置群头衔、群管理（需钟离是群主）
- [x] 被辱骂后告状
- [x] ``禁言@xx 60``、``解禁@xx``、``踢出@xx``，感谢[yzyyz1387/nonebot_plugin_admin](https://github.com/yzyyz1387/nonebot_plugin_admin)提供的方法
- [x] 发送加群申请者信息

### bot管理
- [x] ``[打开|关闭] xx``：控制插件开关状态
- [x] ``先生[休息|醒醒]``：控制bot全局开关状态
- [x] ``滴滴xxx``：向bot管理发送消息
- [x] ``同意好友``,``删除好友``，``同意入群``，``退群``
- [x] ``广播``：向bot所在群广播消息 （容易风控，尽量别用）
 
</details>

<details>
<summary>实用功能</summary>
 
- [x] 简洁的点歌功能，来自[noneplugin/nonebot-plugin-simplemusic](https://github.com/noneplugin/nonebot-plugin-simplemusic)
- [x] 米游币商品兑换，来自[CMHopeSunshine/LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon/tree/Bot/src/plugins/nonebot_plugin_myb_exchange)
- [x] 学词，并记录到词库中，抄的[kexue-z/nonebot-plugin-word-bank2](https://github.com/kexue-z/nonebot-plugin-word-bank2)
- [x] 多语种翻译，来自[@bingyue](https://github.com/bingqiu456)
- [x] 疫情查询，来自[@bingyue](https://github.com/bingqiu456)
 
</details>

# TODO
- [ ] ``我的面板``变为图片形式
- [ ] 收集并分析聊天数据，优化聊天互动
- [ ] 增加``偷袭群友``与``挑战钟离``
- [ ] ``俄罗斯轮盘``加入1v1对战模式
- [ ] 增加``礼物背包``，用于存放钟离赠送的礼物
- [ ] 记录群成员生日，并在当天祝福与赠礼 <br>

 ## 碎碎念
 作者是一个一般路过同人女，技术较菜，正在学习中，目标是创作一个生动的钟离先生。 <br>
 啊，希望有朝一日我的代码能和钟离先生一样美丽优雅。<br>
bot架构和部分插件是从[真寻](https://github.com/HibiKier/zhenxun_bot)和[mini_jx3_bot](https://github.com/JustUndertaker/mini_jx3_bot)上抄的。（逃走）<br>另外感谢[@Slock](https://github.com/Sclock)妈咪，多次被我的代码气出高血压，但仍未放弃治疗我，非常感动。

# 致谢
[nonebot2](https://github.com/nonebot/nonebot2)：超棒的机器人框架！<br>
[真寻bot](https://github.com/HibiKier/zhenxun_bot)：堪称百科全书的模范bot！<br>
[mini_jx3_bot](https://github.com/JustUndertaker/mini_jx3_bot)：白师傅，elegant！<br>
