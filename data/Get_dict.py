from functools import partial
from .wordbank import wordbank_dic

class Get_dict:
    def __getattr__(self,name:str):
        return partial(self.call_api,name)

    def call_api(self,key:str)  -> str :
        v=self.dict.get(key)
        if v:
            return v
        raise KeyError

    def __init__ (self):
    # 这里写你的词库字典
        self.dict: dict = wordbank_dic

dailyChat_dict= Get_dict()

# dailyChat_dict