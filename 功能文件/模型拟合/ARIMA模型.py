from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
plt.rcParams['font.sans-serif']=['simhei']#用于正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用于正常显示负号
from 数据文件.基本参数 import *

data=pd.read_csv(PATH_INDEPENDENT_VV_PREMIUM_SERIES,index_col=0)

sm.tsa.adfuller(data,regression='c')
sm.tsa.adfuller(data,regression='nc')
sm.tsa.adfuller(data,regression='ct')


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(data.values.squeeze(), lags=12, ax=ax1)#自相关系数图1阶截尾,决定MA（1）
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(data, lags=12, ax=ax2)#偏相关系数图1阶截尾,决定AR（1）

model = ARIMA(data, order=(1, 0, 1)).fit()#拟合模型
model.summary()#统计信息汇总

#系数检验
params=model.params#系数
tvalues=model.tvalues#系数t值
bse=model.bse#系数标准误
pvalues=model.pvalues#系数p值


#计算模型拟合值
fit=model.predict(exog=data[['TLHYL']])





















