import pandas as pd
from 数据文件.基本参数 import *
import numpy as np
from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
import matplotlib.pyplot as plt



# -*- coding:utf-8 -*-
# 异步进程池（非阻塞）
from multiprocessing import Pool

def test(i):
    print(i)

if __name__ == "__main__":
    pool = Pool(2)
    for i in range(100):
        '''
        For循环中执行步骤：
        （1）循环遍历，将100个子进程添加到进程池（相对父进程会阻塞）
        （2）每次执行8个子进程，等一个子进程执行完后，立马启动新的子进程。（相对父进程不阻塞）
        apply_async为异步进程池写法。异步指的是启动子进程的过程，与父进程本身的执行（print）是异步的，而For循环中往进程池添加子进程的过程，与父进程本身的执行却是同步的。
        '''
        pool.apply_async(test, args=(i,))  # 维持执行的进程总数为8，当一个进程执行完后启动一个新进程.
    print("test")
    pool.close()
    pool.join()

    k=2

















#观察



    #观察独立VV风险溢价
    PRE=pd.read_csv(PATH_INDEPENDENT_VV_PREMIUM)

    PRE=PRE.loc[PRE[C.Volga]>=0.1,:]
    PRE

    plt.figure(figsize=(10,8))
    plt.scatter(PRE[C.FutureDelta],PRE[C.PREMIUM_Indep_VV])
    plt.scatter(PRE[C.KF_minus_1],PRE[C.PREMIUM_Indep_VV])

    PRE_OUT=PRE[PRE[C.FutureDelta].abs()<=0.1]
    PRE_OUT[C.PREMIUM_Indep_VV].describe()







    gains=pd.read_csv(data_real_path('数据文件/生成数据')+'/陈蓉2011delta中性收益率.csv')
    P_V=pd.read_csv('数据文件/生成数据/已实现vol_of_vol.csv')
    P_V.rename(columns={'date':'TradingDate'},inplace=True)

    Q_V=pd.read_csv('数据文件/生成数据/隐含vol_of_vol.csv')
    Q_V.rename(columns={'Unnamed: 0':'TradingDate'},inplace=True)
    col_X=Q_V.columns

    gains=pd.merge(gains,Q_V,on=['TradingDate'])
    gains=pd.merge(gains,P_V,on=['TradingDate'])

    gains=pd.pivot_table(gains,index=['TradingDate'],values=['ImpliedVolatility',col_X[2],'gains','UnderlyingScrtClose'])

    #X=gains['vol_of_vol']
    X = gains[['ImpliedVolatility',col_X[2]]]  # 解释变量
    Y = gains['gains']/gains['UnderlyingScrtClose']# 被解释变量




    model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)
    model, params, tvalues, pvalues, resid, F, p_F, R_2


    Q_V



