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

        self.premium_ind_VV=self.premium_ind_VV[self.premium_ind_VV[C.Volga]>=0.05]
        # 剔除实值期权
        #参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
        self.gains=self.gains[((self.gains[C.KF]>=0.97)&(self.gains[C.KF]<=1.1)&(self.gains[C.CallOrPut]=='C'))|\
                              ((self.gains[C.KF]>=0.90)&(self.gains[C.KF]<=1.03)&(self.gains[C.CallOrPut]=='P'))]


        self.premium_ind_VV = self.premium_ind_VV[(self.premium_ind_VV[C.PREMIUM_Indep_VV] > self.premium_ind_VV[C.PREMIUM_Indep_VV].quantile(0.05)) \
                                                  & (self.premium_ind_VV[C.PREMIUM_Indep_VV] < self.premium_ind_VV[C.PREMIUM_Indep_VV].quantile(0.95))]
        self.premium_ind_VV_pivot =pd.pivot_table(self.premium_ind_VV,index=[C.TradingDate],values=[C.PREMIUM_Indep_VV])
        self.premium_ind_VV_pivot.to_csv(PATH_INDEPENDENT_VV_PREMIUM_SERIES,encoding='utf_8_sig')

        ARIMA(self.premium_ind_VV_pivot, order=(1, 0, 1)).fit()  # 拟合模型





        dates=list(self.gains_pivot.index)
        self.gains_pivot[C.Gains_lag1] = self.gains_pivot[C.Gains_to_underlying].shift().fillna(method='bfill')
        results=[]
        for date in dates[1173:]:
            try:
                date_train_last_index=dates.index(date)#训练集最后一个样本所在日期的编号
                date_test_first = dates[date_train_last_index+1]  # 测试集第一个样本所在日期

                for col_X in [['QVV', 'IV']]:
                    for day in WINDOWS_DAYS_NATURAL:
                        col_X_=[f'{x}{day}' for x in col_X]+[C.Gains_lag1]
                        X=self.gains_pivot.loc[dates[0]:dates[date_train_last_index],col_X_]

                        Y=self.gains_pivot.loc[dates[0]:dates[date_train_last_index],C.Gains_to_underlying]

                        model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                        X_next=sm.add_constant(self.gains_pivot.loc[date_test_first:, col_X_])
                        #X_next=sm.add_constant(pd.DataFrame(self.gains_pivot.loc[date_test_first,col_X_]).T.insert(loc=0,column='const',value=1))
                        results.append([date,day,model.predict(X_next).values[0]])
                        print([date,day,model.predict(X_next).values[0]])

            except:
                continue
        results



        results.to_csv(PATH_GAINS_OLS_IV_and_QVV, encoding='utf_8_sig', index=False)

        return results


