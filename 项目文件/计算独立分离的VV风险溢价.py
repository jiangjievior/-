# 学习时间 2023/4/7 21:43
# -*- coding:utf-8 -*-
from 功能文件.模型拟合.对一列数据进行描述性统计分析 import describe
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
from scipy import stats
# Statstic: 代表显著性水平
# P: 代表概率论与数理统计中的P值

# # 对随机样本进行检验
# jarque_bera_test = stats.jarque_bera(y_unknow)
# print("JB Test Statstic:{}   Pvalue:{}".format(jarque_bera_test.statistic,jarque_bera_test.pvalue))



if __name__=='__main__':
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    gains['d1']=(np.log(gains[C.UnderlyingScrtClose]/gains[C.StrikePrice])+(gains[C.RisklessRate]/100+gains[C.ImpliedVolatility]**2/2)\
                 *gains[C.RemainingTerm])/(gains[C.ImpliedVolatility]*np.sqrt(gains[C.RemainingTerm]))

    #添加RV
    RV=pd.read_csv(PATH_RV)
    gains=pd.merge(gains,RV,on=[C.TradingDate])

    gains['Volga']=gains[C.Vega]*gains['d1']*(gains['d1']-gains[C.ImpliedVolatility]*np.sqrt(gains[C.RemainingTerm]))/gains[C.ImpliedVolatility]


    #计算volga收益
    gains['gains_volga'] =(gains[C.Gains]-gains[C.Vega]*(1/365)*(gains[C.RV]**2-gains[C.ImpliedVolatility]**2))/(gains['Volga']*(1/365))

    #不同Volga取值范围下的


    gains_pool=pd.pivot_table(gains.loc[gains['Volga']>=0.12,:],index=[C.TradingDate],values=['gains_volga'])
    gains_pool=gains_pool[(gains_pool>gains_pool.quantile(0.01))&(gains_pool<gains_pool.quantile(0.99))]


    values,cols=describe(gains_pool.values.reshape(1,-1).tolist())
    mean, median, skew, kurt, std, min_, max_, percent_negative, percent_positive, AR1, t, p, star=values




    gains_pool.dropna().describe()
    gains_pool['Volga'].describe()
    gains_pool['Volga'].quantile(0.96)

    gains_moneyness=pd.pivot_table(gains.loc[gains['Volga']>=0.05,:],index=[C.TradingDate],columns=[C.KF_minus_1_bin],values=['gains_volga'])
    gains_moneyness = gains_moneyness[(gains_moneyness > gains_moneyness.quantile(0.2)) &\
                                      (gains_moneyness < gains_moneyness.quantile(0.8))]
    gains_summary=gains_moneyness.describe()

    gains[C.Gains].describe()



    















