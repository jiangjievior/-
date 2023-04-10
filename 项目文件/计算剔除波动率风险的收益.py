import copy

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.模型拟合.计算一列数据的t检验统计结果 import t_test
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
from statsmodels.tsa.arima.model import ARIMA

# 剔除已实现波动率的风险(剩余风险收益/总风险收益的绝对值)
def remove_RV_gains():
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    # 剔除实值期权
    # 参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
    gains = gains[
        ((gains[C.KF] >= 0.97) & (gains[C.KF] <= 1.1) & (gains[C.CallOrPut] == 'C')) | \
        ((gains[C.KF] >= 0.90) & (gains[C.KF] <= 1.03) & (gains[C.CallOrPut] == 'P'))]
    gains=pd.pivot_table(gains,index=[C.TradingDate],values=[C.Gains_to_underlying])


    regression_RV=pd.read_csv(PATH_GAINS_OLS_RV_and_QVV)
    regression_RV = regression_RV.loc[16:, :]

    RV=pd.read_csv(PATH_RV,index_col=0)

    gains_s=[]
    for days in WINDOWS_DAYS_NATURAL:
        coef=regression_RV.loc[regression_RV['Maturity']==days,'RV'].values[0]
        gains['RV']=RV['RV']

        gains_=gains[C.Gains_to_underlying]-coef*RV['RV']**2
        #2023-03-23   -0.000359
        gains_=-gains_/gains[C.Gains_to_underlying]
        #缩尾处理
        gains_=gains_[(gains_<=gains_.quantile(0.99))&(gains_>=gains_.quantile(0.01))]
        gains_s.append(gains_)

    gains_s=pd.concat(gains_s,keys=WINDOWS_DAYS_NATURAL,axis=1)
    gains_s.to_csv(PATH_REMOVE_RV_GAINS,encoding='utf_8_sig')
    # gains_s.describe().to_csv(PATH_REMOVE_RV_GAINS_SUMMRY,encoding='utf_8_sig')


#剔除隐含波动率的风险(剩余风险收益/总风险收益的绝对值)
def  remove_IV_gains():
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    # 剔除实值期权
    # 参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
    gains = gains[
        ((gains[C.KF] >= 0.97) & (gains[C.KF] <= 1.1) & (gains[C.CallOrPut] == 'C')) | \
        ((gains[C.KF] >= 0.90) & (gains[C.KF] <= 1.03) & (gains[C.CallOrPut] == 'P'))]

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
    # gains_s.describe().to_csv(PATH_REMOVE_IV_GAINS_SUMMRY,encoding='utf_8_sig')


def Summary_gains_except_Voltility():
    gains_IV=pd.read_csv(PATH_REMOVE_IV_GAINS,index_col=0)
    gains_RV = pd.read_csv(PATH_REMOVE_RV_GAINS,index_col=0)
    gains={'IV':gains_IV,'RV':gains_RV}

    results=[]
    for key in gains.keys():
        gains_key=gains[key].dropna()
        for i in WINDOWS_INDEX:

            days=str(WINDOWS_DAYS_NATURAL[i])
            gains_key_days = gains_key[days]
            mean=round(gains_key_days.mean(),3)
            median=round(gains_key_days.median(),3)
            skew=round(gains_key_days.skew(),3)
            kurt = round(gains_key_days.kurt(), 3)
            std = round(gains_key_days.std(), 3)
            #小于零的数所占百分比
            percent=f'{round(sum(gains_key_days<0)/len(gains_key_days)*100,2)}%'
            #计算AR(1)系数
            model = ARIMA(gains_key_days, order=(1, 0, 0)).fit()
            AR1 = model.params['ar.L1']  # 系数

            t, p, star=t_test(gains_key[str(WINDOWS_DAYS_NATURAL[i])])
            results.append([key,days,f'{mean}{star}',median,skew,kurt,percent,std,AR1,len(gains_key_days)])

    results=pd.DataFrame(results,columns=['type_V','Maturity(天)','mean','median','skew','kurt','%<0','std','AR(1)','Num'])
    results.to_csv(PATH_REMOVE_GAINS_SUMMRY,encoding='utf_8_sig')










if __name__=='__main__':

    remove_RV_gains()

    remove_IV_gains()

    Summary_gains_except_Voltility()