#利用期权构造Vega中性组合
class VegaNeutralGains():

    def __init__(self,
                 ):
        self.option=pd.read_csv(PATH_50ETF_OPTION)
        self.option
        
        # 剔除实值期权
        #参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
        self.option=self.option[((self.option[C.KF]>=0.97)&(self.option[C.KF]<=1.1)&(self.option[C.CallOrPut]=='C'))|\
                              ((self.option[C.KF]>=0.90)&(self.option[C.KF]<=1.03)&(self.option[C.CallOrPut]=='P'))]

        self.option=self.option[(self.option[C.RemainingTerm]>=7/365)&(self.option[C.RemainingTerm]<=1)]

        # 添加期货价格数据
        self.add_future()


    ##添加期货价格数据
    def add_future(self):
        # 读取期货数据
        future = pd.read_csv(PATH_50ETF_FUTURE)
        future = future[future['Trdvar'] == '上证50股指期货']

        future.rename(columns={'Trddt': C.TradingDate, 'Deldt': C.FutureExpiration, 'Clsprc': C.FutureClose},
                      inplace=True)
        # 期货距离到期日天数
        future[C.FutureDays] = (pd.to_datetime(future[C.FutureExpiration]) - pd.to_datetime(
            future[C.TradingDate])).astype(str).str[:-24].astype(int)
        # 期货距离到期日年数
        future[C.FutureRemainingTerm] = future[C.FutureDays] / 365
        # 计算次日期货价格
        future[C.FutureClose] /= 1000
        future_ = future[[C.TradingDate, C.FutureClose]].drop_duplicates().sort_values(
            C.TradingDate)
        future[C.next_FutureClose] = future_[C.FutureClose].shift(-1)
        # 期货到期月份
        future[C.ExpirationMonth] = future[C.FutureExpiration].str[:7]
        self.option[C.ExpirationMonth] = self.option[C.ExerciseDate].str[:7]
        self.option = pd.merge(self.option, future[
            [C.TradingDate, C.FutureClose, C.FutureExpiration, C.FutureRemainingTerm, C.ExpirationMonth,
             C.next_FutureClose]], on=[C.TradingDate, C.ExpirationMonth])
        # 计算期货Delta
        self.option[C.FutureDelta] = self.option[C.Delta] * np.exp(
            -self.option[C.FutureRemainingTerm] * self.option[C.RisklessRate] / 100)



    #计算每个期权Vega与Gamma中性组合的多头收益
    def gains_Vega_Gamma_neutral_1(self, AT, option_type, i):
        option_proflio = AT.append(option_type.loc[i, :])

        # 为使Gamma和Vega保持中性，求解二元一次方程组，获得两只平值期权权重
        A = AT.loc[:, [C.Gamma, C.Vega]].values
        b = -option_type.loc[i, [C.Gamma, C.Vega]].values

        A = np.array([[A[0, 0], A[1, 0]], [A[0, 1], A[1, 1]]])  # A代表系数矩阵
        b = np.array([b[0], b[1]])  # b代表常数列
        x = linalg.solve(A, b)

        # 添加权重
        option_proflio[C.weight] = x.tolist() + [1]

        # 计算目标期权与对冲工具所构成的资产组合的总delta，并用期货对冲
        delta_total = x[0] * AT[C.FutureDelta].values[0] + x[1] * AT[C.FutureDelta].values[1] + 1 * option_type.loc[
            i, C.FutureDelta]

        # 计算持有一天后的收益
        gains_future = (option_proflio.loc[i, C.next_FutureClose] - option_proflio.loc[i, C.FutureClose]) * (delta_total)
        gains_option = sum((option_proflio[C.next_Close] - option_proflio[C.ClosePrice]) * option_proflio[C.weight])
        gains_risk_less = sum(
            option_proflio[C.ClosePrice] * option_proflio[C.RisklessRate] / 100 * tao * option_proflio[C.weight])

        # 计算期权组合多头的总收益
        gains_total = gains_option - gains_future - gains_risk_less

        return [gains_total,gains_option,gains_future,gains_risk_less],\
            [C.gains_VN_total,C.gains_VN_option,C.gains_VN_future,C.gains_VN_risk_less]

    #计算Vega中性收益时间序列
    def run_1(self):


        #用于分类的标签
        self.option['date&maturity']=self.option[C.TradingDate]+'&'+self.option[C.ExerciseDate]
        #用于判断平值期权的KF绝对值差
        self.option['KF_diff']=(self.option[C.KF]-1).abs()

        self.option=self.option.loc[self.option[C.CallOrPut]=='P',:]


        self.option.sort_values(['date&maturity','KF_diff'],ascending=True,axis=0,inplace=True)

        gains_all=[]#所有的期权收益
        for type in self.option['date&maturity'].unique():

            option_type=self.option[self.option['date&maturity']==type]
            option_type.reset_index(inplace=True)
            #做Vega和Gmama中性，至少需要三只期权
            if len(option_type)>=3:
                #逐个对每个期权进行中性构造:为了计算方便，我们先构造组合多头，并计算其收益。组合空头收益只需要在多头收益添加负号即可
                for i in range(len(option_type)):
                    try:
                        ShortName=option_type.loc[i,C.ShortName]

                        #在对最初两只最接近平值的期权对冲时，使用1，2，3中的两外两只期权作为对冲工具
                        if i==0:
                            AT=option_type.loc[[1,2],:]
                            vlaues,cols=self.gains_Vega_Gamma_neutral_1(AT, option_type, i)
                        elif i==1:
                            AT = option_type.loc[[0,2], :]
                            vlaues,cols=self.gains_Vega_Gamma_neutral_1(AT, option_type, i)
                        else:
                            AT = option_type.loc[[0, 1], :]
                            vlaues,cols=self.gains_Vega_Gamma_neutral_1(AT, option_type, i)
                        gains_all.append(type.split('&')+[ShortName]+vlaues)
                        print(f'计算Vega和Gamma中性收益已经完成{type}')
                    except:
                        continue

        GAINS_Vega_Neutral=pd.DataFrame(gains_all,columns=[C.TradingDate,C.ExerciseDate,C.ShortName]+cols)
        GAINS_Vega_Neutral.to_csv(PATH_GAINS_VEGA_NEUTRAL,encoding='utf_8_sig',index=False)
        # gains_all_[C.gains_VN_total].describe()


    #对1中的Vega中性收益结果进行分析
    def summary_1(self):

        option=pd.read_csv(PATH_50ETF_OPTION)
        GAINS_Vega_Neutral=pd.read_csv(PATH_GAINS_VEGA_NEUTRAL)
        VV=pd.read_csv(PATH_Q_VV)
        VV.columns=[C.TradingDate]+COL_QVV
        premium_independent=pd.read_csv(PATH_INDEPENDENT_VV_PREMIUM)


        GAINS_Vega_Neutral=pd.merge(GAINS_Vega_Neutral,option,on=[C.TradingDate,C.ShortName])
        GAINS_Vega_Neutral = pd.merge(GAINS_Vega_Neutral,VV,on=[C.TradingDate])
        GAINS_Vega_Neutral = pd.merge(GAINS_Vega_Neutral, premium_independent[[C.TradingDate, C.ShortName, C.Volga, C.PREMIUM_Indep_VV]], on=[C.TradingDate, C.ShortName])
        GAINS_Vega_Neutral=GAINS_Vega_Neutral[(GAINS_Vega_Neutral[C.gains_VN_total]>=GAINS_Vega_Neutral[C.gains_VN_total].quantile(0.005))&\
                                              (GAINS_Vega_Neutral[C.gains_VN_total]<=GAINS_Vega_Neutral[C.gains_VN_total].quantile(0.995))]
        # GAINS_Vega_Neutral = GAINS_Vega_Neutral[(GAINS_Vega_Neutral[C.RemainingTerm] >= 10/365)&(GAINS_Vega_Neutral[C.RemainingTerm] <= 60/365)]
        # GAINS_Vega_Neutral=GAINS_Vega_Neutral[((GAINS_Vega_Neutral[C.KF]>=0.97)&(GAINS_Vega_Neutral[C.KF]<=1.1)&(GAINS_Vega_Neutral[C.CallOrPut]=='C'))|\
        #                       ((GAINS_Vega_Neutral[C.KF]>=0.90)&(GAINS_Vega_Neutral[C.KF]<=1.03)&(GAINS_Vega_Neutral[C.CallOrPut]=='P'))]
        # GAINS_Vega_Neutral.drop_duplicates([C.TradingDate,C.ShortName],inplace=True)

        GAINS_Vega_Neutral[C.gains_VN_total]/GAINS_Vega_Neutral[C.next_FutureClose].describe()

        GAINS_Vega_Neutral.loc[GAINS_Vega_Neutral['QVV30']>=GAINS_Vega_Neutral['QVV30'].quantile(0.5)][C.gains_VN_total].describe()



        # GAINS_Vega_Neutral.loc[GAINS_Vega_Neutral[C.TradingDate]<='2018-12-31',:][C.gains_VN_total].describe()
        GAINS_Vega_Neutral[C.gains_VN_total].describe()

        pd.pivot_table(GAINS_Vega_Neutral,index=[C.TradingDate],columns=[C.CallOrPut],values=['gains_total']).describe()
        pd.pivot_table(GAINS_Vega_Neutral, index=[C.TradingDate], columns=[C.KF_minus_1_bin],
                       values=['gains_total']).describe()



        #检验独立VV风险溢价与Vega中性收益之间的关系
        GAINS_Vega_Neutral=GAINS_Vega_Neutral[GAINS_Vega_Neutral[C.Volga]>=0.05]
        GAINS_Vega_Neutral[[C.PREMIUM_Indep_VV, 'gains_total']].corr()







        #按照看涨看跌分类
        pd.pivot_table(GAINS_Vega_Neutral,index=[C.TradingDate,C.ShortName],columns=[C.CallOrPut],values=['gains_total'])

        pd.merge(GAINS_Vega_Neutral,VV)

        GAINS_Vega_Neutral





























if __name__=='__main__':
    # VNG=VegaNeutralGains()
    # VNG.run_1()
    # VNG.summary_1()

    #交易策略：构造一个组合：选择一只目标期权进行做多操作，并使用另外两只期权保证Gamma和Vega中性，最后根据总delta补充相应得期货，以保证组合得delta中性
    #将整个投资组合卖空，便可以获得正的VV风险收益
    TS=TradeStrategys()
    TS.run_1()







































