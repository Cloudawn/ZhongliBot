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
 **钟离部分文案（包括故事、早晚安、进群欢迎）、图片资源来自lof同人作者 [@阿辰不会写刀](https://whz0508.lofter.com)、 [@误曲公子可顾](https://wuqugongzikegu.lofter.com)、[@丙实](https://tuzimulang.lofter.com)、[@猫猫哭哭](https://moraxmywife.lofter.com)、[@钟狐](https://huidanqing464.lofter.com)，禁止抄袭或无授权更改引用。**<BR>
 
 
# 简单搭建教程
1. 新建文件夹，作为钟离先生的家（这也是bot根目录）。
2. 下载[gocqhttp](https://docs.go-cqhttp.org/)并运行。
3. 在先生的家（bot根目录）执行``git clone https://github.com/Cloudawn/ZhongliBot.git``。若克隆失败，可挂一个梯子。或者下载源码手动解压。
4. 下载依赖(推荐使用虚拟环境)：在bot根目录执行``pip install -r requirements.txt``，然后执行``playwright install chromium``。
5. 下载[SQLite](https://www.sqlite.org/index.html)作为数据库。
6. 在``config_default.yml``文件内填写好bot配置，然后保存退出，config_default.yml重命名为``config.yml``。
7. ``db_default``文件夹重命名为``db``。
8. 一切准备就绪，在bot根目录执行``nb run``，提示连接成功后，先生就跑起来啦！
 
 
# 已实现的功能
- [x] 使用本地词库进行日常聊天
- [x] 以好感度作为分级的~~吃桃~~日常互动；如``亲亲``，``抱抱``，``贴贴``，``摸摸``
- [x] 富文本消息回复，包括语音/图片/图文/视频等~~(所以resources很大)~~
- [x] 日常签到，获取升级经验值和原石
- [x] 个人面板，包括攻击、血量、双暴、速度等
- [x] 昵称系统
- [x] 进群欢迎
- [x] 设置群头衔、群管理（需群主权限）
- [x] 随机发送一张钟离照片
- [x] 色色禁言——不可以不敬仙师！
- [x] 俄罗斯轮盘小游戏，包括 ``单人模式``和``多人模式``
- [x] ``钟离讲故事``，随机发送一段文字或语音故事

# TODO
- [ ] ``我的面板``变为图片形式
- [ ] 增加全局开关和插件管理系统
- [ ] 收集并分析聊天数据，优化聊天互动
- [ ] 增加``偷袭群友``与``挑战钟离``
- [ ] ``俄罗斯轮盘``加入1v1对战模式
- [ ] 增加``礼物背包``，用于存放钟离赠送的礼物
- [ ] 记录群成员生日，并在当天祝福与赠礼
 
 ## 碎碎念
 作者是一个一般路过同人女，技术较菜，正在学习中，目标是创作一个生动的钟离先生。 资源为什么不走网络呢...啊，原来是害怕出现雷点cp啊。同人女，恐怖如斯。<br>
bot架构和部分插件是从[真寻](https://github.com/HibiKier/zhenxun_bot)和[mini_jx3_bot](https://github.com/JustUndertaker/mini_jx3_bot)上抄的。（逃走）<br>
