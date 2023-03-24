# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os


# 提取50ETF期权数据
def get_data(
        path_option_price='',
        path_option_volume='',
):
    #期权价格数据
    option_price=pd.read_csv(path_option_price)
    data=option_price[option_price['ShortName'].str[:5]=='50ETF']
    data=data[data['DataType']==1]
    data.dropna(inplace=True)

    #增加期权交易量数据
    option_volume=pd.read_csv(path_option_volume)
    data=pd.merge(data,option_volume[['TradingDate',
       'ContractCode','SettlePrice', 'Change1',
       'Change2', 'Volume', 'Position', 'Amount']],on=['TradingDate','ContractCode'])


    return data


#清洗筛选数据
def clean_data(data,
               path_save=False,#保存路径
               ):

    # 剔除交易日合约数量低于0的样本
    data = data[data['Volume'] > 0]

    # 剔除delta绝对值高于0.8或低于0.02的样本
    data = data[(data['Delta'].abs() <= 0.98) & ((data['Delta'].abs() >= 0.02))]

    # 剔除剩余到期时间低于五个交易日
    data=data[data['RemainingTerm']>=5/365]

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
    data=get_data(path_option_price=data_real_path('数据文件/原始数据/期权收盘价/SO_PricingParameter.csv'),
                  path_option_volume=data_real_path('数据文件/原始数据/期权交易量数据/SO_QuotationBas.csv')
                  )
    data=clean_data(data)





































