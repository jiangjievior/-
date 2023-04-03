from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os








if __name__=='__main__':
    gains=pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    gains=pd.pivot_table(gains,index=[C.TradingDate],values=[C.Gains_to_underlying])[C.Gains_to_underlying]

    regression_results=pd.read_csv(PATH_GAINS_OLS_IV_and_QVV)
    regression_results=regression_results.loc[(regression_results['type_gain'] == C.Gains_to_underlying)]


    IV=pd.read_csv(PATH_IV_SURFACE_SERIES)
    At_IV=IV[IV[C.KF]==1]
    At_IV=pd.pivot_table(At_IV,index=[C.TradingDate],columns=['years'],values=['IV'])['IV']
    At_IV.columns=WINDOWS_DAYS_NATURAL

    for days in WINDOWS_DAYS_NATURAL:
        coef=regression_results.loc[regression_results['type_QVV']==f'QVV{days}','IV'].values[0]
        gains-=coef*At_IV[days]
        gains.describe()















    Q_VV = pd.read_csv(PATH_Q_VV,index_col=0)
    Q_VV.columns = COL_QVV
    Q_VV = Q_VV ** 2

    regression_results

    for col_QVV in COL_QVV:
        Q_VV_=Q_VV[col_QVV]
        coef=regression_results.loc[(regression_results['type_gain']==C.Gains_to_underlying)&(regression_results['type_QVV']==col_QVV),'QVV'].values[0]
        gains-=coef*Q_VV_
        gains.describe()





























