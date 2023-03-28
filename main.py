# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

from 项目文件.数据清洗 import get_data, clean_data


########################################################################################################################
#一、数据基本处理
########################################################################################################################

#1.数据清洗
data = get_data()
data = clean_data(data,path_save=PATH_50ETF_OPTION)


########################################################################################################################
#二.拟合隐含波动率曲面时间序列
# 参考陈蓉（2010）,按照  ln(IV)=b1+b2*K/S+b3*(K/S)^2+b4*years+b5*(years*K/S) 建立隐含波动率曲面
########################################################################################################################
from 项目文件.拟合隐含波动率曲面 import construct_volatility_surface

option = pd.read_csv(PATH_50ETF_OPTION)
construct_volatility_surface(data=option,
                             grids=[
                                 [0.8, 0.9, 1, 1.1, 1.2],#在值程度
                                 WINDOWS_YEARS#剩余到期时间
                             ],
                             path_save=PATH_IV_SURFACE_SERIES
                             )

########################################################################################################################
#三.计算波动率的波动率风险溢价
########################################################################################################################
from 项目文件.计算隐含vol_of_vol import implied_vol_of_vol
from 项目文件.计算已实现vol_of_vol import realized_vol_of_vol
from 项目文件.计算波动率的波动率风险溢价 import Premium_VV

#1.计算隐含波动率的波动率
implied_vol_of_vol(PATH_IV_SURFACE_SERIES,path_save=PATH_Q_VV)


#2.计算已实现含波动率的波动率
realized_vol_of_vol(path_close_5_min=PATH_50ETF_5MIN,
                    windows=WINDOWS_DAYS,
                    path_save=PATH_P_VV,
                    type=1
                    )


#3.计算波动率的波动率风险溢价
Premium_VV(
    path_Q_VV=PATH_Q_VV,
    path_P_VV=PATH_P_VV,
    type_P_VV=1
)






































