# %%
import pandas as pd
import numpy as np
import scipy.stats as stats
import collections

MetaBond = collections.namedtuple('Bond',('name', 'info'))

def read_data():
    dfRaw = pd.read_csv('./excel1.csv',encoding='gbk').set_index('DateTime')
    dfRaw2 = pd.read_csv('./excel2.csv',encoding='gbk').set_index('DateTime')
    return dfRaw, dfRaw2

class Bond1:
    def __init__(self, stock, K ):
        self.stock = stock
        self.sigma, self.sigma_y = self.get_sigma(self.stock)
        self.C1 = self.get_C(stock)

    def get_sigma(self, stock): 
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

    def get_C(self, stock):
        def especially_small(C):
            for i, item in enumerate(C.values.tolist()):
                if item < 1e-4:
                    C.iat[i] = 0
            return C
        T = len(stock) / 250 
        up = np.log(stock / K) + T * (r - q + np.power(self.sigma,2)/2)
        down = self.sigma * np.sqrt(T)
        d1 = up / down
        d2 = d1 - down
        C = stock * stats.norm(0,1).cdf(d1) - K* np.exp(-1*r*T) * stats.norm(0,1).cdf(d2)
        C = especially_small(C)
        return C


class Bond2:
    def __init__(self,interest_list):
        self.interest_list = interest_list
        self.C2 = self.get_C2()

    def get_C2(self):
        def f(l,n):
            return l/np.power(1+r,n)
        total = 0 
        for i, item in enumerate(self.interest_list):
            l = item
            n = i+1
            total += f(l,n)
        return total

class Bond:
    def __init__(self, bond1, bond2, bond_name):
        self.C1, self.C2 = bond1.C1, bond2.C2
        self.name = bond_name
        self.value = self.C1 + self.C2

class Bondbook:
    def __init__(self):
        self.content = []
    
    def add_bond(self, name, value):
        self.content.append(MetaBond(name, value))

if __name__ == "__main__":
    dfRaw, dfRaw2 = pd.DataFrame(), pd.DataFrame()
    if (len(dfRaw)==0) or (len(dfRaw2)==0):
        dfRaw, dfRaw2 = read_data()

    list1=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5]
    bond_price = dfRaw.iloc[:,0]
    bond_name = pd.DataFrame(dfRaw.iloc[:,0]).columns.tolist()[0]
    stock = dfRaw2.iloc[:,0]
    K = 37.97
    r = 0.02277500 # 2020年5月27日的五年期的国债收益率
    # 持有到期可获得收益率，[债券分红, 到期的溢价]，折算到现在
    q = 0

    bond = Bond(Bond1(stock, K), Bond2(list1), bond_name)
    bondbook = Bondbook()
    bondbook.add_bond(bond.name, bond.value)

    bond_price = dfRaw.iloc[:,0]
    arbitrage = bond_price - bond.value

    print("Done")





# %%
