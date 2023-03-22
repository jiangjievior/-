import pandas as pd
import numpy as np
import statsmodels.api as sm
from typing import Union,List
import copy

def OLS_model(X:pd.DataFrame,#解释变量
              Y:pd.DataFrame,#被解释变量
              const=True,#添加常数项
              summary:bool=False,#将结果输出为表格
              title_params:List[str]=None#系数名称
              )->Union[float,list]:

    if const:
        X = sm.add_constant(X)#添加常数项
        if summary:
            title_params_=copy.deepcopy(title_params)
            title_params_=['const']+list(title_params_)

    model = sm.OLS(Y, X).fit()#模型拟合

    params = list(model.params)  # 系数
    tvalues = list(model.tvalues)  # 系数t值
    pvalues = list(model.pvalues)  # 系数p值
    resid = list(model.resid)  # 残差序列
    F=model.fvalue  # F值
    p_F=model.f_pvalue  # F检验P值
    R_2=model.rsquared_adj#调整后拟合优度
    AIC=model.aic
    BIC=model.bic
    if summary:
        # 将结果输出为表格形式
        result=pd.DataFrame({
                                '系数':params,
                                '系数t值':tvalues,
                                '系数p值':pvalues,
                            },index=title_params_)
        result['AIC']=AIC
        result['BIC']=BIC
        result['调整后R方']=R_2

        return model,result,resid



    else:
        return model,params,tvalues,pvalues,resid,F,p_F,R_2


if __name__=='__main__':
    #1.回归
    data = pd.DataFrame(# 创建数据
        {'Y': np.random.normal(0, 1, 30), 'X1': -3 * np.random.normal(0, 1, 30), 'X2': 5 * np.random.normal(0, 1, 30)})
    X = data[['X1', 'X2']]  # 解释变量
    Y=data['Y']#被解释变量

    model,params, tvalues, pvalues, resid, F, p_F, R_2=OLS_model(X,Y)
    model, params, tvalues, pvalues, resid, F, p_F, R_2


    #2.回归并展示表格结果
    data = pd.DataFrame(# 创建数据
        {'Y': np.random.normal(0, 1, 30), 'X1': -3 * np.random.normal(0, 1, 30), 'X2': 5 * np.random.normal(0, 1, 30)})
    X = data[['X1', 'X2']]  # 解释变量
    Y = data['Y']  # 被解释变量

    model,result,resid = OLS_model(X, Y,summary=True,title_params=['X1','X2'])
    model,result,resid









































