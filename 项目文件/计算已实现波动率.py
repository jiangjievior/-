import numpy as np
import pandas as pd
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *





def RV(path_save=False):
    data = pd.read_csv(PATH_50ETF_5MIN)
    data = data[data['trade_time'] >= '2015-02-01 00:00:00'].reset_index()

    data['r'] = np.log(data['close'] / data['close'].shift())
    data[C.TradingDate] = data['trade_time'].astype(str).str[:10]

    # 已实现波动率
    RV_s = []
    for date in data[C.TradingDate].unique():
        data_date = data[data[C.TradingDate] == date].dropna()
        RV_s.append([date, np.sqrt(sum(data_date['r'] ** 2))*10])
    RV_s = pd.DataFrame(RV_s, columns=[C.TradingDate, 'RV'])

    if path_save:
        RV_s.to_csv(path_save,encoding='utf_8_sig',index=False)

if __name__=='__main__':
    RV(path_save=PATH_RV)









