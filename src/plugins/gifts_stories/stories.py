
import asyncio
import os
import random
from typing import Type

from configs.path_config import DATA_PATH, IMAGE_PATH
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent, Message,
                                         MessageEvent, MessageSegment)
from nonebot.internal.matcher import Matcher
from src.utils.config import config


async def story_qince(zl_story: Type[Matcher]):
    await zl_story.send("说起雨声……应是谷物生长的时节了。曾经的璃月，还没有如今这般繁华，那时的人们，每天早出晚归，辛勤劳作采买物资，日子虽然过的算不上富裕，但也能论上和平。")
    await asyncio.sleep(2)
    await zl_story.send("如今轻策庄那里孩童与老叟较多，有气力与志向的年轻人，大多都来了城内谋一份工作……不过，若论生活安逸程度，那恐怕还是轻策山庄更胜一筹吧。")


async def story_qinxu(zl_story: Type[Matcher]):
    await zl_story.send("青墟浦此地亦有许多传说，其中可信度较高的是青墟浦为无名魔神与其信众留下的遗迹，建立的年代或许更早于岩之神执掌璃月的时间。")
    await asyncio.sleep(2)
    await zl_story.send("也许在黑暗侵扰璃沙郊之前，善于开拓探索的璃月先民们亦曾到访此处，并在岩间高塔上留下了自己的印记吧......")
    await asyncio.sleep(2)
    await zl_story.send("在魔神混战的年岁里，璃沙郊地区被水淹没，于今所见的高耸岩山，在那时不过是出露水面的小小岛屿。")
    await asyncio.sleep(2)
    await zl_story.send("但与大多数分布在璃月大地上的其他遗迹类似，在原先的居民离开后，遗迹被魔物占据。若无要事，还是不要贸然前往的好。")


async def story_guili_1(zl_story: Type[Matcher]):
    await zl_story.send("在过去的岁月里，它曾经被人唤作“归离集”。")
    await asyncio.sleep(2)
    await zl_story.send("有传说提及“归离”之名来源于曾率领人众居于此地的两位魔神，其一薨于魔神混战的战火，这也是归离集最终废弃的原因之一。")
    await asyncio.sleep(2)
    await zl_story.send("也有古书《石书辑录》提及，此名取自于“归流民于此集”之意。")


async def story_guili_2(zl_story: Type[Matcher]):
    await zl_story.send("在人们离去的现在，游荡在归离原上的除了少量魔物，便只有试图从古时聚落中攫取传说中宝物的盗宝团，而比宝物更珍贵的东西，则就此遗失在时间的洪流中了……")


async def story_guili_3(zl_story: Type[Matcher]):
    await zl_story.send("归离原位于石门至璃月港的交通要道上，虽有魔物侵扰，亦时时有千岩军驻防把守。如果路遇危急，也可以向他们求援。")


async def story_guili_4(zl_story: Type[Matcher]):
    await zl_story.send("想了解关于归离原的过去吗？在过去，这里曾是璃月久远的故都。后来，那里灾乱频繁，更甚者有一场大水泛滥。于是，归离原的人们才南迁到璃月港，建立新的家园。")
    await asyncio.sleep(2)
    await zl_story.send("魔神战争很久以前，璃月的土地上还都是战乱。归离原亦不能幸免。那时候，它的名字还不叫此，而是名为「归离集」，至于这个名字的含义吗……")
    await asyncio.sleep(2)
    await zl_story.send("「今我离民，皆安居乐业，几同归乡。」莫如名之归离原，归离原故而得名。")


async def story_stone_bird(zl_story: Type[Matcher]):
    await zl_story.send("石鸢，你在孤云阁见过这种鸟兽吗？它正是在山岩林立的绝峰之间筑巢的猛禽，世人常说这种难以见得的禽鸟永远在云间放浪，无足无巢。")
    await asyncio.sleep(2)
    await zl_story.send("但这终究只是一种飞鸟，石鸢也要为腹中餐食、巢中幼鸟而奔波……")
    await asyncio.sleep(2)
    await zl_story.send("唔，为何无缘无故提到了食用上面……？")


