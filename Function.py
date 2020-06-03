# 以下是函数
#import math
from Adapter import GlobalFunctions
import scipy.stats as stats
import pandas as pd
import numpy as np
class GetAttrs:
    '''计算得到，容器Bond内的属性，用容器Attr容纳
    '''
    rf = 0.022956 # 设置无风险利率，类属性
    @staticmethod
    def get_C0(interest_list):
        '''债券到期的终值
        #TODO根据付息日不同，应该有六个值
        '''
        length = len(interest_list)
        def f(l,n):
            return l*np.power(1 + GetAttrs.rf, length - n)
        total = 0
        for i, item in enumerate(interest_list):
            total += f(item,i+1)
        return total
    @staticmethod
    def get_r(C0):
        r = np.power(C0/100, 1/6) - 1
        return r
    @staticmethod
    def get_T(time_list, stock):
        ''' 债券的存续时间序列
        这里要求股票的开始时间必须和债券的开始时间相同
        Args:
            start_point_string: string, 债券开始的时间，eg: start_point_string = '2019-02-15'
            end_point_string: string, 债券结束时间，eg: end_point_string = '2025-02-15'
            stock: dataframe[n*1], 用于数据对齐
        Return:
            pd.DataFrame: (存续天数 * 1), (columns = ['T']), 距离到期还有多少年
        '''
        start_point_string, end_point_string = time_list[0], time_list[1]
        date_index = pd.date_range(start_point_string, end_point_string).strftime('%Y-%m-%d')
        T = pd.DataFrame(index = date_index ,columns = ['T'])
        for i in range(T.shape[0]):
            T.iat[i,0] = (len(date_index)- (i+1))/365.333
        T = GlobalFunctions.series_align(stock, T)
        return T
    @staticmethod
    def get_K(time_list, time_price_dict):
        '''得到行权价的时间序列K
        Args:
            time_list: list, stock.index.values.tolist()
            time_price_dict: dict, {'2019-02-15':37.97, '2019-08-22':22.22}
        '''
        K = pd.DataFrame(index = time_list, data = [np.nan for i in range(len(time_list))])
        for key, value in time_price_dict.items():
            K.loc[key] = value
        K = K.fillna(method='ffill')
        return K
    @staticmethod
    def get_sgima(stock_df):
        '''获得股票的波动率，序列数据
        Args:
            stock_df: 正股的收盘价
        Returns:
            股票的年波动率
        '''
        stock_ln_df = np.log(stock_df)
        miu = stock_ln_df.diff().fillna(method='bfill')
        sigma_df = pd.DataFrame(index= stock_df.index.values.tolist(), columns=['simga'])
        for i in range(2, sigma_df.shape[0]):
            temp_miu = miu.iloc[1:i+1]
            temp_miu_avr = temp_miu.mean()
            total = 0
            for j in range(len(temp_miu)):
                total += np.power(temp_miu.iloc[j] - temp_miu_avr, 2)
            total = np.sqrt(total/(len(temp_miu) - 1))
            sigma_df.iat[i,0] = total
            sigma_df = sigma_df.fillna(method='bfill')
        sigma_df = sigma_df * np.sqrt(250)
        return sigma_df

    @staticmethod
    def get_C1(stock, r, K, T, sigma):
        def especially_small(C):
            for i, item in enumerate(C.values.tolist()):
                if item < 1e-4:
                    C.iat[i] = 0
            return C
        sigma_y = GlobalFunctions.check_if_series(sigma)
        K = GlobalFunctions.check_if_series(K)
        T = GlobalFunctions.check_if_series(GlobalFunctions.series_align(K, T))
        front = GlobalFunctions.check_if_series(np.log(stock / K))
        back = GlobalFunctions.check_if_series((T * (r + np.power(sigma_y,2)/2)))
        up = front + back
        down = sigma_y * np.power(T, 0.5)
        d1 = up / down
        d2 = d1 - down
        C = stock * stats.norm(0,1).cdf(d1.astype(float)) - K* np.exp((-1*r*T).astype(float)) * stats.norm(0,1).cdf(d2.astype(float))
        C = especially_small(C)
        return C
    @staticmethod
    def get_C2(C0, T):
        '''得到纯债的价值C2, 是个时间序列数据。
        Args:
            C0: 债券的到期价值，单值数据
            T: 整个债券的存续期
        '''
        C2 = pd.Series(index = T.index.values.tolist())
        for i in range(T.shape[0]):
            C2.iat[i] = C0 / np.power((1 + GetAttrs.rf), T.iloc[i,0])
        return C2
    @staticmethod
    def get_Value_Series(K, stock):
        '''设置可转债的转股价值
        (100/转股价格) * 正股价格
        Parameters
        ----------
        K : dataframe
            可转债的转股价.
        stock : datframe
            正股的股价.

        Returns
        -------
        Value_Series : dataframe
            可转债的转股价值.

        '''
        K = GlobalFunctions.check_if_series(K)
        Value_Series = (100/K) * stock
        return Value_Series
    @staticmethod
    def get_Premium_Rate(bond_price, Value_Series):
        Premium_Rate = (bond_price - Value_Series)/ Value_Series
        return Premium_Rate
    @staticmethod
    def get_Bond_Value(C1, C2):
        '''
        计算可转债的价值
        纯债价值 + 期权价值
        Parameters
        ----------
        C1 : DataFrame
            期权价值.
        C2 : DataFrame
            纯债价值.

        Returns
        -------
        Bond_Value : DataFrame
            可转债价值.

        '''
        Bond_Value = C1 + C2
        return Bond_Value
