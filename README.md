# bingshi
 
本项目测试中...

钟离部分文案（包括故事、早晚安、进群欢迎）来自lof同人作者 [@阿辰不会写刀](https://whz0508.lofter.com)，禁止抄袭或无授权更改引用。<BR>

简易搭建教程如下：<BR>
框架：``gocqhttp+nonebot2``<BR>
环境要求：``python 3.10``

1. 下载[gocqhttp](https://docs.go-cqhttp.org/)
2. 新建文件夹，作为钟离先生的家（这也是bot根目录）
3. 在先生的家（bot根目录）执行``git clone https://github.com/Cloudawn/ZhongliBot.git``
若克隆失败，可挂一个支持外网访问的工具。或者下载源码手动解压。
4. 下载依赖(推荐使用虚拟环境)：在bot根目录执行``pip install requirements.txt -r``，然后执行``playwright install chromium``
5. 下载[SQLite](https://www.sqlite.org/index.html)作为数据库
6. 在``config_default.yml``文件内填写好bot配置，然后保存退出，config_default.yml重命名为``config.yml``
7.   ``db_default``文件夹重命名为``db``
8. 一切准备就绪，在bot根目录执行``nb run``，然后运行``gocqhttp``，提示连接成功后，先生就跑起来啦！
