# 学习时间 2023/4/7 21:43
# -*- coding:utf-8 -*-
from 功能文件.模型拟合.对一列数据进行描述性统计分析 import describe
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
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

    gains[C.Volga]=gains[C.Vega]*gains['d1']*(gains['d1']-gains[C.ImpliedVolatility]*np.sqrt(gains[C.RemainingTerm]))/gains[C.ImpliedVolatility]


    #计算volga收益
    gains[C.gains_VV] =(gains[C.Gains]-gains[C.Vega]*(1/365)*(gains[C.RV]**2-gains[C.ImpliedVolatility]**2))/(gains['Volga']*(1/365))
    gains.to_csv(PATH_INDEPENDENT_VV_PREMIUM,encoding='utf_8_sig',index=False)


    #不同Volga取值范围下的volga中性收益描述性统计分析
    results=[]
    for volga in np.arange(1,41)/100:

        gains_Volga=gains.loc[gains[C.Volga]>=volga,:]
        gains_pool=pd.pivot_table(gains_Volga,index=[C.TradingDate],values=['gains_volga'])
        gains_pool=gains_pool[(gains_pool>gains_pool.quantile(0.01))&(gains_pool<gains_pool.quantile(0.99))]


        values,cols=describe(gains_pool.dropna().values.reshape(1,-1).tolist()[0])
        mean, median, skew, kurt, std, min_, max_, percent_negative, percent_positive, AR1,Number, t, p, star=values

        results.append([volga]+values+[len(gains_Volga)])

    results=pd.DataFrame(results,columns=[C.Volga]+cols+['NumSample'])
    results.to_csv(PATH_INDEPENDENT_VV_PREMIUM_SUMMARY,encoding='utf_8_sig',index=False)

    #绘制均值、标准差、偏度、极值 与Volga的图
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure(num=1, figsize=(12, 8))  # 创建一块总画布

    # 画块ax1
    ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=1,
                           colspan=1)  # 将画板分为四行四列共16个单元格，(0, 0)表示从第一行第一列即第一个单元格开始画图，将第一行的三个单元格作为一个画块作画
    x = results[C.Volga]
    y_1 = results['mean']
    ax1.plot(y_1, color='r')
    #ax1.legend(loc='upper right')  # 用于显示画布ax1的图，切记用 loc= 表示位置
    ax1.set_ylabel('mean', fontsize=15)
    plt.grid(True)
    # 在此处，ax1.set_ylabel('线性值')和plt.ylabel('线性值')具有同样的效果，但是plt.ylabel('线性值')必须紧随其后，紧跟在画块ax1后面执行。如果画完ax2再来此处运行plt.ylabel('线性值')，将对ax2产生效果

    # 画块ax2
    ax2 = plt.subplot2grid((2, 2), (0, 1), rowspan=1, colspan=1)
    x = results[C.Volga]
    y_2 = results['std']
    ax2.plot(y_2, color='b')
    # ax1.legend(loc='upper right')  # 用于显示画布ax1的图，切记用 loc= 表示位置
    ax2.set_ylabel('std', fontsize=15)
    plt.grid(True)

    # 画块ax3
    ax3 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, colspan=1)
    x = results[C.Volga]
    y_3 = results['skew']
    ax3.plot(y_3, color='y')
    # ax1.legend(loc='upper right')  # 用于显示画布ax1的图，切记用 loc= 表示位置
    ax3.set_ylabel('skew', fontsize=15)
    plt.grid(True)

    # 画块ax4
    ax4 = plt.subplot2grid((2, 2), (1, 1), rowspan=1, colspan=1)
    x = results[C.Volga]
    y_4_min = results['min']
    ax4.plot(y_4_min, color='g')
    y_4_max = results['max']
    ax4.plot(y_4_max, color='pink')
    # ax1.legend(loc='upper right')  # 用于显示画布ax1的图，切记用 loc= 表示位置
    ax4.set_ylabel('min&max', fontsize=15)
    plt.grid(True)

    plt.savefig(PATH_PLOT_GAINS_AND_VOLAG)


    #绘制不同在值程度下的独立VV风险溢价描述性统计分析特征(使用Volga>0.13)
    gains=gains[gains[C.Volga] >= 0.04]
    #gains_pivot=pd.pivot_table(gains[gains[C.Volga]>=0.04],index=[C.TradingDate],columns=[C.KF_minus_1_bin],values=[C.gains_VV])[C.gains_VV]
    results_moneyness=[]
    for col in gains[C.KF_minus_1_bin].unique():
        gains_moneyness=gains[gains[C.KF_minus_1_bin]==col].dropna()

        values, cols = describe(gains_moneyness[C.gains_VV].values.reshape(1, -1).tolist()[0])
        results_moneyness.append([col]+values+[len(gains)])
    # gains_pivot = pd.pivot_table(gains[gains[C.Volga] >= 0.04], index=[C.TradingDate], columns=[C.KF_minus_1_bin],
    #                                  values=[C.gains_VV])[C.gains_VV]
    results_moneyness=pd.DataFrame(results_moneyness,columns=['Moneyness']+cols+['NumSample'])
    results_moneyness.to_csv(PATH_INDEPENDENT_VV_PREMIUM_MONEYNESS_SUMMARY,encoding='utf_8_sig',index=False)

    















