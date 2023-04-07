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
    #option=pd.read_csv(PATH_50ETF_OPTION)
    under=option[['TradingDate','UnderlyingScrtClose']].drop_duplicates().sort_values('TradingDate')
    under['r_Underlying']=np.log(under['UnderlyingScrtClose']/under['UnderlyingScrtClose'].shift())

    RV=pd.read_csv(PATH_RV)

    Q_VV=pd.read_csv(PATH_Q_VV)
#    P_VV = pd.read_csv(PATH_P_VV)

    #将P_VV和Q_VV合并到under中
    Q_VV.columns=['TradingDate']+[f'Q_VV{x}' for x in WINDOWS_DAYS_NATURAL]
#    P_VV.columns=['TradingDate','P_VV']
    under=pd.merge(under,Q_VV,on=['TradingDate'])
#    under = pd.merge(under, P_VV, on=['TradingDate'])
    under = pd.merge(under, RV, on=['TradingDate'])
    #under=under[under['r_Underlying']<=under['r_Underlying'].quantile(0.5)]#筛选出小于0.5分位数的收益率 ？


    corr_s=[]
    col_s = [f'Q_VV{x}' for x in WINDOWS_DAYS_NATURAL] + ['RV']
#    col_s=[f'Q_VV{x}' for x in WINDOWS_DAYS_NATURAL]+['P_VV','RV']
    for col_VV in col_s:
        under[col_VV]=np.log(under[col_VV]/under[col_VV].shift())#Qvv的变化率
        under.dropna(inplace=True)
        S2xy_1=under[[col_VV,'r_Underlying']]-under[[col_VV,'r_Underlying']].mean()

        S2xy=sum(S2xy_1[col_VV] * S2xy_1['r_Underlying'])
        r =S2xy/np.sqrt(sum(S2xy_1[col_VV]**2) * sum(S2xy_1['r_Underlying']**2))#QVV和r相关系数计算

        t=r/np.sqrt(1-r**2)*np.sqrt(len(S2xy_1)-2)#QVV和r的t值计算

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






#验证陈蓉2015.2.9-2016.7.8的IV、RV与M的关系
def COV_between_IV_and_M(
        option,path_save=False
):
    option=pd.read_csv(PATH_50ETF_OPTION)
    under1=option[['TradingDate','UnderlyingScrtClose']].drop_duplicates().sort_values('TradingDate')
    under1['r_Underlying'] = np.log(under1['UnderlyingScrtClose'] / under1['UnderlyingScrtClose'].shift())
    RV=pd.read_csv(PATH_RV)
    # 加入RV
    under1=pd.merge(under1,RV,on=['TradingDate'])

    #构造每一交易日不同到期时间的IV
    IV1 = pd.read_csv(PATH_IV_SURFACE_SERIES)
    IV1 =IV1[['TradingDate','years','IV']]
    IV1 = pd.pivot_table(IV1, columns = ['years'], index = ['TradingDate'], values = ['IV'])['IV']
    IV1.reset_index(inplace = True)
    IV1.columns = ['TradingDate'] + [f'IV{x}' for x in WINDOWS_DAYS_NATURAL]

    under1 = pd.merge(under1,IV1, on = ['TradingDate'])
    under1 = under1[under1['r_Underlying'] <= under1['r_Underlying'].quantile(0.5)]
    # 筛选出小于0.5分位数的收益率
    corr_s1=[]
    col_s1= [f'IV{x}' for x in WINDOWS_DAYS_NATURAL] + ['RV']#所有日度到期时间的IV+RV
    for col_V in col_s1:
        under1[col_V]=np.log(under1[col_V]/under1[col_V].shift())#IV的变化率
        under1.dropna(inplace=True)
        S2xy_2=under1[[col_V,'r_Underlying']]-under1[[col_V,'r_Underlying']].mean()

        S2xy1=sum(S2xy_2[col_V] * S2xy_2['r_Underlying'])#IV和r协方差计算
        r1 =S2xy1/np.sqrt(sum(S2xy_2[col_V]**2) * sum(S2xy_2['r_Underlying']**2))#IV和r相关系数计算

        t1=r1/np.sqrt(1-r1**2)*np.sqrt(len(S2xy_2)-2)#QVV和r的t值计算

        corr_s1.append([col_V,r1,t1])

    corr_s1=pd.DataFrame(corr_s1,columns=['risk','corr','t'])
    if path_save:
        corr_s.to_csv(PATH_RISK_SYSMETRIC,encoding='utf_8_sig',index=False)

    return corr_s1

if __name__ == '__main__':
    # 全范围样本
    option = pd.read_csv(PATH_50ETF_OPTION)
    option = option[(option[C.TradingDate] >= '2015-02-09') & (option[C.TradingDate] <= '2016-07-08')]
    corr_s1 = COV_between_IV_and_M(option = option)

    corr_s1



















