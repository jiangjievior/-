import pandas as pd
import numpy as np
import re
import os
import copy

# #参考JF2020计算的高斯核函数回归
# def gaussian_kernels_JF2020(X:pd.DataFrame,
#                             Y:pd.DataFrame
#                             ):
#     h_ln=X['years']
#
#
#     #计算每只期权样本权重
#     def weight(x,times,delta):
#
#         w=(1-abs(delta))*np.exp()

#参考JF2020计算的高斯核函数回归
class GaussianKernelsJF2020():

    def __init__(self,
                 data,
                 col_m,
                 col_times,
                 col_delta,
                 col_IV,
                 **kwargs):
        self.data = data
        self.col_m = col_m
        self.col_times = col_times
        self.col_delta = col_delta
        self.col_IV=col_IV
        self.std_m=self.data[self.col_m].std()
        self.std_times = self.data[self.col_times].std()
        self.n=len(self.data)
        self.bandwidths()#计算最优带宽


    #计算最优带宽
    def bandwidths(self):
        self.h_m=(4/(3*self.n))**(1/5)*self.std_m
        self.h_times = (4 / (3 * self.n)) ** (1 / 5) * self.std_times


    #在数据中加入权重
    def weight(self,
               m_target,#目标在值程度
               times_target#目标剩余到期时间
               ):
        self.data['weight']=(1-self.data[self.col_delta].abs())*np.exp(-(self.data[self.col_m]-m_target)**2/(2*self.h_m**2))*np.exp(-(np.log(self.data[self.col_times])-np.log(times_target))**2/(2*self.h_times**2))


    #计算单个样本隐含波动率预测值
    def predict__(self,m_target,times_target):
        self.weight(m_target,times_target)
        IV=(self.data['weight']/self.data['weight'].sum()*self.data[self.col_IV]).sum()

        return IV

    #预测隐含波动率
    def predict(self,X):
        try:
            IV=X.apply(lambda data:self.predict__(m_target=data[self.col_m],times_target=data[self.col_times]),axis=1)
        except:
            IV=np.nan
        return IV

if __name__=='__main__':
    data = pd.read_csv('H:\美国标普500期权\原始数据\标普500期权CSV原始数据(第二次剔除无效数据)\SPX500_5.csv')
    data = data[data['date'] == '2017-01-09']
    X=data[['x','years']]
    GK=GaussianKernelsJF2020(   data,
                                col_m='x',
                                col_times='years',
                                col_delta='Delta',
                                col_IV='IV')

    IV=GK.predict(X)








































