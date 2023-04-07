#《Unknown Unknowns: Uncertainty About Risk and Stock Returns》
import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *


#在各个剩余到期时间上，使用平值隐含波动率计算vol-of-vol
def implied_vol_of_vol(path_surface_series:str,#隐含波动率曲面时间序列
                    path_save:str=False,#历史波动率的波动率的保存路径
                    moneyness=1,#在值程度

                    )->pd.DataFrame:
    surface_series=pd.read_csv(path_surface_series)#读取波动率曲面时间序列数据
    surface_series=surface_series[surface_series[C.KF]==moneyness]#筛选出平值期权
    surface_series=pd.pivot_table(surface_series,index=C.TradingDate,columns='years',values='IV')

    date_s=surface_series.index.tolist()#根据条件获取元素所在的位置（索引），获取交易日时间序列

    lags=20
    vol_of_vol_s= {}#？
    for date in date_s[lags:]:#
        try:
            IV_date=surface_series.loc[date_s[date_s.index(date)-lags]:date,:]#根据索引获取某一data二十天前的索引对应的date到当日date的数据
            IV_mean=IV_date.sum()/lags#过去20天IV平方和除以20
            vol_of_vol=(np.sqrt(((IV_date-IV_mean)**2).sum()/lags)/IV_mean).tolist()#计算vov的公式，将vov转化为列表
            vol_of_vol_s[date]=vol_of_vol#方便看出是哪个交易日的vov
            print(f'计算moneyness为{moneyness}Q_VV已经完成{date_s.index(date)/len(date_s)}')#qvv计算
        except:
            continue

    vol_of_vol_s=pd.DataFrame(vol_of_vol_s,index=surface_series.columns).T#与波动率曲面时间序列数据相同的列标签，建立VV曲面时间序列
    vol_of_vol_s.index.name=C.TradingDate#索引设置为交易日
    if path_save:
        vol_of_vol_s.to_csv(path_save,encoding='utf_8_sig')

    return vol_of_vol_s



#在各个在值程度和剩余到期时间上计算隐含VV：
def vol_of_vol_moneyness(path_save=False):
    VV_s=[]
    for KF in MONEYNESS_KF:
        VV=implied_vol_of_vol(PATH_IV_SURFACE_SERIES,moneyness=KF)#不同在值程度下计算IVV
        VV_s.append(VV)#算一个在值程度，在VV_s后加一列
    VV_s=pd.concat(VV_s,keys=MONEYNESS_KF)#keys合并后保留KF的信息
    VV_s.index.names=[C.KF,C.TradingDate]#在值程度和交易日期作为索引（合并后保留在值程度的信息）
    VV_s.columns=WINDOWS_DAYS_NATURAL
    VV_s.reset_index(inplace=True)
    if path_save:
        VV_s.to_csv(PATH_Q_VV_Moneyness,encoding='utf_8_sig',index=False)










if __name__=='__main__':

    path_surface_series=data_real_path('数据文件/生成数据/隐含波动率曲面时间序列.csv')
    path_save=data_real_path('数据文件/生成数据')+'/隐含vol_of_vol.csv'
    implied_vol_of_vol(path_surface_series)

    vol_of_vol_moneyness(path_save=PATH_Q_VV_Moneyness)






















































