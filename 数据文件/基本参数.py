from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
import pandas as pd

#原始数据路径
PATH_PARAMETERS=data_real_path('数据文件/原始数据/个股期权合约定价重要参数表20230328/SO_PricingParameter.csv')
PATH_BASIC=data_real_path('数据文件/原始数据/个股期权合约日交易基础表20230328/SO_QuotationBas.csv')
PATH_DERIVE=data_real_path('数据文件/原始数据/个股期权合约日交易衍生表20230328/SO_QuotationDer.csv')

PATH_50ETF_5MIN=data_real_path('数据文件/原始数据/50ETF五分钟收盘价.csv')
PATH_50ETF_1MIN=data_real_path('数据文件/原始数据/50ETF一分钟收盘价.csv')
PATH_50ETF_FUTURE=data_real_path('数据文件/原始数据/股指期货日交易数据225129281/FFUT_FDT.csv')
PATH_50ETF=data_real_path('数据文件/原始数据/50ETF日度收盘价.csv')

#生成数据路径
PATH_50ETF_OPTION=data_real_path('数据文件/生成数据')+'/上证50ETF期权数据.csv'
PATH_IV_SURFACE_SERIES=data_real_path('数据文件/生成数据') + '/隐含波动率曲面时间序列.csv'
PATH_RV=data_real_path('数据文件/生成数据') + '/已实现波动率.csv'
PATH_Q_VV=data_real_path('数据文件/生成数据') + '/隐含vol_of_vol.csv'
PATH_P_VV=data_real_path('数据文件/生成数据') + '/已实现vol_of_vol.csv'



#交易日窗口长度，基于中国期权上证50ETF
DAYS_OF_YEAR=242#一年中交易日个数，参考陈蓉（2019）《波动率风险和波动率风险溢酬_中国的独特现象》 脚注9
DAYS_OF_MONTH=20#一个月中交易日个数，参考陈蓉（2019）《波动率风险和波动率风险溢酬_中国的独特现象》 脚注9
WINDOWS_MONTH=[1,2,3,6,12]#常需考察的期权剩余到期月数，参考 Carr and Wu(2020)《Option Profit and Loss Attribution and Pricing: A New Framework》 P2286
WINDOWS_DAYS=[x*DAYS_OF_MONTH for x in WINDOWS_MONTH]#常需考察的期权剩余到期天数
WINDOWS_YEARS=[X/DAYS_OF_YEAR for X in WINDOWS_DAYS]#常需考察的期权剩余到期年数


#自然日窗口长度
DAYS_OF_YEAR_NATURAL=365#一年中自然日个数
DAYS_OF_MONTH_NATURAL=30#一个月中自然日个数
WINDOWS_MONTH=[1,2,3,6,12]#常需考察的期权剩余到期月数，参考 Carr and Wu(2020)《Option Profit and Loss Attribution and Pricing: A New Framework》 P2286
WINDOWS_DAYS_NATURAL=[x*DAYS_OF_MONTH_NATURAL for x in WINDOWS_MONTH]#常需考察的期权剩余到期天数
WINDOWS_YEARS_NATURAL=[X/DAYS_OF_YEAR_NATURAL for X in WINDOWS_DAYS_NATURAL]#常需考察的期权剩余到期年数


PATH_P_VV_2=data_real_path('数据文件/生成数据') + '/已实现vol_of_vol_2.csv'
PATH_P_VV_3=data_real_path('数据文件/生成数据') + '/已实现vol_of_vol_3.csv'

PATH_GAINS_DELTA_NEUTRAL_ChenRong2011=data_real_path('数据文件/生成数据') + '/陈蓉2011delta中性收益率.csv'


# 数据列标题
class Columns():
    SecurityID = 'SecurityID'
    Symbol = 'Symbol'
    ExchangeCode = 'ExchangeCode'
    ContractCode = 'ContractCode'
    ShortName = 'ShortName'
    CallOrPut = 'CallOrPut'
    StrikePrice = 'StrikePrice'
    ExerciseDate = 'ExerciseDate'
    TradingDate = 'TradingDate'
    ClosePrice = 'ClosePrice'
    UnderlyingScrtClose = 'UnderlyingScrtClose'
    RemainingTerm = 'RemainingTerm'
    RisklessRate = 'RisklessRate'
    HistoricalVolatility = 'HistoricalVolatility'
    ImpliedVolatility = 'ImpliedVolatility'
    TheoreticalPrice = 'TheoreticalPrice'
    Delta = 'Delta'
    Gamma = 'Gamma'
    Vega = 'Vega'
    Theta = 'Theta'
    Rho = 'Rho'
    SettlePrice = 'SettlePrice'
    Volume = 'Volume'
    Position = 'Position'
    Amount = 'Amount'
    Gains = 'gains'
    delta_bin = 'delta_bin'
    Gains_to_option = 'gains/O'  # 收益/期权价格
    Gains_to_underlying = 'gains/S'  # 收益/标的价格
    RV = 'RV'
    KF='K/F'#在值程度：执行价格/远期价格，参考陈蓉(2010)《隐含波动率曲面_建模与实证_陈蓉》.P144
    KF_bin='K/F_bin'
    KF_minus_1 = 'K/F-1'
    KF_minus_1_bin = 'K/F-1_bin'


C= Columns()

#建立隐含波动率曲面时间序列
MONEYNESS_KF=[0.95,0.97,1,1.03,1.05]#在值程度，用于建立隐含波动率曲面底盘，参考陈蓉（2010）《隐含波动率曲面_建模与实证_陈蓉》




#拟合delta中性收益与风险的时间序列关系
COL_IV=[f'IV{x}' for x in WINDOWS_DAYS_NATURAL]
COL_QVV=[f'QVV{x}' for x in WINDOWS_DAYS_NATURAL]
PATH_GAINS_OLS_RV_and_QVV=data_real_path('数据文件/生成数据') + '/GAINS_OLS_RV_and_QVV回归结果.csv'
PATH_GAINS_OLS_IV_and_QVV=data_real_path('数据文件/生成数据') + '/GAINS_OLS_IV_and_QVV回归结果.csv'
PATH_Moneyness_GAINS_OLS_IV_and_QVV=data_real_path('数据文件/生成数据') + '/基于不同在值程度的GAINS_OLS_IV_and_QVV回归结果.csv'
MONEYNESS_BIN=pd.IntervalIndex.from_tuples([(-0.03, 0.03), (0.03, 0.1), (-0.1, -0.03)])




