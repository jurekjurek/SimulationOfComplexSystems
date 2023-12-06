import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

# 下载S&P 500指数数据
data = yf.download('SPY', start='2012-01-01', end='2022-12-31')

# 计算日回报率
data['Return'] = data['Adj Close'].pct_change()
data.dropna(inplace=True)

# 定义测试窗口期
test_start = '2015-01-01'
estimation_window_size = 250
p_var = [0.95, 0.99]

# 筛选测试窗口期数据
test_data = data[data.index >= test_start]

# 初始化VaR值存储
normal_var = pd.DataFrame(index=test_data.index, columns=['95%', '99%'])
historical_var = pd.DataFrame(index=test_data.index, columns=['95%', '99%'])
ewma_var = pd.DataFrame(index=test_data.index, columns=['95%', '99%'])

# 计算VaR值
lambda_ = 0.94
sigma2 = test_data['Return'].iloc[0] ** 2

for date in test_data.index:
    # 正态分布法
    sigma = data['Return'][:date].tail(estimation_window_size).std()
    z_scores = norm.ppf(p_var)
    normal_var.loc[date] = -sigma * z_scores

    # 历史模拟法
    sorted_returns = data['Return'][:date].tail(estimation_window_size).sort_values(ascending=False)
    historical_var.loc[date, '95%'] = -sorted_returns.quantile(p_var[0])
    historical_var.loc[date, '99%'] = -sorted_returns.quantile(p_var[1])

    # EWMA
    if date != test_data.index[0]:
        prev_date = data.index.asof(date - pd.Timedelta(days=1))
        sigma2 = (1 - lambda_) * data['Return'][prev_date] ** 2 + lambda_ * sigma2
    sigma = np.sqrt(sigma2)
    ewma_var.loc[date] = -sigma * z_scores

# 绘制VaR值图表
plt.figure(figsize=(12, 6))
plt.plot(normal_var['95%'], label='Normal 95%')
plt.plot(normal_var['99%'], label='Normal 99%')
plt.title('Normal Distribution VaR')
plt.xlabel('Date')
plt.ylabel('VaR')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(historical_var['95%'], label='Historical 95%')
plt.plot(historical_var['99%'], label='Historical 99%')
plt.title('Historical Simulation VaR')
plt.xlabel('Date')
plt.ylabel('VaR')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(ewma_var['95%'], label='EWMA 95%')
plt.plot(ewma_var['99%'], label='EWMA 99%')
plt.title('EWMA VaR')
plt.xlabel('Date')
plt.ylabel('VaR')
plt.legend()
plt.show()

# 比较每种方法的95%置信区间VaR值与实际每日收益率
plt.figure(figsize=(12, 6))
plt.plot(test_data['Return'], label='Daily Returns', color='grey')
plt.plot(normal_var['95%'], label='Normal 95%', linestyle='--')
plt.plot(historical_var['95%'], label='Historical 95%', linestyle='-.')
plt.plot(ewma_var['95%'], label='EWMA 95%', linestyle=':')
plt.title('VaR 95% vs Daily Returns')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()
plt.show()

# 选择一个特定的时间段，例如2020年的市场波动期
start_date = '2020-03-01'
end_date = '2020-4-30'

# 筛选特定月份的数据
selected_data = test_data[(test_data.index >= start_date) & (test_data.index <= end_date)]

# 绘制图表
plt.figure(figsize=(12, 6))

# 使用柱状图表示收益率
plt.bar(selected_data.index, selected_data['Return'], label='Daily Returns', color='grey', width=0.5)

# 使用折线图展示三种VaR计算方法的值
plt.plot(selected_data.index, normal_var.loc[selected_data.index, '95%'], label='Normal 95%', linestyle='--')
plt.plot(selected_data.index, historical_var.loc[selected_data.index, '95%'], label='Historical 95%', linestyle='-.')
plt.plot(selected_data.index, ewma_var.loc[selected_data.index, '95%'], label='EWMA 95%', linestyle=':')

# 标记正态分布法VaR突破点
normal_breaches = selected_data[selected_data['Return'] < normal_var.loc[selected_data.index, '95%']]
plt.scatter(normal_breaches.index, normal_var.loc[normal_breaches.index, '95%'], color='blue', marker='o')

# 标记历史模拟法VaR突破点
historical_breaches = selected_data[selected_data['Return'] < historical_var.loc[selected_data.index, '95%']]
plt.scatter(historical_breaches.index, historical_var.loc[historical_breaches.index, '95%'], color='red', marker='o')

# 标记EWMA法VaR突破点
ewma_breaches = selected_data[selected_data['Return'] < ewma_var.loc[selected_data.index, '95%']]
plt.scatter(ewma_breaches.index, ewma_var.loc[ewma_breaches.index, '95%'], color='yellow', marker='o')

plt.title('VaR Breaches in August 1998')
plt.xlabel('Date')
plt.ylabel('Returns')
plt.legend()
plt.show()
