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
