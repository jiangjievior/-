import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import numpy as np
import pandas as pd
import pandas as pd
from 数据文件.基本参数 import *


#绘制两种VV风险溢价的时间序列，包括（独立VV风险溢价、剔除波动率风险项后的期权收益）
def plot_premium_independent_and_remove():
    #合并两种VV风险溢价数据（独立VV风险溢价、剔除波动率风险项后的期权收益）
    premium_independent=pd.read_csv(PATH_INDEPENDENT_VV_PREMIUM)
    premium_independent=premium_independent[premium_independent[C.Volga]>=0.05]#选择Volga大于0，05的期权样本
    premium_independent=premium_independent[(premium_independent['gains_volga']>=premium_independent['gains_volga'].quantile(0.05))\
                                            &(premium_independent['gains_volga']<=premium_independent['gains_volga'].quantile(0.95))]

    premium_independent=pd.pivot_table(premium_independent,index=[C.TradingDate],values=['gains_volga'])['gains_volga']

    gains_RV=pd.read_csv(PATH_REMOVE_RV_GAINS,index_col=0)
    gains_IV=pd.read_csv(PATH_REMOVE_IV_GAINS,index_col=0)
    #选择剩余时间为30天的VV
    premium_=pd.concat([premium_independent,gains_IV['30'],gains_RV['30']],axis=1)
    premium_.columns=['premium(VV)','premium(-IV)','premium(-RV)']

    #绘图
    fig, axs = plt.subplots(3, 1, figsize=(11, 7))
    for ax,col_y in zip(axs,premium_.columns):
        ax.plot(premium_.index, premium_[col_y],linewidth=0.4)
        #绘制零线，用于区分高于零和低于零的区域
        ax.plot(premium_.index,[0]*len(premium_),color='r')
        ax.fill_between(premium_.index, [0]*len(premium_), [min(premium_[col_y])]*len(premium_), facecolor='y',
                         alpha=0.1)  # 填充
        ax.text(premium_.index[int(len(premium_.index)/3*2)],min(premium_[col_y]),  f'percent<0 : {round(sum(premium_[col_y]<0)/len(premium_[col_y])*100,2)}%'
                )  # 在横轴为74的地方添加文字备注

        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.grid(True)
        ax.set_ylabel(fr'{col_y} ')
    plt.xticks(ticks=premium_.index[np.linspace(0,len(premium_)-1,num=10).astype(int)],rotation=320)
    plt.savefig(PATH_PREMIUM_INDEPENDENT_AND_REMOVE)



if __name__=='__main__':
    # 绘制两种VV风险溢价的时间序列，包括（独立VV风险溢价、剔除波动率风险项后的期权收益）
    plot_premium_independent_and_remove()

















