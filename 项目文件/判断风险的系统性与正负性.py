import copy

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import statsmodels.api as sm



#检验两个时间序列之间的相关性
#参考陈蓉(2019)和冯志新(2013)，检验V和VV收益率与市场收益率的相关性
def COV_between_QVV_and_M(
        option,path_save=False
):
    under=option[['TradingDate','UnderlyingScrtClose']].drop_duplicates().sort_values('TradingDate')
    under['r_Underlying']=np.log(under['UnderlyingScrtClose']/under['UnderlyingScrtClose'].shift())

    RV=pd.read_csv(PATH_RV)

    Q_VV=pd.read_csv(PATH_Q_VV)
    P_VV = pd.read_csv(PATH_P_VV)

    #将P_VV和Q_VV合并到under中
    Q_VV.columns=['TradingDate']+[f'Q_VV{x}' for x in WINDOWS_DAYS_NATURAL]
    P_VV.columns=['TradingDate','P_VV']
    under=pd.merge(under,Q_VV,on=['TradingDate'])
    under = pd.merge(under, P_VV, on=['TradingDate'])
    under = pd.merge(under, RV, on=['TradingDate'])
    under=under[under['r_Underlying']<=under['r_Underlying'].quantile(0.5)]


    corr_s=[]
    col_s=[f'Q_VV{x}' for x in WINDOWS_DAYS_NATURAL]+['P_VV','RV']
    for col_VV in col_s:
        under[col_VV]=np.log(under[col_VV]/under[col_VV].shift())
        under.dropna(inplace=True)
        S2xy_1=under[[col_VV,'r_Underlying']]-under[[col_VV,'r_Underlying']].mean()

        S2xy=sum(S2xy_1[col_VV] * S2xy_1['r_Underlying'])
        r =S2xy/np.sqrt(sum(S2xy_1[col_VV]**2) * sum(S2xy_1['r_Underlying']**2))

        t=r/np.sqrt(1-r**2)*np.sqrt(len(S2xy_1)-2)

        corr_s.append([col_VV,r,t])

    corr_s=pd.DataFrame(corr_s,columns=['risk','corr','t'])
    if path_save:
        corr_s.to_csv(PATH_RISK_SYSMETRIC,encoding='utf_8_sig',index=False)

    return corr_s
















if __name__=='__main__':
    #2015年2月9日——2016年7月8日
    option = pd.read_csv(PATH_50ETF_OPTION)
    option=option[(option[C.TradingDate]>='2015-02-09')&(option[C.TradingDate]<='2016-07-08')]
    corr_s = COV_between_QVV_and_M(option=option)


    #全范围样本
    option = pd.read_csv(PATH_50ETF_OPTION)
    corr_s=COV_between_QVV_and_M(option=option,path_save=PATH_RISK_SYSMETRIC)

    corr_s

















