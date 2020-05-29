import concurrent
import matplotlib.pyplot as plt
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