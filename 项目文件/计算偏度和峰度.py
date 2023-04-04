# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

# 计算P偏度：参考2022，郑振龙，《方差风险、偏度风险与市场收益率的可预测性》
def P_SKEW():
    data = pd.read_csv(PATH_50ETF_5MIN)
    data['r'] = np.log(data['close'] / data['close'].shift())
    data[C.TradingDate] = data['trade_time'].astype(str).str[:10]
    P_SKEW_s = []
    for date in data[C.TradingDate].unique():
        data_date = data[data[C.TradingDate] == date].dropna()
        SKEW = sum(data_date['r'] ** 3) / (sum(data_date['r'] ** 2) ** (3 / 2)) * np.sqrt(len(data_date))
        P_SKEW_s.append([date, SKEW])
        print(f'计算P_SKEW已经完成{date}')

    P_SKEW_s = pd.DataFrame(P_SKEW_s, columns=[C.TradingDate, C.P_SKEW])
    P_SKEW_s.to_csv(PATH_P_SKEW, encoding='utf_8_sig', index=False)





if __name__=='__main__':
    #P_SKEW()

    #计算Q偏度和Q峰度
    #参考：2020,《上证50ETF隐含高阶矩风险对股票收益的预测研究》，王琳玉
    #参考：2013，《Does Risk-Neutral Skewness Predict the Cross Section of Equity Option Portfolio Returns?》
    data=pd.read_csv(PATH_50ETF_OPTION)
    data

    for date in data[C.TradingDate].unique():
        data_date=data[data[C.TradingDate]==date]

        data_C=data_date[data_date[C.CallOrPut]=='C']
        data_P=data_date[data_date[C.CallOrPut]=='P']

        #筛选虚值期权
        data_C=data_C[data_C[C.KF]>=1]
        data_P = data_P[data_P[C.KF] >= 1]


        V=sum((2*(1-np.log(data_C[C.StrikePrice]/data_C[C.UnderlyingScrtClose]))/data_C[C.StrikePrice]**2)*data_C[C.ClosePrice]*K_DIFF)+\
            sum((2*(1+np.log(data_P[C.UnderlyingScrtClose]/data_P[C.StrikePrice]))/data_P[C.StrikePrice]**2)*data_P[C.ClosePrice]*K_DIFF)

        W=sum(((6*np.log(data_C[C.StrikePrice]/data_C[C.UnderlyingScrtClose])-3*np.log(data_C[C.StrikePrice]/data_C[C.UnderlyingScrtClose])**2)/data_C[C.StrikePrice]**2)*data_C[C.ClosePrice]*K_DIFF)\
        -sum(((6*np.log(data_P[C.UnderlyingScrtClose]/data_P[C.StrikePrice])+3*np.log(data_P[C.UnderlyingScrtClose]/data_P[C.StrikePrice])**2)/data_P[C.StrikePrice]**2)*data_P[C.ClosePrice]*K_DIFF)

        X=sum(((12*np.log(data_C[C.StrikePrice]/data_C[C.UnderlyingScrtClose])**2-4*np.log(data_C[C.StrikePrice]/data_C[C.UnderlyingScrtClose])**3)/data_C[C.StrikePrice]**2)*data_C[C.ClosePrice]*K_DIFF)\
        +sum(((12*np.log(data_P[C.UnderlyingScrtClose]/data_P[C.StrikePrice])+4*np.log(data_P[C.UnderlyingScrtClose]/data_P[C.StrikePrice])**3)/data_P[C.StrikePrice]**2)*data_P[C.ClosePrice]*K_DIFF)

        EXP=np.exp(data[C.RisklessRate]/100*data[C.RemainingTerm])
        miu=np.exp(data[C.RisklessRate]/100*data[C.RemainingTerm])









































































