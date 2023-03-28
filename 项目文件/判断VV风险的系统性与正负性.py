import copy

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import statsmodels.api as sm



#
def COV_between_QVV_and_M():
    option=pd.read_csv(PATH_50ETF_OPTION)
    under=option[['TradingDate','UnderlyingScrtClose']].drop_duplicates().sort_values('TradingDate')
    under['r_Underlying']=np.log(under['UnderlyingScrtClose']/under['UnderlyingScrtClose'].shift())


    Q_VV=pd.read_csv(PATH_Q_VV)
    P_VV = pd.read_csv(PATH_P_VV).rename()
    P_VV_2=pd.read_csv(PATH_P_VV_2).rename(columns={'trade_date':'TradingDate'})

    P_VV_2['r_RV']=np.log(P_VV_2['RV']/P_VV_2['RV'].shift())
    P_VV_2['r_PVV'] = np.log(P_VV_2['PVV'] / P_VV_2['PVV'].shift())

    IV=pd.read_csv(PATH_IV_SURFACE_SERIES)


    under=pd.merge(under,P_VV_2,on=['TradingDate'])
    np.corrcoef(under[['r_Underlying','r_RV','r_PVV']].dropna().T)










    pass



if __name__=='__main__':
    COV_between_QVV_and_M()

















