
from statsmodels.tsa.arima_model import ARIMA

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.模型拟合.计算一列数据的t检验统计结果 import t_test
# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from scipy import linalg

from 项目文件.计算样本外预测收益 import VegaNeutralGains


class TradeStrategys():

    def __init__(self,
                 bins_moneyness=5,#按照moneyness将数据划分为指定个小组
                 ):
        self.bins_moneyness=bins_moneyness

        #读取数据
        self.gains= pd.read_csv(PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
        self.IV=pd.read_csv(PATH_IV_SURFACE_SERIES)
        self.RV=pd.read_csv(PATH_RV)
        self.Q_VV=pd.read_csv(PATH_Q_VV)
        self.Q_SKEW_KURT=pd.read_csv(PATH_Q_SKEW_KURT)
        self.combine_data()

        #读取独立VV风险溢价
        self.premium_ind_VV=pd.read_csv(PATH_INDEPENDENT_VV_PREMIUM)

        # 剔除实值期权
        #参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
        self.gains=self.gains[((self.gains[C.KF]>=0.97)&(self.gains[C.KF]<=1.1)&(self.gains[C.CallOrPut]=='C'))|\
                              ((self.gains[C.KF]>=0.90)&(self.gains[C.KF]<=1.03)&(self.gains[C.CallOrPut]=='P'))]

        #建立日度均值时间序列
        self.gains_pivot = pd.pivot_table(self.gains, index=[C.TradingDate],
                                          values=[C.Gains, C.Gains_to_underlying,
                                                  C.Gains_to_option,C.RV] + COL_IV + COL_QVV+[C.Q_SKEW,C.Q_KURT])
        self.gains_pivot.dropna(inplace=True)

    #将收益与波动率数据合并
    def combine_data(self):
        #添加已实现波动率数据
        self.RV[C.RV]=self.RV[C.RV]**2
        self.gains = pd.merge(self.gains, self.RV, on=[C.TradingDate])

        #添加QVV数据
        self.Q_VV.columns = [C.TradingDate] + COL_QVV
        self.Q_VV[COL_QVV]=self.Q_VV[COL_QVV]**2
        self.gains = pd.merge(self.gains, self.Q_VV, on=[C.TradingDate])

        #将平值期权IV添加进数据
        self.At_IV=pd.pivot_table(self.IV[self.IV[C.KF]==1],index=[C.TradingDate],columns=['years'],values=['IV'])['IV']
        self.At_IV.columns=COL_IV
        self.At_IV[COL_IV]=self.At_IV[COL_IV]**2
        self.At_IV.reset_index(inplace=True)
        self.gains=pd.merge(self.gains,self.At_IV,on=[C.TradingDate])

        self.gains = pd.merge(self.gains, self.Q_SKEW_KURT, on=[C.TradingDate])

        # 普通OLS回归:用 gains/S = IV^2 + QVV^2 + gains/S(-1) 在时间序列上回归
        # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    def run_1(self):

        #独立VV风险溢价数据
        self.premium_ind_VV=self.premium_ind_VV[self.premium_ind_VV[C.Volga]>=0.05]
        # 剔除实值期权
        #参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
        self.gains=self.gains[((self.gains[C.KF]>=0.97)&(self.gains[C.KF]<=1.1)&(self.gains[C.CallOrPut]=='C'))|\
                              ((self.gains[C.KF]>=0.90)&(self.gains[C.KF]<=1.03)&(self.gains[C.CallOrPut]=='P'))]


        self.premium_ind_VV = self.premium_ind_VV[(self.premium_ind_VV[C.PREMIUM_Indep_VV] > self.premium_ind_VV[C.PREMIUM_Indep_VV].quantile(0.1)) \
                                                  & (self.premium_ind_VV[C.PREMIUM_Indep_VV] < self.premium_ind_VV[C.PREMIUM_Indep_VV].quantile(0.9))]
        #计算独立VV风险溢价时间序列
        self.premium_ind_VV_pivot =pd.pivot_table(self.premium_ind_VV,index=[C.TradingDate],values=[C.PREMIUM_Indep_VV])
        self.premium_ind_VV_pivot.to_csv(PATH_INDEPENDENT_VV_PREMIUM_SERIES,encoding='utf_8_sig')
        self.premium_ind_VV_pivot.index = list(map(lambda x:pd.datetime.strptime(x, '%Y-%m-%d'),self.premium_ind_VV_pivot.index))  # 将时间列改为专门时间格式，方便后期操作
        dates = self.premium_ind_VV_pivot.index
        self.premium_ind_VV_pivot.index=range(len(self.premium_ind_VV_pivot.index))


        #采用滑动窗口方式预测次日独立VV风险溢价
        results=[]
        windows=800
        for i in range(windows-1,len(dates)):
            try:
                dates[i]
                model=ARIMA(self.premium_ind_VV_pivot[0:i], order=(1, 0, 1)).fit()  # 拟合模型
                pred=model.predict(i-1,i+1,dynamic=True)
                results.append([i,pred.loc[i+1]])
                print(dates[i])
            except:
                continue
        results=pd.DataFrame(results,columns=['id',C.PREMIUM_Indep_VV_pred])

        #将计算结果还原为日期格式
        results[C.TradingDate]=results['id'].apply(lambda x:dates[x])#添加日期
        self.premium_ind_VV_pivot[C.TradingDate]=dates
        results=pd.merge(results,self.premium_ind_VV_pivot,on=[C.TradingDate])
        #确认可以交易的样本
        results['long']=(results[C.PREMIUM_Indep_VV_pred]>results[C.PREMIUM_Indep_VV])
        results.to_csv(PATH_SHOULD_TRADE,encoding='utf_8_sig',index=False)


        #读取Vega中性收益数据
        Gains_Vega_Neutral=pd.read_csv(PATH_GAINS_VEGA_NEUTRAL)
        results[C.TradingDate]=results[C.TradingDate].astype(str)
        #将Vega收益数据与期权数据相结合
        self.premium_ind_VV
        self.premium_ind_VV=pd.merge(self.premium_ind_VV,Gains_Vega_Neutral,on=[C.ShortName,C.TradingDate,C.ExerciseDate])
        #确认可交易数据
        data =pd.merge(self.premium_ind_VV,results[[C.TradingDate,'long']],how='right')
        data=data.loc[data['long'] == True, :].dropna()
        data=data[(data[C.gains_VN_total]>=data[C.gains_VN_total].quantile(0.01))&(data[C.gains_VN_total]<=data[C.gains_VN_total].quantile(0.99))]
        pd.pivot_table(data,columns=C.KF_minus_1_bin,values=[C.gains_VN_total])
        #计算平值期权的收益获利统计
        gains_summary=[]
        for col in data[C.KF_minus_1_bin].unique():
            t_test(data.loc[data[C.KF_minus_1_bin]==col,C.gains_VN_total])










if __name__=='__main__':
    TS=TradeStrategys()
    TS.run_1()









    VNG.summary_1()



    gains_CALL=pd.read_csv(PATH_GAINS_VEGA_NEUTRAL_CALL)
    gains_CALL

















