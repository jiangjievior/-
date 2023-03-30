# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

from 项目文件.拟合delta中性收益与风险的时间序列关系 import SeriesOlsGainsAndRisk
from 项目文件.数据清洗 import get_data, clean_data


########################################################################################################################
#一、数据基本处理
########################################################################################################################

# #1.数据清洗
# data = get_data()
# data = clean_data(data,path_save=PATH_50ETF_OPTION)


########################################################################################################################
#二.计算隐含波动率 和 隐含波动率的波动率
# 参考陈蓉（2010）,按照  ln(IV)=b1+b2*K/S+b3*(K/S)^2+b4*years+b5*(years*K/S) 建立隐含波动率曲面
########################################################################################################################
# from 项目文件.拟合隐含波动率曲面 import construct_volatility_surface
# from 项目文件.计算隐含vol_of_vol import implied_vol_of_vol
#
# #1.拟合隐含波动率曲面时间序列
# option = pd.read_csv(PATH_50ETF_OPTION)
# construct_volatility_surface(data=option,
#                              grids=[
#                                  MONEYNESS_KF,#在值程度
#                                  WINDOWS_YEARS_NATURAL#剩余到期时间
#                              ],
#                              path_save=PATH_IV_SURFACE_SERIES
#                              )
#
# #2.计算隐含波动率的波动率
# implied_vol_of_vol(PATH_IV_SURFACE_SERIES,path_save=PATH_Q_VV)

# #3.绘制隐含vol_of_vol和隐含波动率的三维坐标图



########################################################################################################################
#三.计算已实现波动率 和 已实现含波动率的波动率
########################################################################################################################
# from 项目文件.计算已实现波动率 import RV
# from 项目文件.计算已实现vol_of_vol import realized_vol_of_vol
#
# #1.计算已实现波动率
# RV(path_save=PATH_RV)

# #2.计算已实现含波动率的波动率
# realized_vol_of_vol(path_close_5_min=PATH_50ETF_5MIN,
#                     windows=WINDOWS_DAYS,
#                     path_save=PATH_P_VV,
#                     type=1
#                     )

########################################################################################################################
#四.计算波动率的波动率风险溢价
########################################################################################################################

# from 项目文件.计算波动率的波动率风险溢价 import Premium_VV
#
# Premium_VV(
#     path_Q_VV=PATH_Q_VV,
#     path_P_VV=PATH_P_VV,
#     type_P_VV=1
# )


########################################################################################################################
#五.计算期权delta中性收益
#######################################################################################################################
# from 项目文件.计算delta中性收益 import DeltaNeutralGains
#
# DNG = DeltaNeutralGains(path_option=PATH_50ETF_OPTION)
# DNG.run(path_save=PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)


########################################################################################################################
#六.用波动率和波动率的波动率预测期权delta中性收益
########################################################################################################################

# 普通OLS回归:用 gains/S = IV + QVV + gains/S(-1) 在时间序列上回归
# gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
SOGAR = SeriesOlsGainsAndRisk()
SOGAR.run_1()

# 普通OLS回归:用 gains/S = RV + QVV + gains/S(-1) 在时间序列上回归
# gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
SOGAR = SeriesOlsGainsAndRisk()
SOGAR.run_2()

# 普通OLS回归:用 gains/S = IV + QVV + gains/S(-1) 在时间序列上回归
# gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
SOGAR = SeriesOlsGainsAndRisk()
SOGAR.run_3()


########################################################################################################################
#七.计算跳跃风险，并拟合
########################################################################################################################
from 项目文件.计算跳跃风险 import Jump_Risk
Jump_Risk()


#普通OLS回归:用 gains/S = IV + QVV + gains/S(-1) 在时间序列上回归
#gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
SOGAR = SeriesOlsGainsAndRisk()
SOGAR.run_4()

pass































