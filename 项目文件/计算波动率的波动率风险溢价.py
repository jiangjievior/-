import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path




def Premium_VV(
        path_Q_VV='',
        path_P_VV='',
        type_P_VV=1,

):
    if type_P_VV==1:
        Q_VV=pd.read_csv(path_Q_VV,index_col=0)
        P_VV=pd.read_csv(path_P_VV,index_col=0)
        Q_VV['P_VV']=P_VV['vol_of_vol']

        Premium={}
        for col in Q_VV.columns[:-1]:
            Premium[col]=(Q_VV['P_VV']-Q_VV[col]).values
        Premium=pd.DataFrame(Premium)
        Premium.mean()





    pass













