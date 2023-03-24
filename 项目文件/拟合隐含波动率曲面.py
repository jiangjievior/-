# -*- coding:utf-8 -*-
import copy

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import statsmodels.api as sm

# 参考陈蓉（2010）,按照  ln(IV)=b1+b2*K/S+b3*(K/S)^2+b4*years+b5*(years*K/S) 建立隐含波动率曲面
def construct_volatility_surface(
        data='',#待读取数据
        grids=[
            [0.8, 0.9, 1, 1.1, 1.2],
            [1 / 12, 2 / 12, 3 / 12, 6 / 12, 1]
        ],#隐含波动率曲面底部格点
        path_save=False

    ):

    dates=data['TradingDate'].unique()

    # 按照  ln(IV)=b1+b2*K/S+b3*(K/S)^2+b4*years+b5*(years*K/S)
    #参考陈蓉（2010）
    data['ln(IV)']=np.log(data['ImpliedVolatility'])
    data['K/S'] =data['StrikePrice']/data['UnderlyingScrtClose']
    data['(K/S)^2'] =data['K/S']**2
    data['years']=data['RemainingTerm']
    data['years*(K/S)']=data['years']*data['K/S']

    #拟合隐含波动率曲面模型
    models={}
    for date in dates:
        data_date=data[data['TradingDate']==date]
        X = data_date[['K/S', '(K/S)^2', 'years', 'years*(K/S)']]  # 解释变量
        X=sm.add_constant(X)
        Y = data_date['ln(IV)']  # 被解释变量
        model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)

        models[date]=model
        print(f'拟合隐含波动率曲面模型已经完成{date}')


    #建立隐含波动率曲面时间序列

    #将底部格点恢复成并列结构
    grids=[[x,y] for x in grids[0] for y in grids[1]]
    volatility_surface=pd.DataFrame(grids,columns=['K/S','years'])
    volatility_surface['(K/S)^2'] = volatility_surface['K/S'] ** 2
    volatility_surface['years*(K/S)'] = volatility_surface['years'] * volatility_surface['K/S']

    volatility_surface_series=[]
    for key in models.keys():
        volatility_surface_=copy.deepcopy(volatility_surface)
        volatility_surface_['ln(IV)']=models[key].predict(sm.add_constant(volatility_surface[['K/S', '(K/S)^2', 'years', 'years*(K/S)']]))
        volatility_surface_['IV'] =np.exp(volatility_surface_['ln(IV)'])
        volatility_surface_['date']=key

        volatility_surface_series.append(volatility_surface_)
    volatility_surface_series=pd.concat(volatility_surface_series,axis=0)

    if path_save:
        volatility_surface_series.to_csv(path_save,encoding='utf_8_sig',index=False)




if __name__=="__main__":
    option=pd.read_csv(data_real_path('数据文件/生成数据/上证50ETF期权数据.csv'))
    construct_volatility_surface(data=option,
                                 grids=[
                                     [0.8,0.9,1,1.1,1.2],
                                     [1/12,2/12,3/12,6/12,1]
                                 ],
                                 path_save=data_real_path('数据文件/生成数据')+'/隐含波动率曲面时间序列.csv'
                                 )















