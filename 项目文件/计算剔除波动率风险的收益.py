import copy

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

# 剔除已实现波动率的风险(剩余风险收益/总风险收益的绝对值)
def remove_RV_gains():
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    gains = gains[gains[C.Delta].abs() <= 0.5]
    gains=pd.pivot_table(gains,index=[C.TradingDate],values=[C.Gains_to_underlying])


    regression_RV=pd.read_csv(PATH_GAINS_OLS_RV_and_QVV)
    regression_RV = regression_RV.loc[16:, :]

    RV=pd.read_csv(PATH_RV,index_col=0)

    gains_s=[]
    for days in WINDOWS_DAYS_NATURAL:
        coef=regression_RV.loc[regression_RV['Maturity']==days,'RV'].values[0]
        gains['RV']=RV['RV']

        gains_=gains[C.Gains_to_underlying]-coef*RV['RV']**2
        gains_=-gains_/gains[C.Gains_to_underlying]
        #缩尾处理
        gains_=gains_[(gains_<=gains_.quantile(0.99))&(gains_>=gains_.quantile(0.01))]
        gains_s.append(gains_)

    gains_s=pd.concat(gains_s,keys=WINDOWS_DAYS_NATURAL,axis=1)
    gains_s.to_csv(PATH_REMOVE_RV_GAINS,encoding='utf_8_sig')
    gains_s.describe().to_csv(PATH_REMOVE_RV_GAINS_SUMMRY,encoding='utf_8_sig')


#剔除隐含波动率的风险(剩余风险收益/总风险收益的绝对值)
def  remove_IV_gains():
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    gains = gains[gains[C.Delta].abs() <= 0.5]
    gains=pd.pivot_table(gains,index=[C.TradingDate],values=[C.Gains_to_underlying])

    regression_results=pd.read_csv(PATH_GAINS_OLS_IV_and_QVV)
    regression_results=regression_results.loc[(regression_results['type_gain'] == C.Gains_to_underlying)]
    regression_results =regression_results.loc[16:,:]

    IV=pd.read_csv(PATH_IV_SURFACE_SERIES)
    At_IV=IV[IV[C.KF]==1]
    At_IV=pd.pivot_table(At_IV,index=[C.TradingDate],columns=['years'],values=['IV'])['IV']
    At_IV.columns=WINDOWS_DAYS_NATURAL

    gains_s = []
    for days in WINDOWS_DAYS_NATURAL:
        coef=regression_results.loc[regression_results['Maturity']==days,'IV'].values[0]
        gains['premium_volatility']=coef*At_IV[days]**2
        gains_=gains[C.Gains_to_underlying]-gains['premium_volatility']
        gains_ = -gains_ / gains[C.Gains_to_underlying]
        # 缩尾处理
        gains_ = gains_[(gains_ <= gains_.quantile(0.99)) & (gains_ >= gains_.quantile(0.01))]
        gains_s.append(gains_)
    gains_s = pd.concat(gains_s, keys=WINDOWS_DAYS_NATURAL, axis=1)

    gains_s.to_csv(PATH_REMOVE_IV_GAINS,encoding='utf_8_sig')
    gains_s.describe().to_csv(PATH_REMOVE_IV_GAINS_SUMMRY,encoding='utf_8_sig')





if __name__=='__main__':

    remove_RV_gains()

    remove_IV_gains()












