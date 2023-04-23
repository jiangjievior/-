# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os





########################################################################################################################
#一、数据基本处理
#######################################################################################################################
# from 项目文件.数据清洗 import get_data, clean_data
#
#  #1.数据清洗
# data = get_data()
# data = clean_data(data,path_save=PATH_50ETF_OPTION)

########################################################################################################################
#二.计算隐含波动率 和 隐含波动率的波动率
# 参考陈蓉（2010）,按照  ln(IV)=b1+b2*K/S+b3*(K/S)^2+b4*years+b5*(years*K/S) 建立隐含波动率曲面
########################################################################################################################
# from 项目文件.拟合隐含波动率曲面 import construct_volatility_surface
# from 项目文件.绘图.绘制IV和QVV的三维坐标图 import plot_3D_surface
# from 项目文件.计算隐含vol_of_vol import implied_vol_of_vol, vol_of_vol_moneyness, vol_of_vol_summary

# #1.拟合隐含波动率曲面时间序列
# option = pd.read_csv(PATH_50ETF_OPTION)
# construct_volatility_surface(data=option,
#                              grids=[
#                                  MONEYNESS_KF,#在值程度
#                                  WINDOWS_YEARS_NATURAL#剩余到期时间
#                              ],
#                              path_save=PATH_IV_SURFACE_SERIES
#                              )

# #2.绘制隐含波动率的三维坐标图
# IV = pd.read_csv(PATH_IV_SURFACE_SERIES)
# IV = pd.pivot_table(IV, columns=[C.KF], index=['years'], values=['IV'])['IV']
# IV.index = WINDOWS_DAYS_NATURAL
# IV.sort_index(ascending=True, inplace=True)
# plot_3D_surface(data=IV,
#                 x_label='Maturity(days)',
#                 y_label=C.KF,
#                 z_label='IV',
#                 save_path=PATH_IV_SURFACE_3D)
#
#
# #3.计算隐含波动率的波动率
# implied_vol_of_vol(PATH_IV_SURFACE_SERIES,path_save=PATH_Q_VV)#计算基于平值期权计算的VV
# vol_of_vol_moneyness(path_save=PATH_Q_VV_Moneyness)#计算基于不同在值程度期权计算的VV
# vol_of_vol_summary()#隐含vol_of_vol的描述性统计分析
#
#
# #4.绘制隐含VV曲面3D图
# VV=pd.read_csv(PATH_Q_VV_Moneyness)
# VV=pd.pivot_table(VV,index=[C.KF],values=[str(x) for x in WINDOWS_DAYS_NATURAL[:-2]])[[str(x) for x in WINDOWS_DAYS_NATURAL[:-2]]]
# VV.columns=VV.columns.astype(int)
# plot_3D_surface(data = VV.T,
#                 x_label = 'Maturity(days)',
#                 y_label = C.KF,
#                 z_label = 'QVV',
#                 save_path = PATH_QVV_SURFACE_3D)
#
#
# pass
########################################################################################################################
#三.计算已实现波动率 和 已实现含波动率的波动率
########################################################################################################################
# from 项目文件.计算已实现波动率 import RV
# from 项目文件.计算已实现vol_of_vol import realized_vol_of_vol
#
# #1.计算已实现波动率
# RV(path_save=PATH_RV)

# #2.计算已实现含波动率的波动率(由于找不到合适的参考问献，已经废弃)
# realized_vol_of_vol(path_close_5_min=PATH_50ETF_5MIN,
#                     windows=WINDOWS_DAYS,
#                     path_save=PATH_P_VV,
#                     type=1
#                     )
########################################################################################################################
#三.五.计算偏度和峰度
########################################################################################################################
# from 项目文件.计算偏度和峰度 import P_SKEW, Q_SKEW_KURT
#
# P_SKEW()
#
# Q_SKEW_KURT()

########################################################################################################################
#四.判断风险的系统性与正负性
########################################################################################################################
# from 项目文件.判断风险的系统性与正负性 import COV_between_QVV_and_M
#
# #计算全样本的风险的系统性与正负性
# option = pd.read_csv(PATH_50ETF_OPTION)
# corr_s=COV_between_QVV_and_M(option=PATH_50ETF_OPTION,path_save=PATH_RISK_SYSMETRIC)
#
# corr_s




########################################################################################################################
#五.计算波动率的波动率风险溢价(由于找不到合适的参考问献计算PVV，已经废弃!!)
########################################################################################################################

# from 项目文件.计算波动率的波动率风险溢价 import Premium_VV
#
# Premium_VV(
#     path_Q_VV=PATH_Q_VV,
#     path_P_VV=PATH_P_VV,
#     type_P_VV=1
# )


########################################################################################################################
#六.计算期权delta中性收益
#######################################################################################################################
from 项目文件.计算delta中性收益 import DeltaNeutralGains, DeltaNeutralGains2

#(1和2只能使用一种，另一种必须注释掉。已经证实，2更加科学且可操作)

# #1.用上证50ETF指数计算delta中性收益，并对delta中性收益进行描述性统计分析
# DNG = DeltaNeutralGains(path_option=PATH_50ETF_OPTION)
# DNG.run(path_save=PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
# DNG.gains_delta_neutral_summary()

