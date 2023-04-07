# 学习时间 2023/4/7 21:43
# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os



if __name__=='__main__':
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    gains['d1']=(np.log(gains[C.UnderlyingScrtClose]/gains[C.StrikePrice])+(gains[C.RisklessRate]/100+gains[C.ImpliedVolatility]**2/2)\
                 *(1/365))/(gains[C.ImpliedVolatility]*np.sqrt((1/365)))


    gains['Volga']=gains['d1']*np.sqrt((1/365)/(2*np.pi))*gains[C.UnderlyingScrtClose]*\
                   np.exp(-gains['d1']**2/2)*(gains['d1']/gains[C.ImpliedVolatility]-np.sqrt((1/365)))





    
    #计算volga收益
    gains['gains_volga']=(gains[C.Gains]/gains['Volga']-gains[C.Vega]*(gains['next_ImpliedVolatility']**2-gains[C.ImpliedVolatility]**2)/gains['Volga'])/(1/365)
    gains_pool=pd.pivot_table(gains.loc[gains['Volga']>=0.01,:],index=[C.TradingDate],values=['gains_volga'])
    gains_pool=gains_pool[(gains_pool>gains_pool.quantile(0.05))&(gains_pool<gains_pool.quantile(0.95))]
    gains_pool.dropna().describe()
    gains['Volga'].describe()

    gains_pool.isna().sum()
    
    
    
    
    gains















