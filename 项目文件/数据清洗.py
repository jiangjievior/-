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
    data=option_price[option_price['ShortName'].str[:5]=='50ETF']#筛选50ETF期权数据
    data=data[data['DataType']==1]#筛选出实操数据
    data.dropna(inplace=True)#删掉缺失值所在的行

    #增加期权交易量数据
    option_volume=pd.read_csv(PATH_BASIC)
    data=pd.merge(data,option_volume[['TradingDate',
       'ContractCode','SettlePrice', 'Change1',
       'Change2', 'Volume', 'Position', 'Amount']],on=['TradingDate','ContractCode'])#把交易量数据加入到价格数据中

    #计算期权的次日价格、隐含波动率
    data.sort_values(['ContractCode','TradingDate'],inplace=True)#按照交易日和编码排序，在原表格进行替换
    data['next_Close']=data['ClosePrice'].shift(-1)#把列表上移一行
    data['next_ImpliedVolatility'] = data[C.ImpliedVolatility].shift(-1)  # 把列表上移一行
    #为了方便，直接排序平移，因此会把第二个期权的初始价格移动至第一个期权的末尾，需要处理！！
    data.reset_index(inplace=True)#重置索引，就地重置索引，设置inplace参数为True，否则将创建一个新的 DataFrame
    data['index']=data.index#重新分配索引
    data_drop=pd.pivot_table(data,index=[C.ContractCode],values=['index'],aggfunc=[np.nanmax])['nanmax'].reset_index()#插入数据透视表，以合约编码为索引，index对应每一合约最多持有的天数
    data=data.loc[set(data.index)-set(data_drop['index']),:]#删掉每一份合约最后一个交易日的数据
    data=data.drop('index',axis=1) #删除索引

    return data


#清洗筛选数据
def clean_data(data,
               path_save=False,#保存路径
               ):

    # 剔除交易日合约数量低于5的样本
    data = data[data['Volume'] > 5]

    #剔除交易日开仓头寸低于5的样本
    data=data[data['Position']>5]

    # 剔除delta绝对值高于0.98或低于0.02的样本
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
        -data_c['RisklessRate'].astype(float)/100 * data_c['RemainingTerm'].astype(float)))#看涨期权下限
    index_c = data_c[data_c['ClosePrice'] < data_c['套利'].apply(lambda x: max(x, 0))].index  # 看涨期权不满足套利条件的样本
    data.drop(index_c, axis=0, inplace=True)

    data_p = data[data['CallOrPut'] == 'P']
    data_p['套利'] = (
            data_p['StrikePrice'] * np.exp(-data_p['RisklessRate'].astype(float)/100 * data_p['RemainingTerm'].astype(float)) - data_p[
        'UnderlyingScrtClose'])#看跌期权下限
    index_p = data_p[data_p['ClosePrice'] < data_p['套利'].apply(lambda x: max(x, 0))].index  # 看跌期权不满足套利条件的样本
    data.drop(index_p, axis=0, inplace=True)#删除不满足套利条件的期权

    #计算在值程度:参考陈蓉(2010)《隐含波动率曲面_建模与实证_陈蓉》.P144
    data[C.KF]=data['StrikePrice']/(data['UnderlyingScrtClose']*np.exp(data['RemainingTerm']*data['RisklessRate']/100))

    # 按照在值程度分类分组
    data[C.KF_minus_1] = data[C.KF] - 1
    data[C.KF_minus_1_bin] = data[C.CallOrPut] + (
        pd.cut(data[C.KF_minus_1], bins=MONEYNESS_BIN)).astype(str)


    if path_save:
        data.to_csv(path_save,encoding='utf_8_sig',index=False)

    return data












if __name__=='__main__':
    data=get_data()
    data=clean_data(data,path_save=PATH_50ETF_OPTION)





































