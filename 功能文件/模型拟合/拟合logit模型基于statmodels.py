import pandas as pd
import numpy as np
import statsmodels.api as sm

X=pd.DataFrame(np.random.random(100))
data=pd.DataFrame(
    {
        'y':[1 if i > 0.5 else 0 for i in X[0].tolist()],
        'x':X[0].tolist()
    }
)


#实例化对象
logit = sm.Logit(data['y'], data['x'])

# 拟合模型
result = logit.fit()
#查看模型结果
print(result.summary())
result.predict(data['x'])
logit.pdf(data['x'])

param=result.params[0]#系数
probability_Y=[]
for x in data['x']:
    probability_Y.append(np.exp(param*x)/(1+np.exp(param*x)))
























