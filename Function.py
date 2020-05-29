# 以下是函数
#import math
import scipy.stats as stats
import pandas as pd
import numpy as np
class GetAttrs:
    '''计算得到，容器Bond内的属性，用容器Attr容纳
    '''
    rf = 0.022956 # 设置无风险利率，类属性
    @staticmethod
    def get_C0(interest_list):
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
    def get_T(time_list):
        ''' 这里要求股票的开始时间必须和债券的开始时间相同
        Args:
            start_point_string: string, 债券开始的时间，eg: start_point_string = '2019-02-15'
            end_point_string: string, 债券结束时间，eg: end_point_string = '2025-02-15'
        '''
        start_point_string, end_point_string = time_list[0], time_list[1]
        date_index = pd.date_range(start_point_string, end_point_string).strftime('%Y-%m-%d')
        T = pd.DataFrame(index = date_index ,columns = ['T'])
        for i in range(T.shape[0]):
            T.iat[i,0] = (len(date_index)- (i+1))/365.333
        return T
    @staticmethod
    def get_K(time_list, time_price_dict):
        '''得到时间序列K
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
        '''
        stock_ln_df = np.log(stock_df)
        miu = stock_ln_df.diff().fillna(method='bfill')
        sigma_df = pd.DataFrame(index= stock_df.index.values.tolist(), columns=['simga'])
        for i in range(2, sigma_df.shape[0]):
            print(i)
            temp_miu = miu.iloc[1:i+1]
            temp_miu_avr = temp_miu.mean()
            total = 0
            for j in range(len(temp_miu)):
                total += np.power(temp_miu.iloc[j] - temp_miu_avr, 2)
            total = np.sqrt(total/(len(temp_miu) - 1))
            sigma_df.iat[i,0] = total
        return sigma_df.fillna(method='bfill')

    @staticmethod
    def get_C1(stock, r, K, T):
        def get_sigma(stock): 
            stock_ln = np.log(stock)
            miu = stock_ln.diff()
            miu = miu.iloc[1:]
            miu_avr = miu.mean()
            total=0
            for i in range(len(miu)):
                total += np.power(miu.iloc[i] - miu_avr,2)
            sigma = np.sqrt(total/(len(miu)-1))
            sigma_total = sigma * np.sqrt(250)
            return sigma_total
        def especially_small(C):
            for i, item in enumerate(C.values.tolist()):
                if item < 1e-4:
                    C.iat[i] = 0
            return C
        def check_if_series(x):
            if type(x) != pd.core.series.Series:
                x = pd.Series(index=x.index.values.tolist(),data=x.iloc[:,0])
            return x            
        def series_align(K, T):
            '''让T的index保持与K对齐
            '''
            index_list = K.index.values.tolist()
            T = T.reindex(index_list)
            return T
        sigma_y = get_sigma(stock)
        K = check_if_series(K)
        T = check_if_series(series_align(K, T))
        front = check_if_series(np.log(stock / K))
        back = check_if_series((T * (r + np.power(sigma_y,2)/2)))
        up = front + back
        down = sigma_y * np.power(T, 0.5)
        d1 = up / down
        d2 = d1 - down       
        C = stock * stats.norm(0,1).cdf(d1.astype(float)) - K* np.exp((-1*r*T).astype(float)) * stats.norm(0,1).cdf(d2.astype(float))
        C = especially_small(C)
        return C

#    @staticmethod
#    def get_C2(C0, ):
#        '''得到纯债的价值C2, 是个时间序列数据。
#        Args:
#            C0: 债券的到期价值，单值数据
#        '''
#        return C2
    
        
    @staticmethod
    def get_Value_Series(K, stock):
        Value_Series = (100/K) * stock
        return Value_Series
    @staticmethod
    def get_Premium_Rate(bond_price, Value_Series):
        Premium_Rate = (bond_price - Value_Series)/ Value_Series
        return Premium_Rate
