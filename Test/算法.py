# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:10:04 2020

@author: hs101
"""
# 类型注解
import pandas as pd

def get_string(x: pd.DataFrame, y: pd.Series) -> str:
    return x + y
x = pd.DataFrame(index =[0,1],data=[2,3])
y = pd.Series(index =[0,1],data=[2,3])
z = get_string(x, y)

# 28.call
# 可以调用的对象: 一个特殊的魔术方法可以让类的实例的行为表现的像函数一样

class Entity:
    '''调用实体来改变实体的位置。'''
    
    def __init__(self, size, x, y):
        self.x, self.y = x, y
        self.size = 1
    
    def __call__(self, x, y):
        '''改变实体的位置'''
        self.x, self.y = x, y

e = Entity(1, 2, 3) # 创建实例
e(4, 5) # 实例可以象函数那样执行，并传入x y值，修改对象的x y

# 53.字典推导式
# 将字符串 str1 = "k:1 |k1:2|k2:3|k3:4"，处理成字典 {k:1,k1:2,...}
# d = {key:value for (key,value) in iterable}
d = {k:int(v) for t in str1.split("|") for k, v in (t.split(":"), )}