async def story_qianyan_army(zl_story: Type[Matcher]):
    await zl_story.send("千岩牢固，重嶂不移。千城戎甲，靖妖闲邪。千岩军最初是由岩王帝君的追随者自发组成的部队，最早可追溯到港城落成之时。他们以岩君、璃月之名为旗号，共进退，绝不溃弃。")


async def story_cenyan_1(zl_story: Type[Matcher]):
    await zl_story.send("层岩巨渊，乃星辰陨落之地。自那颗天星从无际夜空垂落而下，尘土化为琉璃晶砂。现在……层岩巨渊已经关闭，还是不要前去。")
    await asyncio.sleep(2)
    await zl_story.send("有朝一日，若是有机会前往此地，去寻那些晶砂吧，那是璃月瑰丽的琉璃器具的原材料之一。")


async def story_cenyan_2(zl_story: Type[Matcher]):
    await zl_story.send("层岩巨渊……它是璃月天然的矿场，从前，或许书上也有记载，古时曾陨落天星，也由此，它才呈现这般模样。矿区内部也很是广阔，各种奇特晶体数不胜数。那里……也是古战场的遗址。")
    await asyncio.sleep(2)
    await zl_story.send("五百年前，一场灾难席卷了大陆。层岩巨渊亦不能幸免，那时，我曾指挥千岩将士与夜叉一族，于无边的漆黑厮杀缠斗。……最终，他们以不灭的意志，对抗着无尽的黑暗。层岩巨渊的灾厄终止了。可他们当中的很大一部分，却只能长眠于无尽的地底。……即便是过去了很久，那些回忆，也会牵动着我。")
    await asyncio.sleep(2)
    await zl_story.send("璃月，它的根也就在于人民的勇敢与不畏牺牲，为了更好的未来与生活，他们甘愿随着神明的脚步，奉上自己的全力。")
    await asyncio.sleep(3)
    await zl_story.send("......(钟离沉默了)")


async def story_fulong(zl_story: Type[Matcher]):
    await zl_story.send(random.choice([
        "血玉之枝......你从何处得来？即使战斗结束如此之久，它的枝叶仍在簌簌作响。它以那位龙王的力量滋养而生，因龙血滋养，永无宁时......",
        "帝君命理水叠山真君以琥牢山为阵，力图镇压若陀龙王。而那棵伏龙树被帝君栽下，想来，已是数百年之久了……"
    ]))


async def story_contract(zl_story: Type[Matcher]):
    await zl_story.send("岩王帝君曾从无杂质的金珀之中削出长刀一柄，他挥剑斫去山峰的一角，以此向子民立下无上庄严的契约：")
    await asyncio.sleep(2)
    await zl_story.send("离散的人，必将聚拢回归；离约的人，必然加以惩治。失去挚爱者、痛失珍宝者、蒙受不公者，将得到补偿。")


async def story_sword(zl_story: Type[Matcher]):
    await zl_story.send("千岩古剑，这是古代千岩军爱用的武器，以构成璃月港的神铸基岩削成，沉重无比，常人难以使用。在过去的年代，古时千岩军人却能自如挥动。")
    await asyncio.sleep(2)
    await zl_story.send("这把巨剑以牢固和沉重为人所知，正如千岩军以己为盾，守护身后的家园。它承载着守护者的责任与意志。")


async def story_spear(zl_story: Type[Matcher]):
    await zl_story.send("武器和人一样是会死的，所以往生堂在这个时代收纳了这些千岩造物。锤炼所用的金属，锻造时闪瞬的火花，连同往日持有者的大愿，这些都是构成它生命的东西。")
    await asyncio.sleep(2)
    await zl_story.send("在这样的时代，它没有再被拿起的一天，所以我们就将它们收纳，尊重这些近死的金锐器物。")


async def story_bishui(zl_story: Type[Matcher]):
    await zl_story.send("这碧水河在获花洲分为两支，一支向北化作醴泉，滋润了蒙德酒乡，我之前跟你说的爱喝酒的朋友，就在蒙德，整日向我吹嘘他的蒲公英酒。")
    await asyncio.sleep(2)
    await zl_story.send("而另一支则向南入海，注入无穷缥缈……海上有一方天地，唤作孤云阁，至于这孤云阁的来历，又是另一段往事了。")


