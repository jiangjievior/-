import copy

import Cython.Compiler.TypeSlots
import click.decorators
import commctrl
import pandas as pd
import numpy as np
import os
import datetime,time
import sas7bdat
from sas7bdat import SAS7BDAT
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 项目文件.数据清洗 import get_data
from 数据文件.基本参数 import *





if __name__=='__main__':
    from 项目文件.计算delta中性收益 import DeltaNeutralGains

    DNG = DeltaNeutralGains(path_option=PATH_50ETF_OPTION)
    #DNG.run(path_save=PATH_GAINS_DELTA_NEUTRAL_ChenRong2011)
    #DNG.option = DNG.option[DNG.option[C.Delta].abs() <= 0.5]

    # 计算次日股票价格
    ETF = DNG.option[[DNG.col_TradingDate, DNG.col_UnderlyingScrtClose]].drop_duplicates().sort_values(
        DNG.col_TradingDate)
    ETF['next_Underlying'] = ETF[C.UnderlyingScrtClose] .shift(-1)
    DNG.option = pd.merge(DNG.option, ETF[[DNG.col_TradingDate, 'next_Underlying']], on=[DNG.col_TradingDate])
    #DNG.option=DNG.option[DNG.option[C.KF]]

    gains_to_Maturity=[]
    for ShortName in DNG.option[C.ShortName].unique():
        option=DNG.option[DNG.option[C.ShortName]==ShortName]
        option.sort_values(C.TradingDate,inplace=True)
        gain_option=option[C.ClosePrice].tolist()[-1]-option[C.ClosePrice].tolist()[0]
        gain_Underlying=((option['next_Underlying']-option[C.UnderlyingScrtClose])*option[C.Delta]).sum()
        gain_Cash=sum((option[C.ClosePrice]-option[C.UnderlyingScrtClose]*option[C.Delta])
                      *option[C.RisklessRate]/100*(np.arange(1,len(option)+1)/(len(option))*(len(option)/365)))
        gain=gain_option-gain_Underlying-gain_Cash

        gains_to_Maturity.append([ShortName,option[C.ExerciseDate].tolist()[0],gain])
        print([ShortName,option[C.ExerciseDate].tolist()[0],gain])

        option_main=option[[C.TradingDate,C.ClosePrice,'next_Close',C.UnderlyingScrtClose,'next_Underlying']]

    gains_to_Maturity=pd.DataFrame(gains_to_Maturity,columns=[C.ShortName,C.ExerciseDate,'gain'])
    gains_to_Maturity['gain'].describe()














    pass







































