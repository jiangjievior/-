import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path






def realized_vol_of_vol(
        path_close_5_min='',
        windows=[30, 60, 90, 180, 360],#滑动窗口天数
        path_save=False,
        type=1,#类型

):
    data=pd.read_csv(path_close_5_min)
    data=data[data['trade_time']>='2015-02-01 00:00:00'].reset_index()

    #第一种类型计算波动率的波动率
    #先滑动窗口计算已实现波动率，再逐日计算已实现波动率的波动率

    if type==1:
        data['r']=np.log(data['close']/data['close'].shift())
        #计算已实现波动率
        N=48
        realized_Vol=[]
        for i in range(N-1,len(data)):
            vol=np.sqrt((data.loc[(i-N-1):i,'r']**2).sum())
            realized_Vol.append([data.loc[i,'trade_time'],vol])
            print(f'计算已实现波动率完成{data.loc[i,"trade_time"]}')
        realized_Vol=pd.DataFrame(realized_Vol,columns=['trade_time','vol'])

        #计算已实现波动率的波动率
        realized_Vol['trade_date']=realized_Vol['trade_time'].str[:10]
        vol_of_vol_s=[]
        for date in realized_Vol['trade_date'].unique():

            Vol_date=realized_Vol.loc[realized_Vol['trade_date']==date,'vol']
            mean_Vol=Vol_date.mean()

            vol_of_vol=np.sqrt(sum((Vol_date-mean_Vol)**2)/N)/mean_Vol

            vol_of_vol_s.append([date,vol_of_vol])
        vol_of_vol_s=pd.DataFrame(vol_of_vol_s,columns=['date','vol_of_vol'])


        if path_save:
            vol_of_vol_s.to_csv(path_save,encoding='utf_8_sig',index=False)


























if __name__=='__main__':
    realized_vol_of_vol(path_close_5_min=data_real_path('数据文件/原始数据/ETF50五分钟收盘价.csv'),
                        windows=[1 / 12, 2 / 12, 3 / 12, 6 / 12, 1],
                        path_save=data_real_path('数据文件/生成数据')+'/已实现vol_of_vol.csv'
                        )









