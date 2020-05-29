import math
import concurrent
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
dfRaw, dfRaw2 = pd.DataFrame(), pd.DataFrame()
# 全局变量

# ============================================================================== #
# 以下是容器
class Attr:
    '''Attribute
    '''
    def __init__(self):
        self.value = None
    
    def add_value(self, value):
        self.value = value 

class Bond:
    bond_name_list = []
    def __init__(self):
        self._attrs = {}
    def attr(self, name):
        if name not in self._attrs:
            self._attrs[name] = Attr()
        return self._attrs[name]    


class Bondbook:
    def __init__(self):
        self._bonds = {}
    def bond(self, name):
        if name not in self._bonds:
            self._bonds[name] = Bond()
            Bond.bond_name_list.append(name)
        return self._bonds[name]

# ============================================================================== #
# 以下是函数
class GetAtts:
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
    def get_sgima(stock):
        '''获得股票的波动率，序列数据
        Args:
            
        '''
        
        return sigma_df
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
        
    # @staticmethod
    # def get_C2(#TODO):

    #     return C2
    @staticmethod
    def get_C0(interest_list):
        length = len(interest_list)
        def f(l,n):
            return l*np.power(1 + rf, length - n)
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

# ------------------------------------------------------------------------------ #       
 
class GlobalFunctions:
    @staticmethod
    def save_info(i):
        bond_name = Bond.bond_name_list[i]
        book.bond(bond_name).attr('Arbitrage').value.to_csv('./output/'+bond_name+'.csv',mode='w+')
        # 可转债的套利空间保存为csv文件
    @staticmethod
    def read_data():
        name_list = ['excel1', 'excel2']
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(name_list)) as executor: # 并行读入文件
            results = list(executor.map(lambda file_name: pd.read_csv('./'+file_name+'.csv',encoding='gbk').set_index('DateTime'), name_list))
        dfRaw, dfRaw2 = results[0], results[1]
        return dfRaw, dfRaw2
    @staticmethod
    def draw_scatter(i):
        # 正股股价和溢价率的散点图
        bond_name = Bond.bond_name_list[i]
        temp_bond = book.bond(bond_name) # 获得指定债券的实例
        x = temp_bond.attr('Stock_Price').value
        y = temp_bond.attr('Premium_Rate').value
        plt.scatter(x, y)
        plt.xlabel('Stock_Price')
        plt.ylabel('Premium_Rate')
        plt.show()
    @staticmethod
    def draw_line(i):
        bond_name = Bond.bond_name_list[i]
        temp_bond = book.bond(bond_name) # 获得指定债券的实例
        y1_series = temp_bond.attr('Stock_Price').value # 正股价格
        y2_series = temp_bond.attr('Value_Series').value # 转股价值
        time_line = y1_series.index.tolist() # 时间序列
        y1 = y1_series.values.tolist()
        y2 = y2_series.values.tolist()
        plt.plot(time_line, y1, label = 'Stock_Price')
        plt.plot(time_line, y2, label = 'Value_Series')
        plt.legend()
        plt.show()
    @staticmethod
    def draw_figure(i):
        GlobalFunctions.draw_scatter(i)
        # GlobalFunctions.draw_line(i)
    @staticmethod
    def show_info(i):
        GlobalFunctions.save_info(i)
        GlobalFunctions.draw_figure(i)
    @staticmethod
    def set_up(i, K_dict):
        # 初始化每一个债券
        # 从外部传入数据 TODO 改成函数，不要从文件中读取
        bond_price = dfRaw.iloc[:,i]
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        stock = dfRaw2.iloc[:,i]
        # 所有可转债
        bond1 = book.bond(bond_name)
        # 实例化一个可转债对象
        
        bond1.attr('C0').add_value(GetAtts.get_C0(list1))
        # 设置债券到期价值C0的值
        
        bond1.attr('r').add_value(GetAtts.get_r(bond1.attr('C0').value))
        # 设置可转债的收益率，单值数据
        
        bond1.attr('T').add_value(GetAtts.get_T(#TODO))
        # 设置可转债的到期年限，序列数据
        
        bond1.attr('sigma').add_value(GetAtts.get_sgima(#TODO))
        # 设置可转债的波动率，序列数据
        
        bond1.attr('K').add_value(GetAtts.get_K(stock.index.values.tolist(), K_dict)) 
        # 设置期权的行权价K TODO 序列数据
        
        bond1.attr('C1').add_value(GetAtts.get_C1(stock, bond1.attr('r').value, bond1.attr('K').value, bond1.attr('T').value))
        # 设置期权价值C1 序列数据
        
        # bond1.attr('C2').add_value(GetAtts.get_C2(#TODO))
        # 设置期纯债价值C2 序列数据
        
        bond1.attr('Arbitrage').add_value(bond1.attr('C1').value + bond1.attr('C0').value - bond_price)
        # 设置可转债的套利属性
        
        bond1.attr('Value_Series').add_value(GetAtts.get_Value_Series(bond1.attr('K').value, stock))
        # 设置可转债的转股价值
        
        bond1.attr('Premium_Rate').add_value(GetAtts.get_Premium_Rate(bond_price, bond1.attr('Value_Series').value))
        # 设置可转债的转股溢价率
        
        bond1.attr('Stock_Price').add_value(stock)# 设置正股股价
        bond1.attr('Bond_Price').add_value(bond_price)# 设置可转债价格

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

    GlobalFunctions.set_up(0, K1_dict)
    GlobalFunctions.show_info(0)
    print("Done")

