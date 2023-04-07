# -*- coding:utf-8 -*-
#import commctrl

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os


#使用面板数据拟合delta中性收益与 波动率^2 VV^2 之间的关系
#参考《Volatility-of-Volatility Risk Darien》的(28)
class SeriesOlsGainsAndRisk():

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

        self.def_col()
        self.combine_data()

        # 剔除实值期权
        #参考：陈蓉2019，《波动率风险和波动率风险溢酬 中国的独特现象?》，p3005
        self.gains=self.gains[((self.gains[C.KF]>=0.97)&(self.gains[C.KF]<=1.1)&(self.gains[C.CallOrPut]=='C'))|\
                              ((self.gains[C.KF]>=0.90)&(self.gains[C.KF]<=1.03)&(self.gains[C.CallOrPut]=='P'))]

        #建立日度均值时间序列
        self.gains_pivot = pd.pivot_table(self.gains, index=[self.col_TradingDate],
                                          values=[self.col_Gains, C.Gains_to_underlying,
                                                  C.Gains_to_option,C.RV] + COL_IV + COL_QVV+[C.Q_SKEW,C.Q_KURT])
        self.gains_pivot.dropna(inplace=True)

    #将收益与波动率数据合并
    def combine_data(self):
        #添加已实现波动率数据
        self.RV[C.RV]=self.RV[C.RV]**2
        self.gains = pd.merge(self.gains, self.RV, on=[self.col_TradingDate])

        #添加QVV数据
        self.Q_VV.columns = [self.col_TradingDate] + COL_QVV
        self.Q_VV[COL_QVV]=self.Q_VV[COL_QVV]**2
        self.gains = pd.merge(self.gains, self.Q_VV, on=[self.col_TradingDate])

        #将平值期权IV添加进数据
        self.At_IV=pd.pivot_table(self.IV[self.IV[C.KF]==1],index=[C.TradingDate],columns=['years'],values=['IV'])['IV']
        self.At_IV.columns=COL_IV
        self.At_IV[COL_IV]=self.At_IV[COL_IV]**2
        self.At_IV.reset_index(inplace=True)
        self.gains=pd.merge(self.gains,self.At_IV,on=[C.TradingDate])

        #添加Q_SKEW和Q_KURT数据
        self.Q_SKEW_KURT
        self.gains=pd.merge(self.gains,self.Q_SKEW_KURT[[C.TradingDate,C.Q_SKEW,C.Q_KURT]],on=[C.TradingDate])
        self.gains[C.Q_KURT]/=100




    #普通OLS回归:用 gains/S = IV^2 + QVV^2 + gains/S(-1) 在时间序列上回归
    #gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    def run_1(self):

        #self.gains_pivot=self.gains_pivot.loc[self.gains_pivot.index>='2019-01-01',:]

        results=[]

        for col_X in (['QVV'],['IV'],['QVV','IV']):
            result=[]

            for days in WINDOWS_DAYS_NATURAL:
                X = self.gains_pivot[[f'{x}{days}' for x in col_X]]
                X[C.Gains_lag1] = self.gains_pivot[C.Gains_to_underlying].shift().fillna(method='bfill')
                Y = self.gains_pivot[C.Gains_to_underlying]
                # X[C.Gains_lag1] = self.gains_pivot[C.Gains].shift().fillna(method='bfill')
                # Y = self.gains_pivot[C.Gains]

                model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                result.append([C.Gains_to_underlying]+[days] + params + tvalues + pvalues + [R_2])
            col_X=['const']+col_X+[C.Gains_lag1]
            result=pd.DataFrame(result,columns=['type_gain','Maturity']+col_X+[f't{x}' for x in col_X]+[f'p{x}' for x in col_X]+['R'])
            results.append(result)
        results=pd.concat(results,axis=0)

        results.to_csv(PATH_GAINS_OLS_IV_and_QVV,encoding='utf_8_sig',index=False)

        return results

    #普通OLS回归:用 gains/S = RV^2 + QVV^2 + gains/S(-1) 在时间序列上回归
    #gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    def run_2(self):

        #self.gains_pivot=self.gains_pivot.loc[self.gains_pivot.index<='2019-02-02',:]

        results=[]

        for col_X in (['QVV'],['RV'],['QVV','RV']):
            result=[]

            for days in WINDOWS_DAYS_NATURAL:
                col_X_=[f'{x}{days}' if x=='QVV' else x for x in col_X]
                X = self.gains_pivot[col_X_]
                X[C.Gains_lag1] = self.gains_pivot[C.Gains_to_underlying].shift().fillna(method='bfill')
                Y = self.gains_pivot[C.Gains_to_underlying]
                # X[C.Gains_lag1] = self.gains_pivot[C.Gains].shift().fillna(method='bfill')
                # Y = self.gains_pivot[C.Gains]

                model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                result.append([C.Gains_to_underlying]+[days] + params + tvalues + pvalues + [R_2])
            col_X=['const']+col_X+[C.Gains_lag1]
            result=pd.DataFrame(result,columns=['type_gain','Maturity']+col_X+[f't{x}' for x in col_X]+[f'p{x}' for x in col_X]+['R'])
            results.append(result)
        results=pd.concat(results,axis=0)

        results.to_csv(PATH_GAINS_OLS_RV_and_QVV,encoding='utf_8_sig',index=False)

        return results


    # 普通OLS回归:用 gains/S = IV^2 + QVV^2 + gains/S(-1) 在时间序列上回归
    # gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
    #已经证实：分Moneyness并不显著
    def run_3(self):

        # # 剔除实值期权
        # self.gains = self.gains[self.gains[C.Delta].abs() <= 0.5]

        #计算在值程度
        self.gains[C.KF_minus_1] = self.gains[C.KF] - 1
        self.gains[C.KF_minus_1_bin] = self.gains[C.CallOrPut] + (
            pd.cut(self.gains[C.KF_minus_1], bins=MONEYNESS_BIN)).astype(str)


        results = []
        for col_gain in COL_GAINS:
            gains_pivot = pd.pivot_table(self.gains, index=[C.TradingDate], columns=[C.KF_minus_1_bin],
                                         values=[col_gain])[col_gain]
            #gains_pivot.dropna(inplace=True)
            col_panel_Gains = ['C(-0.03, 0.03]', 'C(0.03, 0.1]', 'P(-0.03, 0.03]', 'P(-0.1, -0.03]']
            gains_pivot = gains_pivot[col_panel_Gains]
            gains_pivot = pd.merge(gains_pivot, self.RV, on=[C.TradingDate])
            gains_pivot = pd.merge(gains_pivot, self.Q_VV, on=[C.TradingDate])
            gains_pivot = pd.merge(gains_pivot, self.At_IV, on=[C.TradingDate])


            # 添加收益的滞后项
            col_panel_Gains_lag = [f'{x}(-1)' for x in col_panel_Gains]
            gains_pivot[col_panel_Gains_lag] = gains_pivot[col_panel_Gains].shift()#.fillna(method='bfill')
            # gains_pivot.fillna(method='bfill',inplace=True)
            #gains_pivot.dropna(inplace=True)


            for i in range(len(COL_IV)):
                for j in range(len(col_panel_Gains)):
                    X = gains_pivot[[COL_IV[i], COL_QVV[i], col_panel_Gains_lag[j]]]
                    Y = gains_pivot[col_panel_Gains[j]]

                    #剔除数据Nan值，并保持一致
                    set([1,2,3,4]).intersection(set([2,3,4,5,6]))
                    index_common=set(Y.dropna().index).intersection(set(X.dropna().index))
                    X=X.loc[index_common,:]
                    Y=Y.loc[index_common]

                    model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                    results.append([col_gain,COL_QVV[i],col_panel_Gains[j]]+params+tvalues+pvalues+[R_2])
        col_params = ['const', 'IV', 'QVV', 'gains(-1)']
        results=pd.DataFrame(results,
                             columns=['type_gain','type_QVV',C.KF_minus_1_bin]+col_params+[f't{x}' for x in col_params]+[f'p{x}' for x in col_params]+['R']
                             )

        results.to_csv(PATH_Moneyness_GAINS_OLS_IV_and_QVV,encoding='utf_8_sig',index=False)

    # 普通OLS回归:用 gains/S = IV^2 + QVV^2+JUMP + gains/S(-1) 在时间序列上回归
    # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    def run_4(self):

        # # 剔除实值期权
        # self.gains = self.gains[self.gains[C.Delta].abs() <= 0.5]
        # self.gains_pivot = pd.pivot_table(self.gains, index=[self.col_TradingDate],
        #                                   values=[self.col_Gains, C.Gains_to_underlying,
        #                                           C.Gains_to_option] + COL_IV + COL_QVV)

        # 添加JUMP风险
        JUMP = pd.read_csv(PATH_JUMP,index_col=0)
        self.gains_pivot[COL_JUMP]=JUMP
        self.gains_pivot.dropna(inplace=True)

        results = []
        for col_gain in COL_GAINS:
            for j in [0,1,3,4]:
                for i in range(len(COL_QVV)):
                    X = self.gains_pivot[[COL_IV[i], COL_QVV[i],COL_JUMP[j]]]
                    #X = self.gains_pivot[['RV', COL_QVV[i], COL_JUMP[j]]]
                    X['gains_lag1'] = self.gains_pivot[col_gain].shift().fillna(method='bfill')
                    Y = self.gains_pivot[col_gain]

                    model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                    results.append([col_gain,COL_JUMP[j],COL_QVV[i]] + params + tvalues + pvalues + [R_2])
        col_params = ['const', 'IV', 'QVV','JUMP', 'gains(-1)']
        results = pd.DataFrame(results,
                               columns=['type_gain','type_JUMP','type_QVV'] + col_params + [f't{x}' for x in col_params] + [f'p{x}' for x in
                                                                                               col_params] + ['R']
                               )

        results.to_csv(PATH_GAINS_OLS_IV_and_QVV_JUMP, encoding='utf_8_sig', index=False)

        return results

        # 普通OLS回归:用 gains/S = RV^2 + QVV^2+JUMP + gains/S(-1) 在时间序列上回归
        # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值

    def run_7(self):

        # # 剔除实值期权
        # self.gains = self.gains[self.gains[C.Delta].abs() <= 0.5]
        # self.gains_pivot = pd.pivot_table(self.gains, index=[self.col_TradingDate],
        #                                   values=[self.col_Gains, C.Gains_to_underlying,
        #                                           C.Gains_to_option] + COL_IV + COL_QVV)

        # 添加JUMP风险
        JUMP = pd.read_csv(PATH_JUMP, index_col=0)
        self.gains_pivot[COL_JUMP] = JUMP
        self.gains_pivot.dropna(inplace=True)

        results = []
        for col_gain in COL_GAINS:
            for j in [0, 1, 3, 4]:
                for i in range(len(COL_QVV)):
                    X = self.gains_pivot[['RV', COL_QVV[i], COL_JUMP[j]]]
                    # X = self.gains_pivot[['RV', COL_QVV[i], COL_JUMP[j]]]
                    X['gains_lag1'] = self.gains_pivot[col_gain].shift().fillna(method='bfill')
                    Y = self.gains_pivot[col_gain]

                    model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                    results.append([col_gain, COL_JUMP[j], COL_QVV[i]] + params + tvalues + pvalues + [R_2])
        col_params = ['const', 'RV', 'QVV', 'JUMP', 'gains(-1)']
        results = pd.DataFrame(results,
                               columns=['type_gain', 'type_JUMP', 'type_QVV'] + col_params + [f't{x}' for x in
                                                                                              col_params] + [f'p{x}' for
                                                                                                             x in
                                                                                                             col_params] + [
                                           'R']
                               )

        results.to_csv(PATH_GAINS_OLS_RV_and_QVV_JUMP, encoding='utf_8_sig', index=False)

        return results

    # 普通OLS回归:用 gains/S = IV^2 + QVV^2+ Q_SKEW+Q_KURT + gains/S(-1) 在时间序列上回归,
    # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    def run_8(self):

        # self.gains_pivot=self.gains_pivot.loc[self.gains_pivot.index<='2017-01-01',:]

        results = []

        for col_X in ([['IV','QVV',C.Q_SKEW,C.Q_KURT]]):
            result = []

            for days in WINDOWS_DAYS_NATURAL:
                X = self.gains_pivot[[f'{x}{days}' for x in col_X[:2]]+col_X[2:]]
                X[C.Gains_lag1] = self.gains_pivot[C.Gains_to_underlying].shift().fillna(method='bfill')
                Y = self.gains_pivot[C.Gains_to_underlying]

                model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                result.append([C.Gains_to_underlying] + [days] + params + tvalues + pvalues + [R_2])
            col_X = ['const'] + col_X + [C.Gains_lag1]
            result = pd.DataFrame(result,
                                  columns=['type_gain', 'Maturity'] + col_X + [f't{x}' for x in col_X] + [f'p{x}' for x
                                                                                                          in col_X] + [
                                              'R'])
            results.append(result)
        results = pd.concat(results, axis=0)

        results.to_csv(PATH_GAINS_OLS_IV_and_QVV_QSKEW_QKURT, encoding='utf_8_sig', index=False)

        return results

    # 普通OLS回归:用 gains/S = RV^2 + QVV^2+ Q_SKEW+Q_KURT + gains/S(-1) 在时间序列上回归,['RV','QVV',C.Q_SKEW,C.Q_KURT],
    #gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    def run_9(self):

        #self.gains_pivot=self.gains_pivot.loc[self.gains_pivot.index<='2019-02-02',:]

        results=[]

        for col_X in ([['RV','QVV',C.Q_SKEW,C.Q_KURT]]):
            result=[]

            for days in WINDOWS_DAYS_NATURAL:
                col_X_=[f'{x}{days}' if x=='QVV' else x for x in col_X]
                X = self.gains_pivot[col_X_]
                X[C.Gains_lag1] = self.gains_pivot[C.Gains_to_underlying].shift().fillna(method='bfill')
                Y = self.gains_pivot[C.Gains_to_underlying]

                model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                result.append([C.Gains_to_underlying]+[days] + params + tvalues + pvalues + [R_2])
            col_X=['const']+col_X+[C.Gains_lag1]
            result=pd.DataFrame(result,columns=['type_gain','Maturity']+col_X+[f't{x}' for x in col_X]+[f'p{x}' for x in col_X]+['R'])
            results.append(result)
        results=pd.concat(results,axis=0)

        results.to_csv(PATH_GAINS_OLS_RV_and_QVV_QSKEW_QKURT,encoding='utf_8_sig',index=False)

        return results


    #面板OLS回归:用 gains/S = IV^2 + PVV^2 + gains/S(-1) 在时间序列上回归
    #gains/S 是多条时间序列，按照moneyness(K/F)进行分类
    def run_5(self):

        #剔除实值期权
        self.gains=self.gains[self.gains[C.Delta].abs()<=0.5]

        #构建面板数据
        self.gains[C.KF].describe()
        self.gains[C.KF_minus_1]=self.gains[C.KF]-1
        self.gains[C.KF_minus_1_bin]=self.gains[C.CallOrPut]+(pd.cut(self.gains[C.KF_minus_1],bins=MONEYNESS_BIN)).astype(str)
        gains_pivot=pd.pivot_table(self.gains,index=[C.TradingDate],columns=[C.KF_minus_1_bin],values=[C.Gains_to_underlying])[C.Gains_to_underlying]
        col_panel_Gains=['C(-0.03, 0.03]', 'C(0.03, 0.1]', 'P(-0.03, 0.03]','P(-0.1, -0.03]']
        gains_pivot=gains_pivot[col_panel_Gains]
        gains_pivot=pd.merge(gains_pivot,self.RV,on=[C.TradingDate])
        gains_pivot = pd.merge(gains_pivot, self.Q_VV, on=[C.TradingDate])
        gains_pivot = pd.merge(gains_pivot, self.At_IV, on=[C.TradingDate])

        #添加收益的滞后项
        col_panel_Gains_lag = [f'{x}(-1)' for x in col_panel_Gains]
        gains_pivot[col_panel_Gains_lag]=gains_pivot[col_panel_Gains].shift().fillna(method='bfill')
        #gains_pivot.fillna(method='bfill',inplace=True)
        gains_pivot.dropna(inplace=True)

        #将数据改为面板格式
        gains_pivot[C.TradingDate]=pd.to_datetime(gains_pivot[C.TradingDate])
        gains_pivot.index=gains_pivot[C.TradingDate]

        Panel_=[]
        for date in gains_pivot.index:
            for x,y in zip(col_panel_Gains,col_panel_Gains_lag):
                values=gains_pivot.loc[date,[C.RV]+COL_QVV+COL_IV].tolist()
                gains=gains_pivot.loc[date,x]
                gains_lag=gains_pivot.loc[date,y]
                Panel_.append([date,x,gains,gains_lag]+values)

                print([date,x])



        Panel=pd.DataFrame(Panel_,columns=[C.TradingDate,C.KF_minus_1_bin]+[C.Gains,'Gains(-1)',C.RV]+COL_QVV+COL_IV)
        Panel

        X = gains_pivot[[COL_IV[0], COL_QVV[0],col_panel_Gains_lag[2]]]
        Y = gains_pivot[col_panel_Gains[3]]

        model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

    #已经证实,回归不显著
    # 普通OLS回归:用 gains/S = IV^2 + QVV^2 + gains/S(-1) 在时间序列上回归
    # gains/S 是一个单条时间序列，在每个交易年份内进行回归
    def run_6(self):

        #self.gains_pivot = self.gains_pivot.loc[self.gains_pivot.index >= '2018-01-01', :]

        years=self.gains_pivot.index.astype(str).str[:4].unique()
        self.gains_pivot['year']=self.gains_pivot.index.astype(str).str[:4]

        results = []
        for year in years:
            gains_pivot_year=self.gains_pivot[self.gains_pivot['year']==year]
            for col_gain in COL_GAINS:
                for i in range(len(COL_QVV)):
                    X = gains_pivot_year[[COL_IV[i], COL_QVV[i]]]
                    X['gains_lag1'] = gains_pivot_year[col_gain].shift().fillna(method='bfill')
                    Y = gains_pivot_year[col_gain]

                    model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

                    results.append([year,col_gain, COL_QVV[i]] + params + tvalues + pvalues + [R_2])
        col_params = ['const', 'IV', 'QVV', 'gains(-1)']
        results = pd.DataFrame(results,
                               columns=['year','type_gain', 'type_QVV'] + col_params + [f't{x}' for x in col_params] + [
                                   f'p{x}' for x in col_params] + ['R']
                               )

        results.to_csv(PATH_GAINS_OLS_IV_and_QVV_YEARS, encoding='utf_8_sig', index=False)

        return results

    #创建面板数据
    def construct_panel(self,


                        ):

        self.gains[self.col_KS]=self.gains[self.col_StrikePrice]/self.gains[self.col_UnderlyingScrtClose]

        bins = pd.IntervalIndex.from_tuples([(0.95, 0.975), (0.975, 1), (1, 1.025), (1.025, 1.05)])
        self.gains[self.col_KS_bin]=pd.cut(self.gains[self.col_KS],bins)
        self.gains[self.col_KS_bin]=self.gains[self.col_CallOrPut]+self.gains[self.col_KS_bin].astype(str)





        self.gains_pivot=pd.pivot_table(self.gains,index=[self.col_TradingDate],columns=[self.col_KS_bin],values=[self.col_Gains])[self.col_Gains]
        self.gains_pivot=self.gains_pivot.fillna(method='ffill')

        dict_moneyness=dict(zip(self.gains_pivot.columns,range(10)))

        #形成面板数据
        data=[]
        for index_ in self.gains_pivot.index:
            for col_ in self.gains_pivot.columns:
                data.append([index_,dict_moneyness[col_],self.gains_pivot.loc[index_,col_]])
        data=pd.DataFrame(data,columns=[self.col_TradingDate,self.col_KS_bin,self.col_Gains])

        self.RV.rename(columns={'trade_date':self.col_TradingDate},inplace=True)
        col_Q_VV=self.Q_VV.columns[1:]
        self.Q_VV.rename(columns={'trade_date':self.col_TradingDate},inplace=True)



        data=pd.merge(data,self.Q_VV,on=[self.col_TradingDate])
        data=pd.merge(data,self.RV,on=[self.col_TradingDate])

        data.index[self.col_TradingDate]
        data[self.col_Gains]
        data.reset_index(inplace=True)
        data[self.col_TradingDate]=(data[self.col_TradingDate].str[:4]+data[self.col_TradingDate].str[5:7]+data[self.col_TradingDate].str[8:10]).astype(int)

        import statsmodels.api as sm  # 回归
        import statsmodels.formula.api as smf  # 回归
        from linearmodels.panel import PanelOLS  # 面板回归

        col_indvidual = self.col_KS_bin  # 个体轴名称
        col_date = self.col_TradingDate  # 时间轴名称

        # 指定自变量和因变量列标题
        col_X = ['RV',col_Q_VV[1]]
        col_Y = self.col_Gains

        # 面板回归之前，需要先设置“个股在外时间在内”的层次化索引
        data.set_index([col_indvidual, col_date], inplace=True)

        # 指定自变量和因变量
        X = sm.add_constant(data[col_X])
        Y = data[col_Y]

        # 混合回归
        model_pooled = PanelOLS(Y, X, entity_effects=True, time_effects=False)
        model_pooled = model_pooled.fit()
        print(model_pooled)

        self.gains[self.col_delta_bin]=pd.qcut(self.gains[self.col_Gains].abs(), q=self.bins_moneyness)
        pd.pivot_table(self.gains, index=[self.col_TradingDate], columns=[self.col_delta_bin], values=[self.col_Gains], aggfunc=[np.size])




    # 为了调用方便，定义列标题
    def def_col(self):
        self.col_SecurityID = 'SecurityID'
        self.col_Symbol = 'Symbol'
        self.col_ExchangeCode = 'ExchangeCode'
        self.col_ContractCode = 'ContractCode'
        self.col_ShortName = 'ShortName'
        self.col_CallOrPut = 'CallOrPut'
        self.col_StrikePrice = 'StrikePrice'
        self.col_ExerciseDate = 'ExerciseDate'
        self.col_TradingDate = 'TradingDate'
        self.col_ClosePrice = 'ClosePrice'
        self.col_UnderlyingScrtClose = 'UnderlyingScrtClose'
        self.col_RemainingTerm = 'RemainingTerm'
        self.col_RisklessRate = 'RisklessRate'
        self.col_HistoricalVolatility = 'HistoricalVolatility'
        self.col_ImpliedVolatility = 'ImpliedVolatility'
        self.col_TheoreticalPrice = 'TheoreticalPrice'
        self.col_Delta = 'Delta'
        self.col_Gamma = 'Gamma'
        self.col_Vega = 'Vega'
        self.col_Theta = 'Theta'
        self.col_Rho = 'Rho'
        self.col_SettlePrice = 'SettlePrice'
        self.col_Volume = 'Volume'
        self.col_Position = 'Position'
        self.col_Amount = 'Amount'
        self.col_Gains='gains'
        self.col_delta_bin= 'delta_bin'
        self.col_KS = 'KS'
        self.col_KS_bin='KS_bin'
        self.col_Gains_to_option='gains_to_option'#收益/期权价格
        self.col_Gains_to_underlying = 'gains_to_underlying'  # 收益/标的价格
        self.col_RV='RV'



    #普通回归
    def norm_OLS(self):
        self.co


        pass





























