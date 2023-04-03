# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 功能文件.辅助功能.画图函数 import surface_3D
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility

from 项目文件.拟合delta中性收益与风险的时间序列关系 import SeriesOlsGainsAndRisk

if __name__=='__main__':
    # 普通OLS回归:用 gains/S = IV + QVV + gains/S(-1) 在时间序列上回归
    # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    SOGAR = SeriesOlsGainsAndRisk()

    # 剔除实值期权
    SOGAR.gains = SOGAR.gains[SOGAR.gains[C.Delta].abs() <= 0.5]

    SOGAR.gains_pivot = pd.pivot_table(SOGAR.gains, index=[SOGAR.col_TradingDate],
                                      values=[SOGAR.col_Gains, C.Gains_to_underlying,
                                              C.Gains_to_option] + COL_IV + COL_QVV)

    SOGAR.gains_pivot =SOGAR.gains_pivot.loc[:,[COL_IV[0],COL_QVV[0],C.Gains_to_underlying]]


    np.random.seed(19680801)

    n = 100_000
    x = SOGAR.gains_pivot[COL_QVV[0]]
    y =SOGAR.gains_pivot[C.Gains_to_underlying]
    xlim = x.min(), x.max()
    ylim = y.min(), y.max()

    fig, (ax0, ax1) = plt.subplots(ncols=2, sharey=True, figsize=(9, 4))

    hb = ax0.hexbin(x, y, gridsize=50, cmap='inferno')
    ax0.set(xlim=xlim, ylim=ylim)
    ax0.set_title("Hexagon binning")
    cb = fig.colorbar(hb, ax=ax0, label='counts')

    hb = ax1.hexbin(x, y, gridsize=50, bins='log', cmap='inferno')
    ax1.set(xlim=xlim, ylim=ylim)
    ax1.set_title("With a log color scale")
    cb = fig.colorbar(hb, ax=ax1, label='log10(N)')

    plt.show()

    
    SOGAR.run_1()





