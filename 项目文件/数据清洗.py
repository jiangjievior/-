# -*- coding:utf-8 -*-
import Cython

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
    data.sort_values(['ContractCode','TradingDate'],inplace=True)
    data['next_Close']=data['ClosePrice'].shift(-1)
    #为了方便，直接排序平移，因此会把第二个期权的初始价格移动至第一个期权的末尾，需要处理！！
    data.reset_index(inplace=True)
    data['index']=data.index
    data_drop=pd.pivot_table(data,index=[C.ContractCode],values=['index'],aggfunc=[np.nanmax])['nanmax'].reset_index()
    data=data.loc[set(data.index)-set(data_drop['index']),:]
    data=data.drop('index',axis=1)

    #增加期货交易价格数据
    future=pd.read_csv(PATH_50ETF_FUTURE)

    return data


#清洗筛选数据
def clean_data(data,
               path_save=False,#保存路径
               ):

    # 剔除交易日合约数量低于5的样本
    data = data[data['Volume'] > 5]

    #剔除交易日开仓头寸低于5的样本
    data=data[data['Position']>5]

    # 剔除delta绝对值高于0.8或低于0.02的样本
    data = data[(data['Delta'].abs() <= 0.98) & ((data['Delta'].abs() >= 0.02))]

    #剔除隐含波动率超过100% 或者小于1%的期权
    data=data[(data['ImpliedVolatility']<=1)&(data['ImpliedVolatility']>=0.01)]


    # 剔除剩余到期时间低于7个交易日
    #RemainingTerm:交易日至行权日之间的天数(自然日)除以365。
    data=data[data['RemainingTerm']>=7/365]

    # 剔除剩余到期时间高于1年
    data=data[data['RemainingTerm']<=365/365]

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

    #计算在值程度:参考陈蓉(2010)《隐含波动率曲面_建模与实证_陈蓉》.P144
    data[C.KF]=data['StrikePrice']/(data['UnderlyingScrtClose']*np.exp(-data['RemainingTerm']*data['RisklessRate']/100))


    if path_save:
        data.to_csv(path_save,encoding='utf_8_sig',index=False)

    return data












if __name__=='__main__':
    data=get_data()
    data=clean_data(data)





































