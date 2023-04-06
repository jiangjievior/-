# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

#依据P值为数据标*号
def star(p):
    if p<=0.01:
        return '***'
    elif p<=0.05:
        return '**'
    elif p<=0.1:
        return '*'
    else:
        return ''

#输入原来路径，生成修改后的路径，以作区分
def path_reformat(path):
    path=path[:-4]+'_格式修改'+path[-4:]
    return path




#修改格式
#'volatility of volatility in China/数据文件/生成数据/GAINS_OLS_IV_and_QVV回归结果.csv'
def reformat_run_1():
    data=pd.read_csv(PATH_GAINS_OLS_IV_and_QVV)
    data=data[data['type_gain']==C.Gains_to_underlying]

    results=[]
    cols=['IV', 'QVV', 'gains(-1)']
    for col in cols:
        result=((data[col]*100).round(2).astype(str)+'('+(data['t'+col].round(2)).astype(str)+')'+data['p'+col].apply(lambda x:star(x))).tolist()
        results.append(result)

    results=pd.DataFrame(results,index=cols).T
    results['R']=data['R'].round(3).values
    results.insert(loc=0,column='Maturity',value=data['Maturity'].values)

    results.to_csv(path_reformat(PATH_GAINS_OLS_IV_and_QVV),encoding='utf_8_sig',index=False)

    return results

#修改格式
#'数据文件/生成数据/GAINS_OLS_RV_and_QVV回归结果.csv'
def reformat_run_2():
    data=pd.read_csv(PATH_GAINS_OLS_RV_and_QVV)
    data=data[data['type_gain']==C.Gains_to_underlying]

    results=[]
    cols=['RV', 'QVV', 'gains(-1)']
    for col in cols:
        result=((data[col]*100).round(2).astype(str)+'('+(data['t'+col].round(2)).astype(str)+')'+data['p'+col].apply(lambda x:star(x))).tolist()
        results.append(result)

    results=pd.DataFrame(results,index=cols).T
    results['R']=data['R'].round(3).values
    results.insert(loc=0,column='Maturity',value=data['Maturity'].values)

    results.to_csv(path_reformat(PATH_GAINS_OLS_RV_and_QVV),encoding='utf_8_sig',index=False)

    return results

#修改格式
#'基于不同在值程度的GAINS_OLS_IV_and_QVV回归结果.csv'
def reformat_run_3():
    data=pd.read_csv(PATH_Moneyness_GAINS_OLS_IV_and_QVV)
    data=data[data['type_gain']==C.Gains_to_underlying]

    results=[]
    cols=['IV', 'QVV', 'gains(-1)']
    for col in cols:
        result=((data[col]*100).round(2).astype(str)+'('+(data['t'+col].round(2)).astype(str)+')'+data['p'+col].apply(lambda x:star(x))).tolist()
        results.append(result)

    results=pd.DataFrame(results,index=cols).T
    results['R']=data['R'].round(3).values
    results.insert(loc=0, column='Moneyness(K/F-1)', value=data[C.KF_minus_1_bin].values)
    results.insert(loc=1,column='Maturity',value=data['type_QVV'].values)
    results['Maturity']=results['Maturity'].str[3:].astype(int)
    results = results.loc[results['Maturity']!=360,:]
    results.sort_values(['Moneyness(K/F-1)','Maturity'],inplace=True)


    results.to_csv(path_reformat(PATH_Moneyness_GAINS_OLS_IV_and_QVV),encoding='utf_8_sig',index=False)

    return results

#修改格式
#'数据文件/生成数据/GAINS_OLS_IV_and_QVV_JUMP回归结果.csv'
def reformat_run_4():
    data=pd.read_csv(PATH_GAINS_OLS_IV_and_QVV_JUMP)
    data=data[data['type_gain']==C.Gains_to_underlying]

    results = []
    cols = ['IV', 'QVV','JUMP', 'gains(-1)']
    for col in cols:
        result = ((data[col]*100).round(2).astype(str) + '(' + (data['t' + col].round(2)).astype(str) + ')' + data[
            'p' + col].apply(lambda x: star(x))).tolist()
        results.append(result)

    results = pd.DataFrame(results, index=cols).T
    results['R'] = data['R'].round(3).values
    results.insert(loc=0, column='Moneyness', value=data['type_JUMP'].values)
    results.insert(loc=1, column='Maturity', value=data['type_QVV'].values)
    results = results.loc[results['Maturity'] != 'QVV360', :]

    results.to_csv(path_reformat(PATH_GAINS_OLS_IV_and_QVV_JUMP),encoding='utf_8_sig',index=False)

    return results

