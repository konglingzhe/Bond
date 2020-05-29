# 以下是函数
import math
import scipy.stats as stats
import pandas as pd
import numpy as np
class GetAttrs:
    rf = 0.022956 # 设置无风险利率
    @staticmethod
    def get_r(C0):
        r = np.power(C0/100, 1/6) - 1
        return r 
    @staticmethod
    def get_T(start_point_string, end_point_string):
        ''' 这里要求股票的开始时间必须和债券的开始时间相同
        Args:
            start_point_string: string, 债券开始的时间，eg: start_point_string = '2019-02-15'
            end_point_string: string, 债券结束时间，eg: end_point_string = '2025-02-15'
        '''
        date_index = pd.date_range(start_point_string, end_point_string)
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
        miu = stock_ln_df.diff().iloc[1:]
        sigma_df = pd.DataFrame(index= stock_df.index.values.tolist(), columns=['simga'])
        for i in range(sigma_df.shape[0]):
            temp_miu = miu.iloc[i:]
            temp_miu_avr = temp_miu.mean()
            total = 0
            for j in range(len(temp_miu)):
                total += np.power(temp_miu.iloc[i] - temp_miu_avr, 2)
            total = np.sqrt(total/(len(temp_miu) - 1))
            sigma_df.iat[i,0] = total
        sigma_df.fillna(method='ffill')
        return sigma_df

#    @staticmethod
#    def get_C1(stock, r, K, T):
#        def get_sigma(stock): 
#            stock_ln = np.log(stock)
#            miu = stock_ln.diff()
#            miu = miu.iloc[1:]
#            miu_avr = miu.mean()
#            total=0
#            for i in range(len(miu)):
#                total += np.power(miu.iloc[i] - miu_avr,2)
#            sigma = np.sqrt(total/(len(miu)-1))
#            sigma_total = sigma * np.sqrt(250)
#            return sigma_total
#        def especially_small(C):
#            for i, item in enumerate(C.values.tolist()):
#                if item < 1e-4:
#                    C.iat[i] = 0
#            return C
#        def check_if_series(x):
#            if type(x)!="<class 'pandas.core.frame.Series'>":
#                x = pd.Series(index=x.index.values.tolist(),data=x.iloc[:,0])
#            return x
#        sigma_y = get_sigma(stock)
#        K = check_if_series(K)
#        up = np.log(stock / K) + T * (r + np.power(sigma_y,2)/2)
#        down = sigma_y * np.sqrt(T)
#        d1 = up / down
#        d2 = d1 - down
#        C = stock * stats.norm(0,1).cdf(d1) - K* np.exp(-1*r*T) * stats.norm(0,1).cdf(d2)
#        C = especially_small(C)
#        return C

    @staticmethod
    def get_C1(S0, K, r, T, sigma):             
        def bsformula(callput, S0, K, r, T, sigma, q=0):
            def norminv(x):
                return ((1.0/math.sqrt(2.0*math.pi)) * math.exp(-x*x*0.5))
            
            def d1(S0, K, r, T, sigma, q):
                deno = (sigma * math.sqrt(T))
                if (deno==0):
                    return 0
                logReturns = math.log(S0/float(K)) if ((S0/float(K)) > 0.0) else 0.0
                return (float(logReturns) + (float(r) - float(q) + float(sigma)*float(sigma)*0.5)*float(T)) / float(deno)
                
            def d2(S0, K, r, T, sigma, q):
                    return d1(S0, K, r, T, sigma, q)-sigma*math.sqrt(T)
            N = stats.norm.cdf
                        
            def optionValueOfCall(S0, K, r, T, sigma, q):       
                _d1 = d1(S0, K, r, T, sigma, q)
                _d2 = d2(S0, K, r, T, sigma, q)
                return S0*math.exp(-q*T)*N(_d1)- K*math.exp(-r*T)*N(_d2)
              
            def optionValueOfPut(S0, K, r, T, sigma, q):
                _d1 = d1(S0, K, r, T, sigma, q)
                _d2 = d2(S0, K, r, T, sigma, q)
                return float(K)*math.exp(-float(r)*float(T))*N(-_d2) - float(S0)*math.exp(-float(q)*float(T))*N(-_d1)
                
            def delta(callput, S0, K, r, T, sigma, q):
                _d1 = d1(S0, K, r, T, sigma, q)        
                if callput.lower() == "call":            
                    return N(_d1) * math.exp(-q*T)
                else:
                    return (N(_d1)-1)* math.exp(-q*T)
            
            def vega(S0, K, r, T, sigma, q):
                _d1 = d1(S0, K, r, T, sigma, q)
                return S0  * math.sqrt(T) * norminv(_d1)  * math.exp(-q*T)
            
            if callput.lower()=="call":
                optionValue = optionValueOfCall(S0, K, r, T, sigma, q)
            else:
                optionValue = optionValueOfPut(S0, K, r, T, sigma, q)
                
            _delta = delta(callput, S0, K, r, T, sigma, q)
            _vega = vega(S0, K, r, T, sigma, q)
            
            return (optionValue, _delta, _vega)
        return bsformula('call', S0, K, r, T, sigma, q=0)[0]

    # @staticmethod
    # def get_C2(#TODO):

    #     return C2
    
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
    def get_Value_Series(K, stock):
        Value_Series = (100/K) * stock
        return Value_Series
    @staticmethod
    def get_Premium_Rate(bond_price, Value_Series):
        Premium_Rate = (bond_price - Value_Series)/ Value_Series
        return Premium_Rate
