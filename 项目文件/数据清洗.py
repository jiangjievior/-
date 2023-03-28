# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os


# 提取50ETF期权数据
def get_data():
    #期权价格数据
    option_price=pd.read_csv(PATH_PARAMETERS)
    data=option_price[option_price['ShortName'].str[:5]=='50ETF']
    data=data[data['DataType']==1]
    data.dropna(inplace=True)

    #增加期权交易量数据
    option_volume=pd.read_csv(PATH_BASIC)
    data=pd.merge(data,option_volume[['TradingDate',
       'ContractCode','SettlePrice', 'Change1',
       'Change2', 'Volume', 'Position', 'Amount']],on=['TradingDate','ContractCode'])

    #计算期权的次日价格
    #为了方便，直接排序平移，因此会把第二个期权的初始价格移动至第一个期权的末尾，需要处理！！
    data.sort_values(['ContractCode','TradingDate'],inplace=True)
    data['next_Close']=data['ClosePrice'].shift(-1)

    #增加期货交易价格数据
    future=pd.read_csv(PATH_50ETF_FUTURE)
    future


    return data


#清洗筛选数据
def clean_data(data,
               path_save=False,#保存路径
               ):

    # 剔除交易日合约数量低于0的样本
    data = data[data['Volume'] > 0]

    #剔除交易日开仓头寸低于0的样本
    data=data[data['Position']>0]

    # 剔除delta绝对值高于0.8或低于0.02的样本
    data = data[(data['Delta'].abs() <= 0.98) & ((data['Delta'].abs() >= 0.02))]

    # 剔除剩余到期时间低于7个交易日
    data=data[data['RemainingTerm']>=7/365]

    # 剔除不满足套利条件的样本
    data_c = data[data['CallOrPut'] == 'C']
    data_c['套利'] = (
            data_c['UnderlyingScrtClose'] - data_c['StrikePrice'] * np.exp(
        -data_c['RisklessRate'].astype(float)/100 * data_c['RemainingTerm'].astype(float)))
    index_c = data_c[data_c['ClosePrice'] < data_c['套利'].apply(lambda x: max(x, 0))].index  # 看涨期权满足套利条件的样本
    data.drop(index_c, axis=0, inplace=True)

    data_p = data[data['CallOrPut'] == 'P']
    data_p['套利'] = (
            data_p['StrikePrice'] * np.exp(-data_p['RisklessRate'].astype(float)/100 * data_p['RemainingTerm'].astype(float)) - data_p[
        'UnderlyingScrtClose'])
    index_p = data_p[data_p['ClosePrice'] < data_p['套利'].apply(lambda x: max(x, 0))].index  # 看跌期权满足套利条件的样本
    data.drop(index_p, axis=0, inplace=True)

    if path_save:
        data.to_csv(path_save,encoding='utf_8_sig',index=False)

    return data












if __name__=='__main__':
    data=get_data()
    data=clean_data(data)





































