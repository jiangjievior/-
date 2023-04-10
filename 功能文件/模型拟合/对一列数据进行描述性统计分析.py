import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

from 功能文件.模型拟合.计算一列数据的t检验统计结果 import t_test


def describe(data):
    mean=round(np.mean(data),3)
    median=round(np.median(data),3)
    skew=round(pd.DataFrame(data).skew(),3)[0]
    kurt = round(pd.DataFrame(data).kurt(), 3)[0]
    std = round(np.std(data), 3)
    min_=round(np.min(data), 3)
    max_ = round(np.max(data), 3)

    # 进行非零t检验，***表示数据显著非零
    t, p, star = t_test(np.array(data))

    data=pd.DataFrame(data)
    #小于零的数所占百分比
    percent_negative=f'{round(sum(data<0)/len(data)*100,2)}%'
    # 小于零的数所占百分比
    percent_positive = f'{round(sum(data > 0) / len(data) * 100, 2)}%'
    #计算AR(1)系数
    model = ARIMA(data, order=(1, 0, 0)).fit()
    AR1 = model.params['ar.L1']  # 系数



    return [mean,median,skew,kurt,std,min_,max_,percent_negative,percent_positive,AR1,t,p,star], \
           ['mean', 'median', 'skew', 'kurt', 'std', 'min', 'max', '%<0', '%>0', "AR(1)", 't', 'p', 'star']



if __name__=='__main__':
    data=np.random.normal(loc=4,size=2000)
    values,cols=describe(data.tolist())
    mean, median, skew, kurt, std, min_, max_, percent_negative, percent_positive, AR1, t, p, star=values
