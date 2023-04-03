# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 功能文件.辅助功能.画图函数 import surface_3D
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import numpy as np
import pandas as pd
import time
plt.rcParams['font.sans-serif']=['simhei']#用于正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用于正常显示负号
from matplotlib import cm#必须从matplotlib中引入cm模块！！
from mpl_toolkits.mplot3d import axes3d
from matplotlib.ticker import LinearLocator,FormatStrFormatter#用于修改坐标轴刻度和数值精确程度


#绘制三维曲面图
def plot_3D_surface(
    data = None,
    x_label = 'Maturity(years)',
    y_label = C.KF,
    z_label = 'IV',
    save_path = None,
    show = True
    ):


    x = data.index
    y = data.columns
    x, y = np.meshgrid(x, y)
    x = x.T
    y = y.T
    z = np.array(data)

    fig = plt.figure(figsize=(12, 16))  # 创建图形
    ax = fig.gca(projection='3d')  # 设置3D坐标轴
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.4,
                           label='曲面图')  # cmap=cm.coolwarm为图形表面设置皮肤,help(cm)可以查看更多中类型皮肤
    fig.colorbar(surf, shrink=0.6, aspect=8)  # # shrink控制标签长度，aspect仅对bar的宽度有影响，aspect值越大，bar越窄

    # 设置坐标轴名称
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    ax.set_zlabel(z_label, fontsize=15)
    ax.view_init(azim=20)  # 调整坐标轴的刚打开图片时的初始显示角度，仰角和方位角。可以用于保存图片

    # plt.title(title, fontsize=25)
    # plt.show()

    if save_path is not None:
        plt.savefig(save_path)









if __name__=='__main__':
    #绘制隐含波动率曲面3D图
    IV=pd.read_csv(PATH_IV_SURFACE_SERIES)
    IV=pd.pivot_table(IV,columns=[C.KF],index=['years'],values=['IV'])['IV']
    IV.index=WINDOWS_DAYS_NATURAL
    IV.sort_index(ascending=True,inplace=True)
    plot_3D_surface(data = IV,
                    x_label = 'Maturity(days)',
                    y_label = C.KF,
                    z_label = 'IV',
                    save_path = PATH_IV_SURFACE_3D)

    #绘制隐含VV曲面3D图
    VV=pd.read_csv(PATH_Q_VV_Moneyness)
    VV=pd.pivot_table(VV,index=[C.KF],values=[str(x) for x in WINDOWS_DAYS_NATURAL])[[str(x) for x in WINDOWS_DAYS_NATURAL]]
    VV.columns=VV.columns.astype(int)
    plot_3D_surface(data = VV.T,
                    x_label = 'Maturity(days)',
                    y_label = C.KF,
                    z_label = 'QVV',
                    save_path = PATH_QVV_SURFACE_3D)


























