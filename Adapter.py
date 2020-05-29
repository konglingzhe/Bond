from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from Container import Bond
import pandas as pd
import concurrent
import matplotlib.pyplot as plt
class GlobalFunctions:
    @staticmethod
    def line_bar_draw(data,html_name):
        x_data = data.index.tolist()
        bars = data.iloc[:,1].values.tolist()
        change = data.iloc[:,0].values.tolist()
        bar = (
            Bar(init_opts=opts.InitOpts(width="1200px", height="800px"))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="Stock_Price",
                yaxis_data=bars,
                label_opts=opts.LabelOpts(is_show=False),
            )

            .extend_axis(
                yaxis=opts.AxisOpts(
                    name="Value_Series",
                    type_="value",
                )
            )
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                    is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                ),
                yaxis_opts=opts.AxisOpts(
                    name="Stock_Price",
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="￥ {value}"),
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(range_start=0, range_end=100),
                    opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
                ],
            )
        )

        line = (
            Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="Value_Series",
                yaxis_index=1,
                y_axis=change,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        bar.overlap(line).render('./output/'+html_name+'.html')
    @staticmethod
    def save_info(book, i):
        bond_name = Bond.bond_name_list[i]
        book.bond(bond_name).attr('Arbitrage').value.to_csv('./output/'+bond_name+'.csv',mode='w+')
        print('Function: save_info ... Done!')
        # 可转债的套利空间保存为csv文件
    @staticmethod
    def read_data():
        name_list = ['excel1', 'excel2']
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(name_list)) as executor: # 并行读入文件
            results = list(executor.map(lambda file_name: pd.read_csv('./'+file_name+'.csv',encoding='gbk').set_index('DateTime'), name_list))
        dfRaw, dfRaw2 = results[0], results[1]
        return dfRaw, dfRaw2
    @staticmethod
    def draw_scatter(book, i):
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
    def draw_line(book, i):
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
    def draw_figure(book, i):
        GlobalFunctions.draw_scatter(book, i)
        GlobalFunctions.draw_line(book, i)
    @staticmethod
    def show_info(book, i):
        GlobalFunctions.save_info(book, i)
        # GlobalFunctions.draw_figure(book, i)
        y2 = book.bond(Bond.bond_name_list[i]).attr('Stock_Price').value
        y1 = book.bond(Bond.bond_name_list[i]).attr('Value_Series').value
        x = y1.index
        line_bar_df = pd.DataFrame(index = x)
        line_bar_df['y1'], line_bar_df['y2'] = y1, y2
        GlobalFunctions.line_bar_draw(line_bar_df , 'StockPrice_ValueSeries')
    @staticmethod
    def series_align(K, T):
        '''让T的index保持与K对齐
        模板在前，要对其的在后
        '''
        index_list = K.index.values.tolist()
        T = T.reindex(index_list)
        return T
    @staticmethod
    def check_if_series(x):
        if type(x) != pd.core.series.Series:
            x = pd.Series(index=x.index.values.tolist(),data=x.iloc[:,0])
        return x












