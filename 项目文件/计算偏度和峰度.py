# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

from 项目文件.数据清洗 import get_data


# 计算P偏度：参考2022，郑振龙，《方差风险、偏度风险与市场收益率的可预测性》
def P_SKEW():
    data = pd.read_csv(PATH_50ETF_5MIN)
    data['r'] = np.log(data['close'] / data['close'].shift())
    data[C.TradingDate] = data['trade_time'].astype(str).str[:10]
    P_SKEW_s = []
    for date in data[C.TradingDate].unique():
        data_date = data[data[C.TradingDate] == date].dropna()
        SKEW = sum(data_date['r'] ** 3) / (sum(data_date['r'] ** 2) ** (3 / 2)) * np.sqrt(len(data_date))
        P_SKEW_s.append([date, SKEW])
        print(f'计算P_SKEW已经完成{date}')

    P_SKEW_s = pd.DataFrame(P_SKEW_s, columns=[C.TradingDate, C.P_SKEW])
    P_SKEW_s.to_csv(PATH_P_SKEW, encoding='utf_8_sig', index=False)


# 计算Q偏度和Q峰度
# 参考：2020,《上证50ETF隐含高阶矩风险对股票收益的预测研究》，王琳玉
# 参考：2013，《Does Risk-Neutral Skewness Predict the Cross Section of Equity Option Portfolio Returns?》
def Q_SKEW_KURT():

    data = get_data()

    # 筛选剩余到期时间介于10天至60天的期权
    # RemainingTerm:交易日至行权日之间的天数(自然日)除以365。
    data = data[data['RemainingTerm'] >= 10 / 365]

    # 剔除剩余到期时间高于60天
    data = data[data['RemainingTerm'] <= 60 / 365]

    # 剔除不满足套利条件的样本
    data_c = data[data['CallOrPut'] == 'C']
    data_c['套利'] = (
            data_c['UnderlyingScrtClose'] - data_c['StrikePrice'] * np.exp(
        -data_c['RisklessRate'].astype(float) / 100 * data_c['RemainingTerm'].astype(float)))  # 看涨期权下限
    index_c = data_c[data_c['ClosePrice'] < data_c['套利'].apply(lambda x: max(x, 0))].index  # 看涨期权不满足套利条件的样本
    data.drop(index_c, axis=0, inplace=True)

    data_p = data[data['CallOrPut'] == 'P']
    data_p['套利'] = (
            data_p['StrikePrice'] * np.exp(
        -data_p['RisklessRate'].astype(float) / 100 * data_p['RemainingTerm'].astype(float)) - data_p[
                'UnderlyingScrtClose'])  # 看跌期权下限
    index_p = data_p[data_p['ClosePrice'] < data_p['套利'].apply(lambda x: max(x, 0))].index  # 看跌期权不满足套利条件的样本
    data.drop(index_p, axis=0, inplace=True)  # 删除不满足套利条件的期权

    data
    results = []
    for date in data[C.TradingDate].unique():
        data_date = data[data[C.TradingDate] == date]

        # 保证期权剩余到期时间一致
        RemainingTerm = data_date[C.RemainingTerm].unique()[0]
        RisklessRate = data_date[C.RisklessRate].unique()[0]
        data_date = data_date[data_date[C.RemainingTerm] == RemainingTerm]

        # 筛选虚值期权
        data_date = data_date[data_date[C.Delta].abs() <= 0.5]

        data_C = data_date[data_date[C.CallOrPut] == 'C']
        data_P = data_date[data_date[C.CallOrPut] == 'P']

        V = sum((2 * (1 - np.log(data_C[C.StrikePrice] / data_C[C.UnderlyingScrtClose])) / data_C[C.StrikePrice] ** 2) *
                data_C[C.ClosePrice] * K_DIFF) + \
            sum((2 * (1 + np.log(data_P[C.UnderlyingScrtClose] / data_P[C.StrikePrice])) / data_P[C.StrikePrice] ** 2) *
                data_P[C.ClosePrice] * K_DIFF)

        W = sum(((6 * np.log(data_C[C.StrikePrice] / data_C[C.UnderlyingScrtClose]) - 3 * np.log(
            data_C[C.StrikePrice] / data_C[C.UnderlyingScrtClose]) ** 2) / data_C[C.StrikePrice] ** 2) * data_C[
                    C.ClosePrice] * K_DIFF) \
            - sum(((6 * np.log(data_P[C.UnderlyingScrtClose] / data_P[C.StrikePrice]) + 3 * np.log(
            data_P[C.UnderlyingScrtClose] / data_P[C.StrikePrice]) ** 2) / data_P[C.StrikePrice] ** 2) * data_P[
                      C.ClosePrice] * K_DIFF)

        X = sum(((12 * np.log(data_C[C.StrikePrice] / data_C[C.UnderlyingScrtClose]) ** 2 - 4 * np.log(
            data_C[C.StrikePrice] / data_C[C.UnderlyingScrtClose]) ** 3) / data_C[C.StrikePrice] ** 2) * data_C[
                    C.ClosePrice] * K_DIFF) \
            + sum(((12 * np.log(data_P[C.UnderlyingScrtClose] / data_P[C.StrikePrice]) + 4 * np.log(
            data_P[C.UnderlyingScrtClose] / data_P[C.StrikePrice]) ** 3) / data_P[C.StrikePrice] ** 2) * data_P[
                      C.ClosePrice] * K_DIFF)

        EXP = np.exp(RisklessRate / 100 * RemainingTerm)
        miu = EXP - 1 - EXP * V / 2 - EXP * W / 6 - EXP * X / 24

        VOL = (EXP * V - miu ** 2) ** (1 / 2)
        SKEW = (EXP * W - 3 * miu * EXP * V + 2 * miu ** 3) / (EXP * V - miu ** 2) ** (3 / 2)
        KURT = (EXP * X - 4 * miu * EXP * W + 6 * miu ** 2 * EXP * V - 3 * miu ** 4) / (EXP * V - miu ** 2) ** 2

        results.append([date, VOL, SKEW, KURT])

        print(f'计算Q_SKEW和Q_KURT已经完成{date}')
    results = pd.DataFrame(results, columns=[C.TradingDate, C.ImpliedVolatility, C.Q_SKEW, C.Q_KURT])

    results.to_csv(PATH_Q_SKEW_KURT,encoding='utf_8_sig',index=False)


if __name__=='__main__':
    P_SKEW()

    Q_SKEW_KURT()









































































