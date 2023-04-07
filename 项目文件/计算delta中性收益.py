import Cython.Compiler.TypeSlots
import click.decorators
#import commctrl
import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 项目文件.数据清洗 import get_data
from 数据文件.基本参数 import *


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
        self.tao=1/DAYS_OF_YEAR

    #按照陈蓉(2011)的方法筛选样本
    def filter(self):
        #剔除交易日高于60天的期权样本
        self.option=self.option[self.option[self.col_RemainingTerm]<=60/365]
        # #剔除实值期权
        # self.option=self.option[self.option[self.col_Delta].abs()<=0.5]



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





    def run(self,path_save):

        #计算次日股票价格
        ETF=self.option[[self.col_TradingDate,self.col_UnderlyingScrtClose]].drop_duplicates().sort_values(self.col_TradingDate)#选取option中的交易日和标的资产收盘价，放入ETF表
        ETF['next_Underlying']=ETF[self.col_UnderlyingScrtClose].shift(-1)#ETF表中生成次日标的资产价格
        self.option=pd.merge(self.option,ETF[[self.col_TradingDate,'next_Underlying']],on=[self.col_TradingDate])#把ETF中的交易日和次日标的资产价格与option合并

        #每日delta中性收益计算,用的年利率，要乘1/242
        self.option['gains']=self.option['next_Close']-self.option[self.col_ClosePrice]-self.option[self.col_Delta]*\
        (self.option['next_Underlying']-self.option[self.col_UnderlyingScrtClose])-self.option[self.col_RisklessRate]/100* \
                             (self.option[self.col_ClosePrice]-self.option[self.col_Delta]*self.option[self.col_UnderlyingScrtClose])*self.tao

        #test
        gains=self.option[[C.TradingDate, C.ShortName, C.Delta, C.CallOrPut, C.Gains,C.UnderlyingScrtClose]].dropna()#C.gains就是self.option['gains']
        pd.pivot_table(gains,index=[C.CallOrPut],values=['gains'])#？
        np.corrcoef(gains['gains'],gains[C.UnderlyingScrtClose])#？


        #计算gains/S
        self.option[C.Gains_to_underlying]=self.option[C.Gains]/self.option[C.UnderlyingScrtClose]
        # self.option[C.Gains_to_underlying] = self.option[C.Gains] / self.option[C.Vega]
        # 计算gains/期权价格
        self.option[C.Gains_to_option] = self.option[C.Gains] / self.option[C.ClosePrice]

        self.option.to_csv(path_save,encoding='utf_8_sig',index=False)

        self.option[self.option[C.CallOrPut]=='C'][C.Gains_to_underlying].describe()#输出描述性统计
        self.option[self.option[C.CallOrPut] == 'P'][C.Gains_to_underlying].describe()


    #对delta中性收益进行描述性统计分析
    def gains_delta_neutral_summary(self):
        
        self.option=self.option[((self.option[C.KF]>=0.97)&(self.option[C.KF]<=1.1)&(self.option[C.CallOrPut]=='C'))|\
                              ((self.option[C.KF]>=0.90)&(self.option[C.KF]<=1.03)&(self.option[C.CallOrPut]=='P'))]


        #剔除极端值
        self.option=self.option[(self.option[C.Gains_to_underlying]>=self.option[C.Gains_to_underlying].quantile(0.01))&\
                                (self.option[C.Gains_to_underlying]<=self.option[C.Gains_to_underlying].quantile(0.99))]


        # 按照在值程度对样本分类
        self.option[C.KF_minus_1] = self.option[C.KF] - 1
        self.option[C.KF_minus_1_bin] = self.option[C.CallOrPut] + (
            pd.cut(self.option[C.KF_minus_1], bins=MONEYNESS_BIN)).astype(str)

        col_panel_Gains = self.option[C.KF_minus_1_bin].unique()

        #按照剩余到期时间对样本分类
        self.option[C.Maturity_bin]=  (
            pd.cut(self.option[C.RemainingTerm], bins=MATURITY_BIN)).astype(str)

        summary=pd.pivot_table(self.option[[C.KF_minus_1_bin,C.Maturity_bin,C.Gains_to_underlying]].dropna(),index=[C.KF_minus_1_bin],columns=[C.Maturity_bin],\
                       values=[C.Gains_to_underlying],aggfunc=[np.mean,np.std]
                       )

        #为了展示简洁，数字全部乘以10000处理
        summary*=10000
        summary.round(3).to_csv(PATH_GAINS_DELTA_NEUTRAL_SUMMARY,encoding='utf_8_sig')





























