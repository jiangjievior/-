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

# #1.数据清洗
# data = get_data(path_option_price=data_real_path('数据文件/原始数据/期权收盘价/SO_PricingParameter.csv'),
#                 path_option_volume=data_real_path('数据文件/原始数据/期权交易量数据/SO_QuotationBas.csv')
#                 )
# data = clean_data(data,path_save=data_real_path('数据文件/生成数据')+'/上证50ETF期权数据.csv')


########################################################################################################################
#二.拟合隐含波动率曲面时间序列
# 参考陈蓉（2010）,按照  ln(IV)=b1+b2*K/S+b3*(K/S)^2+b4*years+b5*(years*K/S) 建立隐含波动率曲面
########################################################################################################################
# from 项目文件.拟合隐含波动率曲面 import construct_volatility_surface
#
# option = pd.read_csv(data_real_path('数据文件/生成数据/上证50ETF期权数据.csv'))
# construct_volatility_surface(data=option,
#                              grids=[
#                                  [0.8, 0.9, 1, 1.1, 1.2],#在值程度
#                                  [1 / 12, 2 / 12, 3 / 12, 6 / 12, 1]#剩余到期时间
#                              ],
#                              path_save=data_real_path('数据文件/生成数据') + '/隐含波动率曲面时间序列.csv'
#                              )

########################################################################################################################
#三.计算波动率的波动率风险溢价
########################################################################################################################
from 项目文件.计算隐含vol_of_vol import implied_vol_of_vol
from 项目文件.计算已实现vol_of_vol import realized_vol_of_vol
from 项目文件.计算波动率的波动率风险溢价 import Premium_VV

# #1.计算隐含波动率的波动率
# path_surface_series = data_real_path('数据文件/生成数据/隐含波动率曲面时间序列.csv')
# path_save = data_real_path('数据文件/生成数据') + '/隐含vol_of_vol.csv'
# implied_vol_of_vol(path_surface_series,path_save=path_save)
#
#
# #2.计算已实现含波动率的波动率
# realized_vol_of_vol(path_close_5_min=data_real_path('数据文件/原始数据/ETF50五分钟收盘价.csv'),
#                     windows=[1 / 12, 2 / 12, 3 / 12, 6 / 12, 1],
#                     path_save=data_real_path('数据文件/生成数据') + '/已实现vol_of_vol.csv',
#                     type=1
#                     )


#3.计算波动率的波动率风险溢价
Premium_VV(
    path_Q_VV=data_real_path('数据文件/生成数据') + '/隐含vol_of_vol.csv',
    path_P_VV=data_real_path('数据文件/生成数据') + '/已实现vol_of_vol.csv',
    type_P_VV=1
)






