#2.用上证50ETF指数期货计算delta中性收益，并对delta中性收益进行描述性统计分析
##参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
DNG = DeltaNeutralGains2(path_option=PATH_50ETF_OPTION)
DNG.run(path_save=PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
DNG.gains_delta_neutral_summary()


########################################################################################################################
#七.用波动率和波动率的波动率预测期权delta中性收益
########################################################################################################################
# from 项目文件.修改数据结果格式 import reformat_run_1,reformat_run_2,reformat_run_3
# from 项目文件.拟合delta中性收益与风险的时间序列关系_新版 import SeriesOlsGainsAndRisk
#
# # 普通OLS回归:用 gains/S = IV^2 + QVV + gains/S(-1) 在时间序列上回归
# # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
# SOGAR = SeriesOlsGainsAndRisk()
# SOGAR.run_1()
# results_1=reformat_run_1()
#
# # 普通OLS回归:用 gains/S = RV + QVV + gains/S(-1) 在时间序列上回归
# # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
# SOGAR = SeriesOlsGainsAndRisk()
# SOGAR.run_2()
# results_2=reformat_run_2()
#
# # 普通OLS回归:用 gains/S = IV + QVV + gains/S(-1) 在时间序列上回归(已废弃!!)
# # gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
# SOGAR = SeriesOlsGainsAndRisk()
# SOGAR.run_3()
# results_3=reformat_run_3()
# pass
########################################################################################################################
#七.五.计算仅有VV风险的期权收益
########################################################################################################################
from 项目文件.计算剔除波动率风险的收益 import remove_RV_gains, remove_IV_gains,Summary_gains_except_Voltility
from 项目文件.绘图.绘制两种风险溢价的序列图 import plot_premium_independent_and_remove
from 项目文件.计算独立分离的VV风险溢价 import compute_independent_VV_premium, independent_VV_premium_different_volga, \
    plot_VV_and_vloga, independent_VV_premium_different_moneyness


#计算剔除波动率风险后的期权收益
remove_RV_gains()
remove_IV_gains()
Summary_gains_except_Voltility()#对计算好的数据进行描述性统计分析

#计算独立分离的VV风险溢价
gains = compute_independent_VV_premium()# 计算独立VV风险溢价
results = independent_VV_premium_different_volga(gains=gains)# 不同Volga取值范围下的volga中性收益描述性统计分析
plot_VV_and_vloga(results)# 绘制均值、标准差、偏度、极值 与Volga的图
results_moneyness = independent_VV_premium_different_moneyness(gains)# 绘制不同在值程度下的独立VV风险溢价描述性统计分析特征(使用Volga>0.05)

# 绘制两种VV风险溢价的时间序列，包括（独立VV风险溢价、剔除波动率风险项后的期权收益）
plot_premium_independent_and_remove()

########################################################################################################################
#八.计算跳跃风险，并拟合
########################################################################################################################
from 项目文件.计算跳跃风险 import Jump_Risk
Jump_Risk()

from 项目文件.修改数据结果格式 import reformat_run_4,reformat_run_7
from 项目文件.拟合delta中性收益与风险的时间序列关系_新版 import SeriesOlsGainsAndRisk



#普通OLS回归:用 gains/S = IV + QVV + gains/S(-1) 在时间序列上回归
#gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
SOGAR = SeriesOlsGainsAndRisk()
SOGAR.run_4()
results_4=reformat_run_4()


#普通OLS回归:用 gains/S = RV + QVV + gains/S(-1) 在时间序列上回归
#gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
SOGAR = SeriesOlsGainsAndRisk()
SOGAR.run_7()
results_7=reformat_run_7()



pass

########################################################################################################################
#九.样本分组，检查子样本组内的回归稳健性(已经验证不太行)
########################################################################################################################
# from 项目文件.修改数据结果格式 import reformat_run_1,reformat_run_2,reformat_run_3
# from 项目文件.拟合delta中性收益与风险的时间序列关系_新版 import SeriesOlsGainsAndRisk
# # 普通OLS回归:用 gains/S = IV^2 + QVV + gains/S(-1) 在时间序列上回归
# # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
# SOGAR = SeriesOlsGainsAndRisk()
# SOGAR.run_6()
# results_1=reformat_run_1()

########################################################################################################################
#十.考虑偏度和峰度风险
########################################################################################################################
from 项目文件.修改数据结果格式 import reformat_run_8,reformat_run_9
from 项目文件.拟合delta中性收益与风险的时间序列关系_新版 import SeriesOlsGainsAndRisk


# 普通OLS回归:用 gains/S = RV^2 + QVV^2+ Q_SKEW+Q_KURT + gains/S(-1) 在时间序列上回归
# gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
SOGAR=SeriesOlsGainsAndRisk()
SOGAR.run_8()
reformat_run_8()

# # 普通OLS回归:用 gains/S = IV^2 + QVV^2+ Q_SKEW+Q_KURT + gains/S(-1) 在时间序列上回归
# gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
SOGAR = SeriesOlsGainsAndRisk()
SOGAR.run_9()
reformat_run_9()


########################################################################################################################
#十一.样本外交易策略收益预测
########################################################################################################################







########################################################################################################################
#终.论文中最终展示表格
########################################################################################################################




















pass






















