import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
from 数据文件.基本参数 import *
import torch
from torch import nn
from torch.autograd import Variable


class lstm(nn.Module):
    def __init__(self, input_size=1, hidden_size=4, output_size=1, num_layer=2):
        super(lstm, self).__init__()
        self.layer1 = nn.LSTM(input_size, hidden_size, num_layer)
        self.layer2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x, _ = self.layer1(x)
        s, b, h = x.size()
        x = x.view(s * b, h)
        x = self.layer2(x)
        x = x.view(s, b, -1)
        return x


def create_dataset(dataset, look_back=2):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)


def LSTM(
        cycle_index,
        data,#数据
        times_train=300,
        look_back=2,#数据滞后期数:解释变量与被解释变量之间的距离期数
        size_train=0.7,#训练集数据所占比例
        input_size=1,#输入维度，训练数据维度
        hidden_size=4, #隐藏层维度
        output_size=1, #输出维度，拟合数据维度
        num_layer=2,#层数
        path_save_train='',#训练过程路径
        path_save_train_fig='',#训练过程图片保存路径
        path_save_predict='',#预测数据保存路径
        path_save_predict_fig='',#预测数据结果绘图保存路径


):
    # 数据预处理
    data = data.dropna()  # 滤除缺失数据
    dataset = data.values  # 获得csv的值
    dataset = dataset.astype('float32')
    max_value = np.max(dataset)  # 获得最大值
    min_value = np.min(dataset)  # 获得最小值
    scalar = max_value - min_value  # 获得间隔数量
    dataset = list(map(lambda x: x / scalar, dataset))  # 归一化

    # 创建好输入输出
    data_X, data_Y = create_dataset(dataset,look_back=look_back)

    # 划分训练集和测试集，70% 作为训练集
    train_size = int(len(data_X) * size_train)
    test_size = len(data_X) - train_size
    train_X = data_X[:train_size]
    train_Y = data_Y[:train_size]
    test_X = data_X[train_size:]
    test_Y = data_Y[train_size:]

    train_X = train_X.reshape(-1, 1, 2)
    train_Y = train_Y.reshape(-1, 1, 1)
    test_X = test_X.reshape(-1, 1, 2)

    train_x = torch.from_numpy(train_X)
    train_y = torch.from_numpy(train_Y)
    test_x = torch.from_numpy(test_X)

    model = lstm(2, 4, 1, 2)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

    # 开始训练
    results_train=[]
    for e in range(times_train):
        var_x = Variable(train_x)
        #var_x=Variable(test_x)
        var_y = Variable(train_y)
        # 前向传播
        out = model(var_x)
        loss = criterion(out, var_y)
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print('第{}次拟合,Epoch: {}, Loss: {:.5f}'.format(cycle_index,e + 1, loss.item()))
        results_train.append([e,loss.item()])

    model = model.eval()  # 转换成测试模式

    data_X_ = data_X.reshape(-1, 1, 2)
    data_X_ = torch.from_numpy(data_X_)
    var_data = Variable(data_X_)
    pred_test = model(var_data)  # 测试集的预测结果


    return float(pred_test[-1][0][0])*scalar



def run_Lstm(data,path_base,col,times_train,futures):

    for cycle_index in range(1, futures+1):
        y_new = LSTM(
            cycle_index=cycle_index,
            data=data,  # 数据
            look_back=2,  # 数据滞后期数:解释变量与被解释变量之间的距离期数
            input_size=1,  # 输入维度，训练数据维度
            hidden_size=4,  # 隐藏层维度
            output_size=1,  # 输出维度，拟合数据维度
            num_layer=2,  # 层数
            times_train=times_train,  # 训练次数
            path_save_train=os.path.join(path_base, f'{col}训练过程.xlsx'),  # 训练过程路径
            path_save_train_fig=os.path.join(path_base, f'{col}训练误差下降图.png'),  # 训练过程图片保存路径
            path_save_predict='',  # 预测数据保存路径
            path_save_predict_fig='',  # 预测数据结果绘图保存路径

        )
        Consume_T = data.T
        Consume_T[f'{data.index[-1][:-1]}{int(data.index[-1][-1]) + 1}'] = y_new
        data = Consume_T.T
        data.to_excel(os.path.join(path_base,f'{col}预测结果.xlsx'))




if __name__=='__main__':
    PREMIUM=pd.read_csv(PATH_INDEPENDENT_VV_PREMIUM_SERIES,index_col=0)
    PREMIUM.index
    path_base = 'E:\python_project\金融数学比赛\数据文件\生成数据\题目2'
    run_Lstm(PREMIUM, path_base, col=0, times_train=300, futures=60)




pass