#修改格式
#'数据文件/生成数据/GAINS_OLS_RV_and_QVV_JUMP回归结果.csv'
def reformat_run_7():
    data=pd.read_csv(PATH_GAINS_OLS_RV_and_QVV_JUMP)
    data=data[data['type_gain']==C.Gains_to_underlying]

    results = []
    cols = ['RV', 'QVV','JUMP', 'gains(-1)']
    for col in cols:
        result = ((data[col]*100).round(2).astype(str) + '(' + (data['t' + col].round(2)).astype(str) + ')' + data[
            'p' + col].apply(lambda x: star(x))).tolist()
        results.append(result)

    results = pd.DataFrame(results, index=cols).T
    results['R'] = data['R'].round(3).values
    results.insert(loc=0, column='Moneyness', value=data['type_JUMP'].values)
    results.insert(loc=1, column='Maturity', value=data['type_QVV'].values)
    results = results.loc[results['Maturity'] != 'QVV360', :]

    results.to_csv(path_reformat(PATH_GAINS_OLS_RV_and_QVV_JUMP),encoding='utf_8_sig',index=False)

    return results


#修改格式
#'数据文件/生成数据/GAINS_OLS_IV_and_QVV_JUMP回归结果.csv'
def reformat_run_8():
    data=pd.read_csv(PATH_GAINS_OLS_IV_and_QVV_QSKEW_QKURT)
    data=data[data['type_gain']==C.Gains_to_underlying]

    results = []
    cols = ['IV', 'QVV',C.Q_SKEW,C.Q_KURT, 'gains(-1)']
    for col in cols:
        result = ((data[col]*100).round(2).astype(str) + '(' + (data['t' + col].round(2)).astype(str) + ')' + data[
            'p' + col].apply(lambda x: star(x))).tolist()
        results.append(result)

    results = pd.DataFrame(results, index=cols).T
    results['R'] = data['R'].round(3).values
    results.insert(loc=1, column='Maturity', value=data['Maturity'].values)
    results = results.loc[results['Maturity'] != '360', :]

    results.to_csv(path_reformat(PATH_GAINS_OLS_IV_and_QVV_QSKEW_QKURT),encoding='utf_8_sig',index=False)

    return results


#修改格式
#'数据文件/生成数据/GAINS_OLS_RV_and_QVV_JUMP回归结果.csv'
def reformat_run_9():
    data=pd.read_csv(PATH_GAINS_OLS_RV_and_QVV_QSKEW_QKURT)
    data=data[data['type_gain']==C.Gains_to_underlying]

    results = []
    cols = ['RV', 'QVV',C.Q_SKEW,C.Q_KURT, 'gains(-1)']
    for col in cols:
        result = ((data[col]*100).round(3).astype(str) + '(' + (data['t' + col].round(2)).astype(str) + ')' + data[
            'p' + col].apply(lambda x: star(x))).tolist()
        results.append(result)

    results = pd.DataFrame(results, index=cols).T
    results['R'] = data['R'].round(3).values
    results.insert(loc=0, column='Maturity', value=data['Maturity'].values)
    results = results.loc[results['Maturity'] != '360', :]

    results.to_csv(path_reformat(PATH_GAINS_OLS_RV_and_QVV_QSKEW_QKURT),encoding='utf_8_sig',index=False)

    return results



if __name__=='__main__':
    reformat_run_4()

    reformat_run_3()

    reformat_run_2()

    # 修改格式'volatility of volatility in China/数据文件/生成数据/GAINS_OLS_IV_and_QVV回归结果.csv'
    reformat_run_1()



































