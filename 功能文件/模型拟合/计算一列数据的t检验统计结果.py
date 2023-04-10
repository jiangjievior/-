import numpy as np
import pandas as pd

import scipy.stats as stats

def t_test(x):

    t=x.mean()/(x.std()/(np.sqrt(len(x))))
    if t>0:
       p=(1-stats.t.cdf(t,df=len(x)))*2
    else:
        p = stats.t.cdf(t, df=len(x))*2


    if p<=0.01:
        star='***'
    elif p<0.05:
        star='**'
    elif p<=0.1:
        star='*'
    else:
        star=''

    return t,p,star



if __name__=='__main__':
    x=np.random.normal(loc=4,size=2000)
    t,p,star=t_test(x)




















