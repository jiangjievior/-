import pandas as pd
import numpy as np

#logistic算法
from sklearn.linear_model import LogisticRegression


#计算logit模型中，
def probability_logit(X,Y):
    X=np.array(X).reshape(len(X),1)
    Y=np.array(Y).reshape(1,len(X))[0]

    #训练模型
    #设置最大迭代次数为3000，默认为1000.不更改会出现警告提示
    log_reg = LogisticRegression(max_iter=3000)
    #给模型喂入数据
    clm=log_reg.fit(X,Y)

    probality_Y=clm.predict_proba(X)

    #利用反推方式计算拟合系数


    return params,pd.DataFrame(probality_Y).loc[:,1]



if __name__=='__main__':

    X=pd.DataFrame(np.random.random(100))
    Y=pd.DataFrame(np.array([1 if i > 0.5 else 0 for i in X.values]))
    probality_Y=probability_logit(X,Y)















