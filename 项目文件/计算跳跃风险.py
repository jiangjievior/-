
import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 项目文件.数据清洗 import get_data
from 数据文件.基本参数 import *


#计算跳跃风险：虚值期权隐含波动率-平值期权隐含波动率
#参考 《Volatility-of-Volatility Risk》 p38
def Jump_Risk():
    IV=pd.read_csv(PATH_IV_SURFACE_SERIES)
    IV=pd.pivot_table(IV,index=[C.TradingDate],columns=[C.KF],values=['IV'])['IV']
    IV=IV[IV.columns[(IV.columns>=0.95)&(IV.columns<=1.05)]]

    Jump=pd.DataFrame(IV.values-IV[IV.columns[2]].values.reshape(-1,1),index=IV.index,columns=IV.columns)
    #深度虚值看跌跳跃、虚值看跌跳跃、平值看跌跳跃、实值看涨跳跃、深度实值看涨跳跃
    Jump.columns=COL_JUMP

    Jump.to_csv(PATH_JUMP)




if __name__=='__main__':
    Jump_Risk()

















































