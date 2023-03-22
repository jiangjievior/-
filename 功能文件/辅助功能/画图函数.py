import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import numpy as np
import pandas as pd
import time
plt.rcParams['font.sans-serif']=['simhei']#用于正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用于正常显示负号
from matplotlib import cm#必须从matplotlib中引入cm模块！！
from mpl_toolkits.mplot3d import axes3d
from matplotlib.ticker import LinearLocator,FormatStrFormatter#用于修改坐标轴刻度和数值精确程度

def scatter_3D(x,y,z,x_label=None,y_label=None,z_label=None):
    """绘制3D散点图
    :param x: iterable
    :param y: iterable
    :param z: iterable
    :param x_label: str，默认None
    :param y_label: str，默认None
    :param z_label: str，默认None
    :return:
    """
    fig = plt.figure(figsize=(12, 16))#创建图形
    ax = fig.gca(projection='3d')  # 设置3D坐标轴
    ax.scatter(xs=x, ys=y, zs=z,alpha=0.5)#绘制立体空间的散点图

    # 设置坐标轴名称
    ax.set_xlabel(x_label,fontsize=15)
    ax.set_ylabel(y_label,fontsize=15)
    ax.set_zlabel(z_label,fontsize=15)

if __name__=='__main__':
    x=np.random.randint(-8,9,100)
    y=np.random.randint(-8,9,100)
    z=np.random.randint(-8,9,100)
    scatter_3D(x, y, z, x_label='X', y_label='Y', z_label='Z')

"""__________________________________________________________________________________________________________________"""

def surface_3D(data,x_label=None,y_label=None,z_label=None,save_path=None,title=None,show=True):
    """绘制3D曲面图，index为x轴，columns为y轴，values为值
    :param data: DataFrame,生成数据，形式如下：
              -5        -4        -3        -2        -1         0
        -2 -0.042076 -0.145171 -0.792229  0.072678 -1.101506  0.210750
        -1 -2.692069  0.813905  0.534286 -0.256929  1.052895  0.537422
         0  0.434038  0.812364 -1.436421 -0.253588  0.058284 -0.747602
         1  0.151999  0.359527  0.493514 -1.611401 -0.653824 -0.428120
         2  0.966574 -0.938842  0.396577  1.358047 -0.882322  0.007148
    :param x_label: str，默认None
    :param y_label: str，默认None
    :param z_label: str，默认None
    :param save_path: str，图片保存路径，默认None
    :param text: str，显示备注，备注内容
    :return:
    """
    #设置不显示图片
    if -show:
        import matplotlib
        matplotlib.use('Agg')

    x=data.index
    y=data.columns
    x,y=np.meshgrid(x,y)
    x=x.T;y=y.T
    z=np.array(data)

    fig = plt.figure(figsize=(12, 16))#创建图形
    ax = fig.gca(projection='3d')  # 设置3D坐标轴
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.4,
                           label='曲面图')  # cmap=cm.coolwarm为图形表面设置皮肤,help(cm)可以查看更多中类型皮肤
    #fig.colorbar(surf, shrink=0.6, aspect=8)  # # shrink控制标签长度，aspect仅对bar的宽度有影响，aspect值越大，bar越窄

    # 设置坐标轴名称
    ax.set_xlabel(x_label,fontsize=25)
    ax.set_ylabel(y_label,fontsize=25)
    ax.set_zlabel(z_label,fontsize=25)
    ax.view_init(azim=20)  # 调整坐标轴的刚打开图片时的初始显示角度，仰角和方位角。可以用于保存图片


    plt.title(title,fontsize=25)

    if save_path is not None:
        plt.savefig(save_path)


if __name__=='__main__':
    data=pd.DataFrame(np.random.randn(5,6),index=np.arange(-2,3),columns=np.arange(-5,1))
    surface_3D(data,title='图片')

"""__________________________________________________________________________________________________________________"""

