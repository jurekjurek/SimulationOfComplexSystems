import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf  # 通过雅虎财经导入金融数据
import matplotlib.pylab as plt
from scipy.stats import norm  # 导入的一个用于处理连续随机正态分布的模块
import math  # 用于进行指数运算
import seaborn as sns

# 创建时间范围
years = 3
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365 * years)

# 创建证券的Ticker（代码），以便从Yahoo Finance中提取财经数据
# SPY: SPDR S&P 500 ETF Trust标普500
# LQD: iShares iBoxx $ Investment Grade Corporate Bond ETF
# GLD: SPDR Gold Trust
# DBC: Invesco DB Commodity Index Tracking Fund
# FXE: Invesco CurrencyShares Euro Trust
tickers = ['SPY', 'LQD', 'GLD', 'DBC', 'FXE']

# 从雅虎财经中将证券过去的历史收盘价格下载下来
# 创建closePrices_df的dataframe
# 通过for循环从yahoo finance中下载数据

closePrices_df = pd.DataFrame()
for ticker in tickers:
    data = yf.download(ticker, start=startDate, end=endDate)
    closePrices_df[ticker] = data['Adj Close']

# 计算上述资产过去两年每日Log Return，并将NA的数据去除
# 通过np.log，以及df.shift的组合计算资产的log return
logReturn = np.log(closePrices_df / closePrices_df.shift(1)).dropna()
logReturn


# 创建组合指标计算公式
# 创建计算组合期望收益率的公式
def portfolio_expected_return(weights, logReturn):
    return np.sum(weights * logReturn.mean())


# 创建计算组合标准差的公式
# 如果是python 3.5版本以上的，可以使用@来计算矩阵相乘
def portfolio_standard_deviation(weights, cov_matrix):
    portfolio_variance = weights.T @ cov_matrix @ weights  # 计算组合方差， 再计算标准差
    std = np.sqrt(portfolio_variance)
    return std


# 创建组合（设置组合权重）
# 设置Portfolio初始金额
portfolio = 1000000
# 创建一个Dictionary，将每个资产的权重都设置成一致
value_per_ticker = 1 / len(tickers)
portfolio_weights = pd.Series({ticker: value_per_ticker for ticker in tickers})
# portfolio_weights = {'SPY': 0.4,'LQD': 0.1,'GLD': 0.1,'DBC': 0.3,'FXE': 0.1}
# portfolio_weights = pd.Series(portfolio_weights)
# 计算各个资产log收益率之间的协方差矩阵
portfolio_covariance = logReturn.cov()
portfolio_covariance

portfolioExpectedReturn = portfolio_expected_return(portfolio_weights, logReturn)
portfolioStd = portfolio_standard_deviation(portfolio_weights, portfolio_covariance)
print(portfolioExpectedReturn)
print(portfolioStd)

logReturn.mean()


# 进行蒙特卡洛模拟设置
# 通过正态分布创建随机数（标准分数/Z-Score）
def random_Z_Score():
    return np.random.normal(0, 1)


# 确定计算几天（X天）的VaR
Days = 10


# 创建一个公式，可以返回一次蒙特卡洛模拟下，组合在X天后的损益情况
def scenario_PL(PortSize, PortExpReturn, PortStvd, days):
    portfolioValue = PortSize
    for day in range(days):
        z_score = random_Z_Score()
        portfolioValue = portfolioValue * np.exp(PortExpReturn + PortStvd * z_score)  # 每天的金额循环
    PortPL = portfolioValue - PortSize
    return PortPL


# 进行蒙特卡洛模拟
# 设置模拟此时
simulationTimes = 100000
# 创建一个空列表来装载模拟的结果
simulationResult = []
# 进行模拟
for i in range(simulationTimes):
    pl = scenario_PL(portfolio,
                     portfolioExpectedReturn,
                     portfolioStd,
                     Days
                     )
    simulationResult.append(pl)  # 每次结果不一样
simulationResult
pd.DataFrame(simulationResult).describe()

# 设置执行区间，并计算VaR值
# 置信区间水平设置越高(显著性水平越小），损失越大
# 天数（days）越大，损失越大
# 设置confidence_interval = 0.95
confidence_interval = 0.95
# 通过np.percentile计算VaR值
VaR = np.percentile(simulationResult, 100 - confidence_interval * 100)
print(VaR)


# 将数据可视化呈现
# 进行作图
sns.histplot(simulationResult, kde=True, color='blue')
plt.xlabel(f'{Days} - 天组合损益')
plt.ylabel('频率/出现次数')
plt.title(f'组合{Days}天损益分布情况')
plt.axvline(VaR, color='r', linestyle='dashed', linewidth=2, label=f'在{confidence_interval:.0%}置信水平下的VaR')
plt.legend()
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False
plt.show()
