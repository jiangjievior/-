# -*- coding:utf-8 -*-
from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

from 项目文件.拟合delta中性收益与风险的时间序列关系_新版 import SeriesOlsGainsAndRisk
#model,result,resid = OLS_model(X, Y





if __name__=='__main__':
    SOGAR=SeriesOlsGainsAndRisk()
    SOGAR
    SOGAR.gains_pivot['RV(-1)']=SOGAR.gains_pivot['RV'].shift(1)
    SOGAR.gains_pivot[[f'{x}(-1)' for x in COL_IV]] = SOGAR.gains_pivot[COL_IV].shift(1)
    SOGAR.gains_pivot[[f'{x}(-1)' for x in COL_QVV]]=SOGAR.gains_pivot[COL_QVV].shift(1)
    SOGAR.gains_pivot.dropna(inplace=True)



    #观察IV=QVV+IV(-1)
    results=[]
    for days in WINDOWS_DAYS_NATURAL:

        X=SOGAR.gains_pivot[[f'QVV{days}',f'IV{days}(-1)']]
        Y=SOGAR.gains_pivot[f'IV{days}']

        model,params,tvalues,pvalues,resid,F,p_F,R_2 = OLS_model(X, Y)

    # 观察QVV=IV+QVV(-1)
    results = []
    for days in WINDOWS_DAYS_NATURAL:
        X = SOGAR.gains_pivot[[f'IV{days}', f'QVV{days}(-1)']]
        Y = SOGAR.gains_pivot[f'QVV{days}']

        model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X, Y)































































