# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import collections
dfRaw, dfRaw2 = pd.DataFrame(), pd.DataFrame()
# 全局变量
# 以下是容器
class Attribute:
    def __init__(self):
        self._values = []
    
    def add_value(self, value):
        self._values.append(value)
    
    def value(self):
        return self._values[0]

class Bond:
    def __init__(self):
        self._attributes = {}
        self.r = np.nan
        self.T = np.nan
    def attribute(self, name):
        if name not in self._attributes:
            self._attributes[name] = Attribute()
        return self._attributes[name]    
    def set_r(self, r):
        self.r = r
        return self.r
    def set_T(self, T):
        self.T = T
        return self.T

class Bondbook:
    def __init__(self):
        self._bonds = {}
    def bond(self, name):
        if name not in self._bonds:
            self._bonds[name] = Bond()
        return self._bonds[name]
# ============================================================================== #
# 以下是函数
class GetAttributes:
    @staticmethod
    def get_r( interest_list, price, T):
        # r = (sum(interest_list) - price) / (price * T)
        # r = 0.02277500
        r = np.power(sum(interest_list)/100, 1/6) - 1
        return r 
    @staticmethod
    def get_T( stock):
        # 这里要求股票的开始时间必须和债券的开始时间相同
        total_year_length = 6
        passed_year_length = len(stock)/250
        T = total_year_length - passed_year_length
        return T
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
            return sigma, sigma_total
        def especially_small(C):
            for i, item in enumerate(C.values.tolist()):
                if item < 1e-4:
                    C.iat[i] = 0
            return C
        sigma, sigma_y = get_sigma(stock)
        up = np.log(stock / K) + T * (r - q + np.power(sigma,2)/2)
        down = sigma * np.sqrt(T)
        d1 = up / down
        d2 = d1 - down
        C = stock * stats.norm(0,1).cdf(d1) - K* np.exp(-1*r*T) * stats.norm(0,1).cdf(d2)
        C = especially_small(C)
        return C
    @staticmethod
    def get_C2(interest_list, r):
        def f(l,n):
            return l/np.power(1 + r,n)
        total = 0 
        for i, item in enumerate(interest_list):
            l = item
            n = i+1
            total += f(l,n)
        return total
    @staticmethod
    def get_Value_Series(K, stock):
        Value_Series = (100/K) * stock
        return Value_Series
    @staticmethod
    def get_Premium_Rate(bond_price, Value_Series):
        Premium_Rate = (bond_price - Value_Series)/ Value_Series
        return Premium_Rate
class GlobalFunctions:
    @staticmethod
    def set_up(i, K):
        # 初始化每一个债券
        bond_price = dfRaw.iloc[:,i]
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        stock = dfRaw2.iloc[:,i]
        # 所有可转债
        bond1 = book.bond(bond_name)
        # 示例化一个可转债对象
        book.bond(bond_name).set_r(GetAttributes.get_r(list1, bond_price , len(stock)))
        book.bond(bond_name).set_T(stock)
        # 传入r和T的值
        bond1.attribute('T').add_value(GetAttributes.get_T(stock))
        bond1.attribute('K').add_value(K)
        bond1.attribute('C1').add_value(GetAttributes.get_C1(stock, book.bond(bond_name).r, K, book.bond(bond_name).T))
        bond1.attribute('C2').add_value((GetAttributes.get_C2(list1, book.bond(bond_name).r)))
        # 设置不同属性的值
        value = book.bond(bond_name).attribute('C1').value() + book.bond(bond_name).attribute('C2').value()
        bond1.attribute('Arbitrage').add_value(value - bond_price)
        # 设置可转债的套利属性
        book.bond(bond_name).attribute('Value_Series').add_value(GetAttributes.get_Value_Series(K, stock))
        # 设置可转债的转股价值
        book.bond(bond_name).attribute('Premium_Rate').add_value(GetAttributes.get_Premium_Rate(bond_price, book.bond(bond_name).attribute('Value_Series').value()))
        # 设置可转债的转股溢价率
        book.bond(bond_name).attribute('Stock_Price').add_value(stock)
        # 设置正股股价
    @staticmethod
    def save_info(i):
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        temp = book.bond(bond_name).attribute('Arbitrage').value()
        # print(temp)
        # 输出可转债的套利空间
        temp.to_csv('./output/'+bond_name+'.csv',mode='w+')
        # 可转债的套利空间保存为csv文件
        print("Done")
    @staticmethod
    def read_data():
        dfRaw = pd.read_csv('./excel1.csv',encoding='gbk').set_index('DateTime')
        dfRaw2 = pd.read_csv('./excel2.csv',encoding='gbk').set_index('DateTime')
        return dfRaw, dfRaw2
    @staticmethod
    def draw_scatter(i):
        # 正股股价和溢价率的散点图
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        temp_bond = book.bond(bond_name) # 获得指定债券的实例
        x = temp_bond.attribute('Stock_Price').value()
        y = temp_bond.attribute('Premium_Rate').value()
        plt.scatter(x, y)
        plt.xlabel('Stock_Price')
        plt.ylabel('Premium_Rate')
        plt.show()
    @staticmethod
    def draw_line(i):
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        temp_bond = book.bond(bond_name) # 获得指定债券的实例
        y1_series = temp_bond.attribute('Stock_Price').value() # 正股价格
        y2_series = temp_bond.attribute('Value_Series').value() # 转股价值
        time_line = y1_series.index.tolist() # 时间序列
        y1 = y1_series.values.tolist()
        y2 = y2_series.values.tolist()
        plt.plot(time_line, y1, label = 'Stock_Price')
        plt.plot(time_line, y2, label = 'Value_Series')
        plt.legend()
        plt.show()
# ============================================================================== #

if __name__=='__main__':
    # 主函数 
    if (len(dfRaw)==0) or (len(dfRaw2)==0):
        dfRaw, dfRaw2 = GlobalFunctions.read_data()
    # 获得数据

    q = 0 # q应该设置成什么我们也不知道
    book = Bondbook()
    # 设置可转债的基本指标
    # 对于所有可转债

    list1=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5] # 债券1的利息表
    K1 = 37.97 # 债券1的行权价
    list2=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5]
    K2 = 20.22 # 债券2的行权价
    # 对于每一个可转债

    GlobalFunctions.set_up(0, K1)
    GlobalFunctions.save_info(0)
    GlobalFunctions.draw_scatter(0)
    GlobalFunctions.draw_line(0)

# %%
