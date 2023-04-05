# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

from 项目文件.修改数据结果格式 import path_reformat



#所使用数据的描述
def table_3_1():
    Option=pd.read_csv(PATH_50ETF_OPTION)
    Option

    Option[Option[C.CallOrPut]=='C']
    Option[Option[C.CallOrPut] == 'P']

    len(Option[C.TradingDate].unique())

    Option[C.TradingDate].min()
    Option[C.TradingDate].max()









def table_3_2():
    data=pd.read_csv(PATH_Q_VV,index_col=0)
    data.columns=WINDOWS_DAYS_NATURAL
    data.describe()
    results=pd.DataFrame({
        'mean':data.mean(),
        'std':data.std(),
        'min': data.min(),
        '25%':data.quantile(q=0.25),
        '75%':data.quantile(q=0.75),
        'max': data.max(),
        'skew':data.skew(),
        'kurt':data.kurt()
    }).round(3).T[WINDOWS_DAYS_NATURAL[:-2]]
    results.to_csv(PATH_FINAL_RESULTS+'/表3_1.csv',encoding='utf_8_sig')









#4(2)	Delta中性收益预测
def table_4_2():
    Results_RV=pd.read_csv(path_reformat(PATH_GAINS_OLS_RV_and_QVV))
    Results_IV=pd.read_csv(path_reformat(PATH_GAINS_OLS_IV_and_QVV))

    Results_RV=Results_RV[Results_RV['Maturity']==30]
    Results_IV = Results_IV[Results_IV['Maturity'] == 30]
    results=pd.concat([Results_RV,Results_IV],keys=['RV','IV'],axis=1)
    results.to_csv(PATH_FINAL_RESULTS+'/表4_2.csv',encoding='utf_8_sig',index=False)







if __name__=='__main__':
    table_3_1()
    table_3_2()
    table_4_2()


























































