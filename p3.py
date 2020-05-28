# %%
from time import *
from concurrent.futures import *
def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [(193309, 2265973), (2030677, 3814172),
            (1551645, 2229620), (2039045, 2020802)]
start = time()
pool = ProcessPoolExecutor(max_workers=2)
results = list(pool.map(gcd, numbers))
end = time()
print(end - start)
# %%
from concurrent.futures import *
import pandas as pd
def read_data(name_list):  
    def read_it(file_name):
        return pd.read_csv('./'+file_name+'.csv',encoding='gbk').set_index('DateTime')  
    pool = ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(read_it, name_list))
    return results
name_list = ['excel1', 'excel2']
dataRaw = read_data(name_list)
    # dfRaw = pd.read_csv('./excel1.csv',encoding='gbk').set_index('DateTime')
    # dfRaw2 = pd.read_csv('./excel2.csv',encoding='gbk').set_index('DateTime')
    # return dfRaw, dfRaw2


# %%
from concurrent.futures import *
import pandas as pd
name_list = ['excel1', 'excel2']
def read_it(file_name):
    output = pd.read_csv('./'+file_name+'.csv',encoding='gbk').set_index('DateTime')
    return output
pool = ProcessPoolExecutor(max_workers=2)
results = list(pool.map(read_it, name_list))


# %%