def scatter_surface(data_init,data_fit,
                    x_label=None,y_label=None,z_label=None,
                    x_name=None,y_name=None,z_name=None,
                    save_path=None):
    """专门用于观察隐含波动率拟合曲面与隐含波动率样本值的贴合情况，样本值为散点，拟合曲面为曲面
    :param data_init: DataFrame,隐含波动率样本值，散乱分布的样本点，至少包括以下列：
                  m     times   implied
        39363 -0.173554  0.031746  0.453126
        39364 -0.153473  0.031746  0.414063
        39365 -0.133851  0.031746  0.367188
        39366 -0.113913  0.031746  0.343751
        39367 -0.021008  0.031746  0.285157
    :param data_fit: DataFrame,拟合好的隐含波动率曲面，index表示m，columns表示剩余到期时间，values为隐含波动率估计值
    :param x_label: str，默认None
    :param y_label: str，默认None
    :param z_label: str，默认None
    :param x_name: str，x轴名称,默None
    :param y_name: str，y轴名称,默认None
    :param z_name: str，z轴名称,默认None
    :param save_path: str，图片保存路径，默认None
    :return:
    """
    fig = plt.figure(figsize=(12, 16))  # 创建图形
    ax = fig.gca(projection='3d')  # 设置3D坐标轴
    ax.scatter(xs=data_init[x_label], ys=data_init[y_label], zs=data_init[z_label], alpha=0.5)  # 绘制立体空间的散点图


    x = data_fit.index
    y = data_fit.columns
    x, y = np.meshgrid(x, y)
    x = x.T;y = y.T
    z = np.array(data_fit)

    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, alpha=0.4,
                           label='曲面图')  # cmap=cm.coolwarm为图形表面设置皮肤,help(cm)可以查看更多中类型皮肤
    #fig.colorbar(surf, shrink=0.6, aspect=8)  # # shrink控制标签长度，aspect仅对bar的宽度有影响，aspect值越大，bar越窄

    # 设置坐标轴名称
    ax.set_xlabel(x_label if x_name is None else x_name, fontsize=15)
    ax.set_ylabel(y_label if y_name is None else y_name, fontsize=15)
    ax.set_zlabel(z_label if z_name is None else z_name, fontsize=15)

    if save_path is not None:
        plt.savefig(save_path)

"""__________________________________________________________________________________________________________________"""
#绘图函数
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.rcParams['font.sans-serif']=['simhei']#用于正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用于正常显示负号

def plot_cols(data,xlabel=None,ylabel=None,path_file=None,marker=True,len_xticks=10,save=False):
    """
    :param data:DataFrame,数据表格--行标题为横坐标，列标题为数据列
                Series,序列——行标题为横坐标，name为数据列
    :param xlabel: str,横坐标名称
    :param ylabel: str,纵坐标名称
    :param path_file: str,保存文件路径
    :param marker: bool,是否为每条线添加不同的标记
    :param len_xticks:int,横坐标显示的值个数
    :param save: bool,是否保存图片
    example:
        data=pd.DataFrame(np.random.random((100,3)),index=np.arange(100),columns=['a','b','c'])
        plot_cols(data,xlabel='指标',ylabel='指数')
    """
    data.index=data.index.astype(str)
    plt.figure(figsize=(12,8))
    markers=['.',',','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']#标记符号

    #如果是DataFrame表格形式，则画出多列；如果是Series，则画出单列
    if type(data) is pd.core.frame.DataFrame:
        #是否为每条线添加不同的符号
        if marker==False:
            for col in data.columns:
                plt.plot(data[col],marker='o',label=col)
        else:
            for col,marker_ in zip(data.columns,markers):
                plt.plot(data[col], marker=marker_, label=col)

    elif type(data) is pd.core.series.Series:
        plt.plot(data, marker='o', label=data.name)

    plt.legend(loc='best',fontsize='small')
    xticks=np.linspace(0,len(data),(len_xticks+1)).astype(int).tolist()[:-1]#被显示的横坐标刻度值的位置
    plt.xticks(data.index[xticks],rotation=270)
    plt.ylabel(ylabel,fontsize=15)
    plt.xlabel(xlabel,fontsize=15)
    plt.grid(True,alpha=0.2)
    if save is not True:plt.savefig(path_file)

if __name__=='__main__':
    data = pd.DataFrame(np.random.random((100, 3)), index=np.arange(100), columns=['a', 'b', 'c'])
    plot_cols(data, xlabel='指标', ylabel='指数')



def plot_twins(data,col1,col2,xlabel=None,ylabel1=None,ylabel2=None,len_xticks=10,figsize=(10,6),save_path=None):
    """将含有两列的DataFrame表格数据作为双轴图
    :param data: DataFrame,含有两列的DataFrame表格数据
    :param col1: str,左图列标题
    :param col2: str,右图列标题
    :param xlabel: str,横轴标题
    :param ylabel1: str,左y轴标题
    :param ylabel2: str,右y轴标题
    :param len_xticks: int,显示的刻度个数
    :param figsize: turple,图大小
    :param save_path: str,图片保存路径。默认为None，不保存图片
    :return:
    example:
        x=np.arange(0,100)
        data=pd.DataFrame({'销售额(元)':3*x+np.random.random(100)*100,'增长率(%)':np.random.random(100)},index=pd.date_range('2015-01-23',periods=100,freq='D'))
        plot_twins(data,col1='销售额(元)',col2='增长率(%)',xlabel=None,ylabel1='销售额(元)',ylabel2='增长率(%)')
    """
    if xlabel in data.columns:data.index = data[xlabel].astype(str)
    else:data.index = data.index.astype(str)
    fig=plt.figure(figsize=figsize)#创建一块总画布
    # 将画板分为四行四列共16个单元格，(0, 0)表示从第一行第一列即第一个单元格开始画图，将第一行的三个单元格作为一个画块作画
    ax=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)

    plt.plot(data[col1],label=col1,color='r',marker='^')
    ax.legend(loc='upper right')#用于显示画布ax的图，切记用 loc= 表示位置
    ax.set_ylabel(ylabel1,fontsize=15)
    xticks=np.linspace(0,len(data),(len_xticks+1)).astype(int).tolist()[:-1]#被显示的横坐标刻度值的位置
    ax.set_xticks(data.index[xticks])
    plt.xticks(rotation=270)

    twin=ax.twinx()
    plt.plot(data[col2],label=col2,color='y',marker='o')
    twin.legend(loc='upper left')
    twin.set_ylabel(ylabel2,fontsize=15)
    ax.set_xlabel(xlabel,fontsize=15)
    ax.set_xticks(data.index[xticks])
    ax.grid(True,alpha=0.2)
    if save_path!=None: plt.savefig(save_path)

