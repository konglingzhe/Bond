import math
import concurrent
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
# ============================================================================== #
from Container import Attr, Bond, Bondbook
import GetAttrs
import GlobalFunctions
import SetUp 
# ============================================================================== #
# 全局变量
dfRaw, dfRaw2 = pd.DataFrame(), pd.DataFrame()
# ============================================================================== #


if __name__=='__main__':
    # 主函数 
    if (len(dfRaw)==0) or (len(dfRaw2)==0):
        dfRaw, dfRaw2 = GlobalFunctions.read_data()
    # 获得数据

    rf = 0.022956 # 设置无风险利率
    book = Bondbook()
    # 设置可转债的基本指标
    # 对于所有可转债

    list1=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5] # 债券1的利息表
    # K1 = 37.97 # 债券1的行权价
    K1_dict = {
        '2019-02-15':37.97,
        '2019-05-31':22.28,
         '2020-05-22':22.22
         }
    # 债券1的行权价
    list2=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5]
    K2 = 20.22 # 债券2的行权价
    # 对于每一个可转债

    SetUp.set_up(0, K1_dict)
    GlobalFunctions.show_info(0)
    print("Done")

