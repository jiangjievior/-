#《Unknown Unknowns: Uncertainty About Risk and Stock Returns》
import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path


#在各个剩余到期时间上，使用平值隐含波动率计算vol-of-vol
def implied_vol_of_vol(path_surface_series:str,#隐含波动率曲面时间序列
                    path_save:str=False,#历史波动率的波动率的保存路径
                    col_m:str='K/S',
                    col_maturity:str='years',
                    col_IV:str='IV',
                    col_tradeDate:str='date',
                    )->pd.DataFrame:
    surface_series=pd.read_csv(path_surface_series)
    surface_series=surface_series[surface_series[col_m]==1]
    surface_series=pd.pivot_table(surface_series,index='date',columns='years',values='IV')

    date_s=surface_series.index.tolist()

    lags=20
    vol_of_vol_s= {}
    for date in date_s[lags:]:
        try:
            IV_date=surface_series.loc[date_s[date_s.index(date)-lags]:date,:]
            IV_mean=IV_date.sum()/lags
            vol_of_vol=(np.sqrt(((IV_date-IV_mean)**2).sum()/lags)/IV_mean).tolist()
            vol_of_vol_s[date]=vol_of_vol
            print(f'计算移动平均vol-of-vol已经完成{date_s.index(date)/len(date_s)}')
        except:
            continue

    vol_of_vol_s=pd.DataFrame(vol_of_vol_s,index=surface_series.columns).T
    if path_save:
        vol_of_vol_s.to_csv(path_save,encoding='utf_8_sig')














if __name__=='__main__':
    path_surface_series=data_real_path('数据文件/生成数据/隐含波动率曲面时间序列.csv')
    path_save=data_real_path('数据文件/生成数据')+'/隐含vol_of_vol.csv'
    implied_vol_of_vol(path_surface_series)






















































