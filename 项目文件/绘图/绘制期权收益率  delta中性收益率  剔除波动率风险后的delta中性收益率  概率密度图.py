# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
plt.rcParams['font.sans-serif']=['simhei']#用于正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用于正常显示负号



#绘制概率密度图
def plot_dentisty():
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    gains
    gains = gains[gains[C.Delta].abs() <= 0.5]

    #期权收益：原始收益、delta中性收益、剔除波动率风险后的delta中性收益、剔除所有风险后的delta中性收益
    col_gains=['Change1',C.Gains,'gains_RV','gains_IV']
    gains=pd.pivot_table(gains,index=[C.TradingDate],values=['Change1',C.Gains,C.Gains_to_underlying,C.UnderlyingScrtClose])
    gains = gains[(gains <= gains.quantile(0.99)) & (gains >= gains.quantile(0.01))]

    gains_RV=pd.read_csv(PATH_REMOVE_RV_GAINS,index_col=0)
    gains_IV = pd.read_csv(PATH_REMOVE_IV_GAINS,index_col=0)

    #将  期权收益 还原
    gains['gains_RV']=gains_RV['30']*gains[C.Gains_to_underlying].abs()*gains[C.UnderlyingScrtClose]
    gains['gains_IV'] =gains_IV['30']*gains[C.Gains_to_underlying].abs()*gains[C.UnderlyingScrtClose]

    gains[col_gains]*=1000
    gains=gains[gains[col_gains]>-10]
    gains = gains[gains[col_gains]<10]

    gains[col_gains].plot(kind='kde')

    gains[col_gains].kurt()
    gains[col_gains].skew()
    gains[col_gains].mean()




















if __name__=='__main__':
    plot_dentisty()


