def plot_figs(data,xlabel=None,ylabels=None,save_path=None,len_xticks=5,length=10,width=3,intervals=1):
    """
    将DataFrame表格中的多列数据绘制成多个图
    :param data:DataFrame,含有多列的表格
    :param xlabel:str,横轴标题
    :param ylabels:list,各个图的纵轴标题
    :param path_save:str,图片保存路径。默认为None，不保存图片
    :param len_xticks: int,显示的刻度个数
    :param length:int,画板长度
    :param width:int,图画宽度
    :param intervals:int,图画之间间隔距离
    :return:
    example:
        data=pd.DataFrame(np.random.random((100,3)),index=np.arange(100),columns=['a','b','c'])
        plot_figs(data,xlabel='标号',ylabels=['a','b','c'])
    """

    cols=data.columns
    num_fig = len(data.columns)
    fig = plt.figure(figsize=(length, 4*num_fig))  # 创建一块总画布
    for i in range(0,num_fig):
        #i=2

        ax = plt.subplot2grid((num_fig*(width+intervals), 1), (i*(width+intervals), 0), rowspan=width,
                               colspan=1)  # 将画板分为四行四列共16个单元格，(0, 0)表示从第一行第一列即第一个单元格开始画图，将第一行的三个单元格作为一个画块作画

        ax.plot(data[cols[i]], label=cols[i])
        ax.legend(loc='upper right')  # 用于显示画布ax1的图，切记用 loc= 表示位置
        if ylabels!=None:ax.set_ylabel(ylabels[i])
        if xlabel!=None and i==(num_fig-1):ax.set_xlabel(xlabel)
        xticks = np.linspace(0, len(data), (len_xticks + 1)).astype(int).tolist()[:-1]  # 被显示的横坐标刻度值的位置
        ax.set_xticks(data.index[xticks])
        plt.grid(True,alpha=0.2)
    if save_path != None: plt.savefig(save_path)

def scatter_cols(data,xlabel=None,ylabel=None,path_file=None,marker=True,len_xticks=10,save=False):
    """
    :param data:DataFrame,数据表格--行标题为横坐标，列标题为数据列
                Series,序列——行标题为横坐标，name为数据列
    :param xlabel: str,横坐标名称
    :param ylabel: str,纵坐标名称
    :param path_file: str,保存文件路径
    :param marker: bool,是否为每条线添加不同的标记
    :param len_xticks:int,横坐标显示的值个数
    :param save: bool,是否保存图片
    example:
        data=pd.DataFrame(np.random.random((100,3)),index=np.arange(100),columns=['a','b','c'])
        plot_cols(data,xlabel='指标',ylabel='指数')
    """
    data.index=data.index.astype(str)
    plt.figure(figsize=(12,8))
    markers=['.',',','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']#标记符号

    #如果是DataFrame表格形式，则画出多列；如果是Series，则画出单列
    if type(data) is pd.core.frame.DataFrame:
        #是否为每条线添加不同的符号
        if marker==False:
            for col in data.columns:
                plt.scatter(data.index,data[col],marker='o',label=col)
        else:
            for col,marker_ in zip(data.columns,markers):
                plt.scatter(data.index,data[col], marker=marker_, label=col)

    elif type(data) is pd.core.series.Series:
        plt.scatter(data.index,data, marker='o', label=data.name)

    plt.legend(loc='best',fontsize='small')
    xticks=np.linspace(0,len(data),(len_xticks+1)).astype(int).tolist()[:-1]#被显示的横坐标刻度值的位置
    plt.xticks(data.index[xticks],rotation=270)
    plt.ylabel(ylabel,fontsize=15)
    plt.xlabel(xlabel,fontsize=15)
    plt.grid(True,alpha=0.2)
    if save==True:plt.savefig(path_file)































