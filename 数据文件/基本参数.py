from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path

PATH_PARAMETERS=data_real_path('数据文件/原始数据/个股期权合约定价重要参数表20230328/SO_PricingParameter.csv')
PATH_BASIC=data_real_path('数据文件/原始数据/个股期权合约日交易基础表20230328/SO_QuotationBas.csv')
PATH_DERIVE=data_real_path('数据文件/原始数据/个股期权合约日交易衍生表20230328/SO_QuotationDer.csv')


PATH_50ETF_OPTION=data_real_path('数据文件/生成数据')+'/上证50ETF期权数据.csv'
PATH_IV_SURFACE_SERIES=data_real_path('数据文件/生成数据') + '/隐含波动率曲面时间序列.csv'
PATH_Q_VV=data_real_path('数据文件/生成数据') + '/隐含vol_of_vol.csv'
PATH_P_VV=data_real_path('数据文件/生成数据') + '/已实现vol_of_vol.csv'

PATH_50ETF_5MIN=data_real_path('数据文件/原始数据/ETF50五分钟收盘价.csv')
PATH_50ETF_FUTURE=data_real_path('数据文件/原始数据/股指期货日交易数据225129281/FFUT_FDT.csv')
PATH_50ETF=data_real_path('数据文件/原始数据/50ETF日度收盘价.csv')

#窗口长度
WINDOWS_DAYS=[30,60,91,182,365]
WINDOWS_MONTH=[1,2,3,6,12]
WINDOWS_YEARS=[X/365 for X in WINDOWS_DAYS]


PATH_P_VV_2=data_real_path('数据文件/生成数据') + '/已实现vol_of_vol_2.csv'



















