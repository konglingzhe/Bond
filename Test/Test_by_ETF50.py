'''
Dependence:
    Convertible_Bond.py
    
'''
import pandas as pd
import sys
sys.path.append("..")
# 调用上一层的文件
# ------------------------------------------------------------------------------ #
from WindPy import w
# ------------------------------------------------------------------------------ #
from Container import Bondbook
from Function import GetAttrs
from Adapter import GlobalFunctions
# ============================================================================== #

dfRaw, dfRaw2 = pd.DataFrame(), pd.DataFrame()
# 全局变量
# ============================================================================== #
class SetUp:
    @staticmethod
    def set_up(i, K_dict, time_list):
        '''初始化每一个债券
        Args:
            i: 表中位置，后续要改掉
            K_dict: dict, 行权价的时间字典
            time_list: list, 债券开始时间和结束时间列表
        '''
        # 从外部传入数据 TODO 改成函数，不要从文件中读取
        w.start()
        bond_price = w.wsd("10002339.SH", "us_close", "2019-01-01", "2020-05-29", "",usedf=True)[0]
        # 50ETF购2020年4月 3.00
        bond_name = 'ETF50'
        stock = w.wsd("510050.SH", "nav", "2019-01-01", "2020-05-29", "period=2;returnType=1",usedf=True)[0]
        # 所有上证ETF50时间序列上的数据
        bond1 = book.bond(bond_name)
        # 实例化一个可转债对象

        bond1.attr('C0').add_value(GetAttrs.get_C0(list1))
        # 设置债券到期价值C0的值

        bond1.attr('r').add_value(GetAttrs.get_r(bond1.attr('C0').value))
        # 设置可转债的收益率，单值数据

        bond1.attr('T').add_value(GetAttrs.get_T(time_list, stock))
        # 设置可转债的到期年限，序列数据

        bond1.attr('sigma').add_value(GetAttrs.get_sgima(stock))
        # 设置可转债的波动率，序列数据

        bond1.attr('K').add_value(GetAttrs.get_K(stock.index.values.tolist(), K_dict))
        # 设置期权的行权价K TODO 序列数据

        bond1.attr('C1').add_value(GetAttrs.get_C1(stock, bond1.attr('r').value, bond1.attr('K').value, bond1.attr('T').value, bond1.attr('sigma').value))
        # 设置期权价值C1 序列数据

# ============================================================================== #

if __name__=='__main__':
    # 主函数
    if (len(dfRaw)==0) or (len(dfRaw2)==0):
        dfRaw, dfRaw2 = GlobalFunctions.read_data()
    # 获得数据

    book = Bondbook()
    # 设置可转债的基本指标
    # 对于所有可转债


    K1_dict = {
        '2019-02-15':37.97,
        '2019-05-31':22.28,
        '2020-05-22':22.22
         }
    # 债券1的行权价
    time_list = ['2019-02-15', '2025-02-15']
    # 债券1的开始时间和结束时间

    SetUp.set_up(0, K1_dict, time_list)
    GlobalFunctions.show_info(book, 0)
    print("Function: __main__ ... Done!")
    
    
    
    
    
    
    
    
    
    
    
    