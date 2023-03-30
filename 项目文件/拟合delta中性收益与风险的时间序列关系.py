# -*- coding:utf-8 -*-
from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os


#使用面板数据拟合delta中性收益与 波动率 VV 之间的关系
#参考《Volatility-of-Volatility Risk Darien》的(28)
class SeriesOlsGainsAndRisk():

    def __init__(self,
                 bins_moneyness=5,#按照moneyness将数据划分为指定个小组
                 ):
        self.bins_moneyness=bins_moneyness

        #读取数据
        self.gains= pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
        self.IV=pd.read_csv(PATH_IV_SURFACE_SERIES)
        self.RV=pd.read_csv(PATH_RV)
        self.Q_VV=pd.read_csv(PATH_Q_VV)

        self.def_col()
        #self.construct_panel()
        self.combine_data()

    #将收益与波动率数据合并
    def combine_data(self):
        self.gains = pd.merge(self.gains, self.RV, on=[self.col_TradingDate])

        self.Q_VV.columns = [self.col_TradingDate] + [f'QVV{x}' for x in WINDOWS_DAYS]
        self.gains = pd.merge(self.gains, self.Q_VV, on=[self.col_TradingDate])




        self.gains

        self.gains=self.gains[self.gains[C.Delta].abs()<=0.4]

        self.gains_pivot=pd.pivot_table(self.gains,index=[self.col_TradingDate],values=[self.col_Gains,self.col_Gains_to_underlying,self.col_Gains_to_option,'RV']+self.col_Q_VV)

        X=self.gains_pivot[['RV',self.col_Q_VV[0]]]
        X['gains_lag1']=self.gains_pivot[self.col_Gains_to_underlying].shift().fillna(method='bfill')
        Y=self.gains_pivot[self.col_Gains_to_underlying]

        model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)



        pass


    #创建面板数据
    def construct_panel(self,


                        ):

        self.gains[self.col_KS]=self.gains[self.col_StrikePrice]/self.gains[self.col_UnderlyingScrtClose]

        bins = pd.IntervalIndex.from_tuples([(0.95, 0.975), (0.975, 1), (1, 1.025), (1.025, 1.05)])
        self.gains[self.col_KS_bin]=pd.cut(self.gains[self.col_KS],bins)
        self.gains[self.col_KS_bin]=self.gains[self.col_CallOrPut]+self.gains[self.col_KS_bin].astype(str)





        self.gains_pivot=pd.pivot_table(self.gains,index=[self.col_TradingDate],columns=[self.col_KS_bin],values=[self.col_Gains])[self.col_Gains]
        self.gains_pivot=self.gains_pivot.fillna(method='ffill')

        dict_moneyness=dict(zip(self.gains_pivot.columns,range(10)))

        #形成面板数据
        data=[]
        for index_ in self.gains_pivot.index:
            for col_ in self.gains_pivot.columns:
                data.append([index_,dict_moneyness[col_],self.gains_pivot.loc[index_,col_]])
        data=pd.DataFrame(data,columns=[self.col_TradingDate,self.col_KS_bin,self.col_Gains])

        self.RV.rename(columns={'trade_date':self.col_TradingDate},inplace=True)
        col_Q_VV=self.Q_VV.columns[1:]
        self.Q_VV.rename(columns={'trade_date':self.col_TradingDate},inplace=True)



        data=pd.merge(data,self.Q_VV,on=[self.col_TradingDate])
        data=pd.merge(data,self.RV,on=[self.col_TradingDate])

        data.index[self.col_TradingDate]
        data[self.col_Gains]
        data.reset_index(inplace=True)
        data[self.col_TradingDate]=(data[self.col_TradingDate].str[:4]+data[self.col_TradingDate].str[5:7]+data[self.col_TradingDate].str[8:10]).astype(int)

        import statsmodels.api as sm  # 回归
        import statsmodels.formula.api as smf  # 回归
        from linearmodels.panel import PanelOLS  # 面板回归

        col_indvidual = self.col_KS_bin  # 个体轴名称
        col_date = self.col_TradingDate  # 时间轴名称

        # 指定自变量和因变量列标题
        col_X = ['RV',col_Q_VV[1]]
        col_Y = self.col_Gains

        # 面板回归之前，需要先设置“个股在外时间在内”的层次化索引
        data.set_index([col_indvidual, col_date], inplace=True)

        # 指定自变量和因变量
        X = sm.add_constant(data[col_X])
        Y = data[col_Y]

        # 混合回归
        model_pooled = PanelOLS(Y, X, entity_effects=True, time_effects=False)
        model_pooled = model_pooled.fit()
        print(model_pooled)

        self.gains[self.col_delta_bin]=pd.qcut(self.gains[self.col_Gains].abs(), q=self.bins_moneyness)
        pd.pivot_table(self.gains, index=[self.col_TradingDate], columns=[self.col_delta_bin], values=[self.col_Gains], aggfunc=[np.size])




    # 为了调用方便，定义列标题
    def def_col(self):
        self.col_SecurityID = 'SecurityID'
        self.col_Symbol = 'Symbol'
        self.col_ExchangeCode = 'ExchangeCode'
        self.col_ContractCode = 'ContractCode'
        self.col_ShortName = 'ShortName'
        self.col_CallOrPut = 'CallOrPut'
        self.col_StrikePrice = 'StrikePrice'
        self.col_ExerciseDate = 'ExerciseDate'
        self.col_TradingDate = 'TradingDate'
        self.col_ClosePrice = 'ClosePrice'
        self.col_UnderlyingScrtClose = 'UnderlyingScrtClose'
        self.col_RemainingTerm = 'RemainingTerm'
        self.col_RisklessRate = 'RisklessRate'
        self.col_HistoricalVolatility = 'HistoricalVolatility'
        self.col_ImpliedVolatility = 'ImpliedVolatility'
        self.col_TheoreticalPrice = 'TheoreticalPrice'
        self.col_Delta = 'Delta'
        self.col_Gamma = 'Gamma'
        self.col_Vega = 'Vega'
        self.col_Theta = 'Theta'
        self.col_Rho = 'Rho'
        self.col_SettlePrice = 'SettlePrice'
        self.col_Volume = 'Volume'
        self.col_Position = 'Position'
        self.col_Amount = 'Amount'
        self.col_Gains='gains'
        self.col_delta_bin= 'delta_bin'
        self.col_KS = 'KS'
        self.col_KS_bin='KS_bin'
        self.col_Gains_to_option='gains_to_option'#收益/期权价格
        self.col_Gains_to_underlying = 'gains_to_underlying'  # 收益/标的价格
        self.col_RV='RV'



    #普通回归
    def norm_OLS(self):


        pass





























if __name__=='__main__':
    SOGAR=SeriesOlsGainsAndRisk()
    SOGAR.norm_OLS()


    pass











