class SetUp:
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
        
        bond1.attr('C0').add_value(GetAttrs.get_C0(list1))
        # 设置债券到期价值C0的值
        
        bond1.attr('r').add_value(GetAttrs.get_r(bond1.attr('C0').value))
        # 设置可转债的收益率，单值数据
        
        bond1.attr('T').add_value(GetAttrs.get_T(#TODO))
        # 设置可转债的到期年限，序列数据
        
        bond1.attr('sigma').add_value(GetAttrs.get_sgima(#TODO))
        # 设置可转债的波动率，序列数据
        
        bond1.attr('K').add_value(GetAttrs.get_K(stock.index.values.tolist(), K_dict)) 
        # 设置期权的行权价K TODO 序列数据
        
        bond1.attr('C1').add_value(GetAttrs.get_C1(stock, bond1.attr('r').value, bond1.attr('K').value, bond1.attr('T').value))
        # 设置期权价值C1 序列数据
        
        # bond1.attr('C2').add_value(GetAttrs.get_C2(#TODO))
        # 设置期纯债价值C2 序列数据
        
        bond1.attr('Arbitrage').add_value(bond1.attr('C1').value + bond1.attr('C0').value - bond_price)
        # 设置可转债的套利属性
        
        bond1.attr('Value_Series').add_value(GetAttrs.get_Value_Series(bond1.attr('K').value, stock))
        # 设置可转债的转股价值
        
        bond1.attr('Premium_Rate').add_value(GetAttrs.get_Premium_Rate(bond_price, bond1.attr('Value_Series').value))
        # 设置可转债的转股溢价率
        
        bond1.attr('Stock_Price').add_value(stock)# 设置正股股价
        bond1.attr('Bond_Price').add_value(bond_price)# 设置可转债价格