import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 项目文件.数据清洗 import get_data


def gains_delta_neutral(path_option):

    data=pd.read_csv(path_option)

    pass


#计算期权delta中性收益
#参考陈蓉（2011），波动率风险溢酬:时变特征及影响因素
class DeltaNeutralGains():

    def __init__(self,path_option
                 ):
        self.option= pd.read_csv(path_option)
        self.option.drop_duplicates(inplace=True)
        
        self.def_col()#定义列标题
        self.filter()#筛选样本

        self.trade_dates=self.option[self.col_TradingDate].unique().tolist()#交易日期
        self.expiration=np.sort(self.option[self.col_ExerciseDate].unique().tolist())#到期日期
        self.tao=1/365

    #按照陈蓉(2011)的方法筛选样本
    def filter(self):
        #剔除交易日高于60天的期权样本
        self.option=self.option[self.option[self.col_RemainingTerm]<=60/365]
        #剔除实值期权
        self.option=self.option[self.option[self.col_Delta].abs()<=0.5]




    #为了调用方便，定义列标题
    def def_col(self):
        
        self.col_SecurityID='SecurityID'
        self.col_Symbol='Symbol'
        self.col_ExchangeCode='ExchangeCode'
        self.col_ContractCode='ContractCode'
        self.col_ShortName='ShortName'
        self.col_CallOrPut='CallOrPut'
        self.col_StrikePrice='StrikePrice'
        self.col_ExerciseDate='ExerciseDate'
        self.col_TradingDate='TradingDate'
        self.col_ClosePrice='ClosePrice'
        self.col_UnderlyingScrtClose='UnderlyingScrtClose'
        self.col_RemainingTerm='RemainingTerm'
        self.col_RisklessRate='RisklessRate'
        self.col_HistoricalVolatility='HistoricalVolatility'
        self.col_ImpliedVolatility='ImpliedVolatility'
        self.col_TheoreticalPrice='TheoreticalPrice'
        self.col_Delta='Delta'
        self.col_Gamma='Gamma'
        self.col_Vega='Vega'
        self.col_Theta='Theta'
        self.col_Rho='Rho'
        self.col_SettlePrice='SettlePrice'
        self.col_Volume='Volume'
        self.col_Position='Position'
        self.col_Amount='Amount'
        


    #计算指定合约在某个交易日的未来一个月内的delta中性收益
    def gains_to_maturity(self,
                          date='',
                          ):


        Symbol=10001174
        TradingDate='2018-01-26'
        data=self.option[(self.option[self.col_Symbol]==Symbol)&(self.option[self.col_TradingDate]>=TradingDate)]



    def run(self):

        #计算次日股票价格
        ETF=self.option[[self.col_TradingDate,self.col_UnderlyingScrtClose]].drop_duplicates().sort_values(self.col_TradingDate)
        ETF['next_Underlying']=self.option[self.col_UnderlyingScrtClose].shift(-1)
        self.option=pd.merge(self.option,ETF[[self.col_TradingDate,'next_Underlying']],on=[self.col_TradingDate])


        self.option['pre_Price']=self.option[self.col_ClosePrice]/(1+self.option['Change1'])
        self.option['gains']=self.option['next_Close']-self.option[self.col_ClosePrice]-self.option[self.col_Delta]*\
        (self.option['next_Underlying']-self.option[self.col_UnderlyingScrtClose])-self.option[self.col_RisklessRate]/100* \
                             (self.option[self.col_ClosePrice]-self.option[self.col_Delta]*self.option[self.col_UnderlyingScrtClose])*self.tao
        self.option['gains'].describe()

        self.option.to_csv(data_real_path('数据文件/生成数据')+'/陈蓉2011delta中性收益率.csv',encoding='utf_8_sig',index=False)




















        for date in self.expiration:
            for type in self.option[self.col_CallOrPut].unique():
                data=self.option[(self.option[self.col_ExerciseDate]==date)&(self.option[self.col_CallOrPut]==type)]
                optionCodes=data[self.col_ContractCode].unique()
                for optionCode in optionCodes:
                    data_=data[data[self.col_ContractCode]==optionCode]





                pass












if __name__=='__main__':
    path_option=data_real_path('数据文件/生成数据/上证50ETF期权数据.csv')

    DNG=DeltaNeutralGains(path_option)
    DNG.run()


    DNG.gains_to_maturity()
    data=DNG.option[(DNG.option['TradingDate']=='2018-01-26')]
    data.sort_values([DNG.col_CallOrPut, DNG.col_RemainingTerm, DNG.col_Delta])


















