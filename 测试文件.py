import pandas as pd
from 数据文件.基本参数 import *
import numpy as np
from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
import matplotlib.pyplot as plt


#观察



#观察独立VV风险溢价
PRE=pd.read_csv(PATH_INDEPENDENT_VV_PREMIUM)

PRE=PRE.loc[PRE[C.Volga]>=0.1,:]
PRE

plt.figure(figsize=(10,8))
plt.scatter(PRE[C.FutureDelta],PRE[C.PREMIUM_Indep_VV])
plt.scatter(PRE[C.KF_minus_1],PRE[C.PREMIUM_Indep_VV])

PRE_OUT=PRE[PRE[C.FutureDelta].abs()<=0.1]
PRE_OUT[C.PREMIUM_Indep_VV].describe()







gains=pd.read_csv(data_real_path('数据文件/生成数据')+'/陈蓉2011delta中性收益率.csv')
P_V=pd.read_csv('数据文件/生成数据/已实现vol_of_vol.csv')
P_V.rename(columns={'date':'TradingDate'},inplace=True)

Q_V=pd.read_csv('数据文件/生成数据/隐含vol_of_vol.csv')
Q_V.rename(columns={'Unnamed: 0':'TradingDate'},inplace=True)
col_X=Q_V.columns

gains=pd.merge(gains,Q_V,on=['TradingDate'])
gains=pd.merge(gains,P_V,on=['TradingDate'])

gains=pd.pivot_table(gains,index=['TradingDate'],values=['ImpliedVolatility',col_X[2],'gains','UnderlyingScrtClose'])

#X=gains['vol_of_vol']
X = gains[['ImpliedVolatility',col_X[2]]]  # 解释变量
Y = gains['gains']/gains['UnderlyingScrtClose']# 被解释变量




model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)
model, params, tvalues, pvalues, resid, F, p_F, R_2


Q_V