# 计算期权delta中性收益,使用上证50ETF期货价格
# 参考陈蓉（2019），波动率风险和波动率风险溢酬：中国的独特现象
class DeltaNeutralGains2():

    def __init__(self, path_option
                 ):
        self.option = pd.read_csv(path_option)
        self.option.drop_duplicates(inplace=True)

        self.def_col()  # 定义列标题
        self.filter()  # 筛选样本

        self.trade_dates = self.option[self.col_TradingDate].unique().tolist()  # 交易日期
        self.expiration = np.sort(self.option[self.col_ExerciseDate].unique().tolist())  # 到期日期
        self.tao = 1 / DAYS_OF_YEAR

    # 按照陈蓉(2011)的方法筛选样本
    def filter(self):
        # 剔除交易日高于60天的期权样本
        self.option = self.option[self.option[self.col_RemainingTerm] <= 30 / 365]
        # #剔除实值期权
        # self.option=self.option[self.option[self.col_Delta].abs()<=0.5]

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

    def run(self, path_save):
        #读取期货数据
        future=pd.read_csv(PATH_50ETF_FUTURE)
        future=future[future['Trdvar']=='上证50股指期货']
        future.columns

        future.rename(columns={'Trddt':C.TradingDate,'Deldt':C.FutureExpiration,'Clsprc':C.FutureClose},inplace=True)
        #期货距离到期日天数
        future['FutureDays']=(pd.to_datetime(future[C.FutureExpiration])-pd.to_datetime(future[C.TradingDate])).astype(str).str[:-4].astype(int)
        #期货距离到期日年数
        future[C.FutureRemainingTerm]=future['FutureDays']/365
        #计算次日期货价格
        future[C.FutureClose]/=1000
        future_ = future[[C.TradingDate, C.FutureClose]].drop_duplicates().sort_values(
            C.TradingDate)
        future['next_FutureClose'] = future_[C.FutureClose].shift(-1)
        #期货到期月份
        future[C.ExpirationMonth]=future[C.FutureExpiration].str[:7]
        self.option[C.ExpirationMonth]=self.option[C.ExerciseDate].str[:7]



        self.option=pd.merge(self.option,future[[C.TradingDate,C.FutureClose,C.FutureExpiration,C.FutureRemainingTerm,C.ExpirationMonth,'next_FutureClose']],on=[C.TradingDate,C.ExpirationMonth])

        self.option[C.FutureDelta]=self.option[C.Delta]*np.exp(-self.option[C.FutureRemainingTerm]*self.option[C.RisklessRate]/100)












        # 计算次日股票价格

        self.option['gains'] = self.option['next_Close'] - self.option[self.col_ClosePrice] - self.option[
            C.FutureDelta] * \
                               (self.option['next_FutureClose'] - self.option[C.FutureClose]) - \
                               self.option[self.col_RisklessRate] / 100 * \
                               (self.option[self.col_ClosePrice] - self.option[C.FutureDelta] * self.option[
                                   C.FutureClose]) * self.tao

        # 计算gains/S
        self.option[C.Gains_to_underlying] = self.option[C.Gains] / self.option[C.UnderlyingScrtClose]
        # 计算gains/期权价格
        self.option[C.Gains_to_option] = self.option[C.Gains] / self.option[C.ClosePrice]

        # C_gains=self.option[self.option[C.CallOrPut]=='C']
        # C_gains=C_gains[C_gains[C.TradingDate]<='2016-12-31']
        # C_gains[C.Gains_to_underlying].describe()
        # pd.pivot_table(C_gains,index=[C.TradingDate],values=[C.Gains_to_underlying]).describe()




        self.option.to_csv(path_save, encoding='utf_8_sig', index=False)


if __name__=='__main__':
    # DNG = DeltaNeutralGains2(path_option=PATH_50ETF_OPTION)
    # DNG.run(path_save=PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)

    DNG=DeltaNeutralGains(path_option=PATH_50ETF_OPTION)
    DNG.run(path_save=PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)




















