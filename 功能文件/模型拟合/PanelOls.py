import statsmodels.api as sm # 回归
import statsmodels.formula.api as smf # 回归
from linearmodels.panel import PanelOLS # 面板回归
import pandas as pd
import numpy as np


# 定义时间轴和个体轴/
date=list(range(70))#时间范围
indvidula=list(range(40))#个体范围
col_indvidual = 'indvidual'#个体轴名称
col_date = 'date'#时间轴名称


#生成数据
data=[]
for date_ in date:
    for indvidula_ in indvidula:
        X1=np.random.normal()
        X2 = np.random.normal()
        X3 = np.random.normal()
        Y=-2*indvidula_-np.random.normal()+3*X1-4*X2+8*X3+date_+np.random.normal()
        data.append([date_,indvidula_,X1,X2,X3,Y])

data=pd.DataFrame(data,columns=['date','indvidual','X1','X2','X3','Y'])


#指定自变量和因变量列标题
col_X = ['X1','X2','X3']
col_Y = 'Y'

# 面板回归之前，需要先设置“个股在外时间在内”的层次化索引
data.set_index([col_indvidual,col_date],inplace = True)


# 指定自变量和因变量
X = sm.add_constant(data[col_X])
Y = data[col_Y]


# 混合回归
model_pooled = PanelOLS(Y, X, entity_effects=False, time_effects=False)
model_pooled = model_pooled.fit()
print(model_pooled)

# 单向固定效应:设置个体固定效应
model_entity = PanelOLS(Y, X, entity_effects=True, time_effects=False)
model_entity = model_entity.fit()
print(model_entity)

# 单向固定效应:设置时间固定效应
model_time = PanelOLS(Y, X, entity_effects=True, time_effects=False)
model_time = model_time.fit()
print(model_time)

# 双向固定效应:设置个体固定效应和时间固定效应
model_twoway = PanelOLS(Y, X, entity_effects=True, time_effects=True)
model_twoway = model_twoway.fit()
print(model_twoway)

params = list(model_twoway.params)  # 系数
tvalues = list(model_twoway.tstats)  # 系数t值
pvalues = list(model_twoway.pvalues)  # 系数p值
