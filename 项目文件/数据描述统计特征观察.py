

# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os




















if __name__=='__main__':
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    gains

    pd.pivot_table(gains,index=[C.CallOrPut],values=[C.Gains])