async def story_hanwu(zl_story: Type[Matcher]):
    await zl_story.send("......自那场地动之后，匠人的那只眼睛只余下彼时无法辨识天地四方上下的黑暗，耳畔时常回荡如天地崩裂的剑石相击之声。")
    await asyncio.sleep(2)
    await zl_story.send("从此匠人的锻炉蒙尘，其中只剩下冰冷的余灰，与未竟的锻兵之梦。")


async def story_tianheng(zl_story: Type[Matcher]):
    await zl_story.send("过去的年岁……天衡叠嶂连璧生，岩层渊薮玉辉蕴。而今的天衡，是璃月港西边的山脉，也是抵御外敌的一道天然保护屏障。")
    await asyncio.sleep(2)
    await zl_story.send("有记载以来，作为璃月的壁垒经历了数不清的大小战争，因此也可以看到不少古城墙、堡垒和防御工事的遗迹。")
    await asyncio.sleep(2)
    await zl_story.send("如果你想要去看看，我也知晓何处有遗迹所在。当然，这遗迹不仅仅是战场，还是当时的人们采石留下的矿洞一类的……若你运气好，也许还能得到一些石珀。")


async def story_geobutterfly(zl_story: Type[Matcher]):
    await zl_story.send("岩晶蝶，是闪光的岩元素生物，也是元素上升凝合而成的产物，以无处不在的岩元素维生，在璃月，它很常见。")
    await asyncio.sleep(2)
    await zl_story.send("世人都说，石珀正是岩之心，岩石是有心的。何况这片土地已经千年之久，一千年，两千年，还是三千年，河床里的石头会做梦，群山也会做梦。")
    await asyncio.sleep(2)
    await zl_story.send("厚重的岩，他们的梦是比风还轻的蝴蝶。在难以尽览的万古中，即使是磐岩也会做梦。据说这些岩晶凝成的飞蝶，正是嵯峨山石之梦。")


async def story_record(zl_story: Type[Matcher]):
    record_path = f"{config.bot_path}/resources/record/在想什么"
    record_list = os.listdir(record_path)
    await zl_story.send(MessageSegment.record(f"file:///{record_path}/{random.choice(record_list)}"))

re_dict = {
    "轻策庄": [story_qince],
    "青虚浦": [story_qinxu, story_record],
    "归离": [story_guili_1, story_guili_2, story_guili_3, story_guili_4],
    "石鸢": [story_stone_bird, story_record],
    "千岩军": [story_qianyan_army],
    "层岩": [story_cenyan_1, story_cenyan_2],
    "伏龙树": [story_fulong],
    "契约": [story_contract],
    "千岩古剑": [story_sword, story_record],
    "千岩长枪": [story_spear],
    "碧水原": [story_bishui, story_record],
    "寒武": [story_hanwu],
    "天衡山": [story_tianheng],
    "岩晶蝶": [story_tianheng],
    "语音故事": [story_record]
}


def zl_send_story():
    """
    返回故事字典
    * ``"轻策庄"``:[story_qince],
    * ``"青虚浦"``:[story_qinxu,story_record],
    * ``"归离"``:[story_guili_1,story_guili_2,story_guili_3,story_guili_4],
    * ``"石鸢"``:[story_stone_bird, story_record],
    * ``"千岩军"``:[story_qianyan_army],
    * ``"层岩"``:[story_cenyan_1,story_cenyan_2],
    * ``"伏龙树"``:[story_fulong],
    * ``"契约"``:[story_contract],
    * ``"千岩古剑"``:[story_sword,story_record],
    * ``"千岩长枪"``:[story_spear],
    * ``"碧水原"``:[story_bishui,story_record],
    * ``"寒武"``:[story_hanwu],
    * ``"天衡山"``:[story_tianheng],
    * ``"岩晶蝶"``:[story_tianheng],
    * ``"语音故事"``:[story_record]
    """
    return re_dict
