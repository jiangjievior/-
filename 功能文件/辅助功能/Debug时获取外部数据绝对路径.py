#由于Debug时，模块内文件无法读取外部目录数据，此函数可以帮助获取外部目录数据的绝对路径
import os


#从目标数据所在相对路径寻找目标数据所在绝对路径
def data_real_path(path_data:str# 目标数据所在相对路径
                   )->str:#目标数据所在绝对路径

    path_now=os.path.realpath('.')#当前工作绝对路径
    path_data_high_most=path_data.split('/')[0]#目标数据所在相对路径最顶层路径

    paths_high=path_now.split('\\')

    #从当前工作目录出发，逐层搜索目标数据顶层目录
    list_path_rev=list(range(len(paths_high) + 1))[::-1]
    for i in list_path_rev:
        path_high='/'.join(paths_high[:i])
        files_high=os.listdir(path_high)
        if path_data_high_most in files_high:
            path_high_ = '/'.join(paths_high[:i])
            path_data_real=f"{path_high_}/{path_data}"

            if not os.path.exists(path_data_real):
                continue
            else:
                break

    return path_data_real

if __name__=='__main__':
    import pandas as pd
    # path_data = "功能文件/生成数据_功能文件/测试.csv"  # 目标数据所在相对路径
    # path_data_real=data_real_path(path_data)
    # pd.DataFrame([1,2,3,4,5]).to_csv(path_data_real)


    #读取外部数据测试
    # data_path=data_real_path(path_data="项目文件/将五个CSV文件合为一个.py")
    # data=pd.read_csv(data_path)
    # data
    #
    #为了保存，需要指定尚不存在的文件路径
    data_path = data_real_path(path_data="项目文件/路径测试.csv")


