if __name__=='__main__':


    # # 普通OLS回归:用 gains/S = IV + PVV + gains/S(-1) 在时间序列上回归
    # # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    # SOGAR=SeriesOlsGainsAndRisk()
    # SOGAR.run_1()



    # # 普通OLS回归:用 gains/S = RV + PVV + gains/S(-1) 在时间序列上回归
    # # gains/S 是一个单条时间序列，每个时间点上的值为所有moneyness对应的均值
    # SOGAR=SeriesOlsGainsAndRisk()
    # SOGAR.run_2()

    # # 普通OLS回归:用 gains/S = IV + PVV + gains/S(-1) 在时间序列上回归
    # # gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
    # SOGAR=SeriesOlsGainsAndRisk()
    # SOGAR.run_3()

    # # 普通OLS回归:用 gains/S = IV + PVV + gains/S(-1) 在时间序列上回归
    # # gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
    # SOGAR=SeriesOlsGainsAndRisk()
    # SOGAR.run_4()

    # # 普通OLS回归:用 gains/S = IV + PVV + gains/S(-1) 在时间序列上回归
    # # gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
    # SOGAR=SeriesOlsGainsAndRisk()
    # SOGAR.run_7()
    #
    # # 普通OLS回归:用 gains/S = RV^2 + QVV^2+ Q_SKEW+Q_KURT + gains/S(-1) 在时间序列上回归
    # # gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
    # SOGAR=SeriesOlsGainsAndRisk()
    # SOGAR.run_8()

    # # 普通OLS回归:用 gains/S = IV^2 + QVV^2+ Q_SKEW+Q_KURT + gains/S(-1) 在时间序列上回归
    # gains/S 是多条时间序列，按照moneyness(K/F)分别在每种moneyness上进行回归
    SOGAR=SeriesOlsGainsAndRisk()
    SOGAR.run_9()


    pass











