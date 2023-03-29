import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *





def realized_vol_of_vol(
        path_close_5_min='',
        windows=[30, 60, 90, 180, 360],#滑动窗口天数
        path_save=False,
        type=1,#类型

):


    #第一种类型计算波动率的波动率
    #先滑动窗口计算已实现波动率，再逐日计算已实现波动率的波动率

    if type==1:
        data = pd.read_csv(PATH_50ETF_5MIN)
        data = data[data['trade_time'] >= '2015-02-01 00:00:00'].reset_index()

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


    #先计算每日已实现波动率，再滑动窗口计算历史 VV
    elif type==2:
        data = pd.read_csv(PATH_50ETF_5MIN)
        data = data[data['trade_time'] >= '2015-02-01 00:00:00'].reset_index()

        data['r'] = np.log(data['close'] / data['close'].shift())
        data['trade_date']=data['trade_time'].astype(str).str[:10]

        #已实现波动率
        RV_s=[]
        for date in data['trade_date'].unique():
            data_date=data[data['trade_date']==date].dropna()
            RV_s.append([date,np.sqrt(sum(data_date['r']**2))])
        RV_s=pd.DataFrame(RV_s,columns=['trade_date','RV'])

        #计算历史VV
        window=20
        VV_s=[]
        for i in RV_s.index[window:]:
            try:
                RV_window=RV_s.loc[(i-window):i,'RV']

                mean_Vol = RV_window.mean()

                vol_of_vol = np.sqrt(sum((RV_window - mean_Vol) ** 2) / window) / mean_Vol
                VV_s.append([RV_s.loc[i,'trade_date'],vol_of_vol])

            except:
                continue

        VV_s = pd.DataFrame(VV_s, columns=['trade_date', 'PVV'])
        VV_s=pd.merge(VV_s,RV_s,on=['trade_date'])

        if path_save:
            VV_s.to_csv(PATH_P_VV_2,encoding='utf_8_sig',index=False)


    #参考 Implied volatility information of Chinese SSE 50 ETF options.pdf
    elif type==3:
        data = pd.read_csv(PATH_50ETF_1MIN)
        data = data[data['trade_time'] >= '2023-02-01 00:00:00'].reset_index()

        data['r']=np.log(data['close']/data['close'].shift())
        #计算5分钟已实现波动率
        N=5
        length=15
        realized_Vol=[]
        for i in range(length-1,len(data)):
            vol=np.sqrt((data.loc[(i-length-1):i,'r']**2).sum()/length*N)
            realized_Vol.append([data.loc[i,'trade_time'],vol])
            print(f'计算已实现波动率完成{data.loc[i,"trade_time"]}')
        realized_Vol=pd.DataFrame(realized_Vol,columns=['trade_time','vol'])

        #筛选出来五分钟已实现波动率
        realized_Vol=realized_Vol.loc[realized_Vol['trade_time'].astype(str).str[15]=='5',:]

        #计算日度已实现波动率的波动率
        realized_Vol['trade_date']=realized_Vol['trade_time'].str[:10]
        vol_of_vol_s=[]
        for date in realized_Vol['trade_date'].unique():
            Vol_date = realized_Vol.loc[realized_Vol['trade_date'] == date, 'vol']
            mean_Vol = Vol_date.mean()

            vol_of_vol = np.sqrt(sum((Vol_date - mean_Vol) ** 2) / N) / mean_Vol

            vol_of_vol_s.append([date, vol_of_vol])
        vol_of_vol_s = pd.DataFrame(vol_of_vol_s, columns=['date', 'vol_of_vol'])


        if path_save:
            vol_of_vol_s.to_csv(path_save,encoding='utf_8_sig',index=False)












if __name__=='__main__':
    realized_vol_of_vol(type=3,path_save=PATH_P_VV)































if __name__=='__main__':
    realized_vol_of_vol(path_close_5_min=data_real_path('数据文件/原始数据/ETF50五分钟收盘价.csv'),
                        windows=[1 / 12, 2 / 12, 3 / 12, 6 / 12, 1],
                        path_save=data_real_path('数据文件/生成数据')+'/已实现vol_of_vol.csv'
                        )









