
import pandas as pd
from prophet import Prophet
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# 读取Excel文件
sales_data = pd.read_excel("D://数模//国赛2023//2023 C题//sales.xlsx")
profit_data = pd.read_excel("D://数模//国赛2023//2023 C题//profit.xlsx")

rows = 6
cols = 7
prediction_sales = [[0] * cols for _ in range(rows)]

# 对每个品类进行遍历
for category in range(1, 7):
    columns = [0, category]  # 第一列的索引为0，第三列的索引为2
    # 销量
    sales = sales_data.iloc[1:, columns]
    sales.columns = ['ds', 'y']
    # 利润率
    profit = profit_data.iloc[1:, columns]
    profit.columns = ['ds', 'profit']

    data = pd.merge(sales, profit, on='ds', how='inner')
    data['profit'].interpolate(method='linear', inplace=True)

    # 创建Prophet模型
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.add_regressor('profit')
    model.add_country_holidays(country_name='CN')  # 添加中国的节假日
    model.fit(data)

    # 绘制图像
    future = model.make_future_dataframe(periods=0)  # 不预测未来，只使用现有数据
    future = pd.merge(future, profit, on='ds')  # 确保future 数据框也包含profit 列
    future['profit'].interpolate(method='linear', inplace=True)
    forecast = model.predict(future)
    print(forecast)
    fig1 = model.plot(forecast)
    fig2 = model.plot_components(forecast)

    # 预测未来7天
    future = model.make_future_dataframe(periods=7)
    future = pd.merge(future, profit, on='ds', how='left')
    future['profit'].interpolate(method='linear', inplace=True)
    forecast = model.predict(future)
    forecasted_values = forecast.tail(7)[['ds', 'yhat']]
    forecasted_sales = list()

    prediction_sales[category - 1] = list(forecasted_values['yhat'])


#---------------------------------------------------------------------------


# 读取Excel文件
cost_data = pd.read_excel("D://数模//国赛2023//2023 C题//cost.xlsx")
rows = 6
cols = 7
prediction_cost = [[0] * cols for _ in range(rows)]
for category in range(1, 7):
    columns = [0, category]
    # 提取相关列作为成本数据
    cost = cost_data.iloc[1:, columns]
    cost.columns = ['ds', 'y']

    # 创建并拟合Prophet模型
    model = Prophet()
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.add_country_holidays(country_name='CN')  # 添加中国的节假日
    model.fit(cost)

    # 画图
    future = model.make_future_dataframe(periods=0)  # 不预测未来，只使用现有数据

    forecast = model.predict(future)
    fig1 = model.plot(forecast)
    fig2 = model.plot_components(forecast)

    # 创建未来时间序列
    future = model.make_future_dataframe(periods=7)
    # 进行预测
    forecast = model.predict(future)

    forecasted_values = forecast.tail(7)[['ds', 'yhat']]
    forecasted_sales = list()

    prediction_cost[category - 1] = list(forecasted_values['yhat'])

print(prediction_cost)

# 模拟退火求解
Q = np.array(prediction_sales)  # 销量
C = np.array(prediction_cost)  # 成本
Loss = np.array([10.66463844, 12.73368135, 7.755571213, 6.411989175, 8.884176144, 8.911259058])


# 模拟退火函数
def simulated_annealing_maximize(initial_solution, temperature, cooling_rate, max_iterations, iter):
    # 生成初始解
    current_solution = initial_solution
    best_solution = initial_solution
    best_value = objective_function(best_solution, iter)

    # 迭代
    for iteration in range(max_iterations):
        temperature *= cooling_rate

        # 生成新的解
        new_solution = generate_new_solution(current_solution, temperature, iter)

        # 计算当前解和新解的目标函数值
        current_value = objective_function(current_solution, iter)
        new_value = objective_function(new_solution, iter)

        # 计算目标函数值的差异
        value_diff = new_value - current_value

        # 判断是否接受新解，与爬山法的区别***********
        if value_diff > 0 or random.random() < math.exp(value_diff / temperature):
            current_solution = new_solution
            current_value = new_value

        # 更新最优解
        if current_value > best_value:
            best_solution = current_solution
            best_value = current_value

    return best_solution


# 生成新的解的函数
def generate_new_solution(solution, temperature, iter):
    y = [random.randint(1, 100) for _ in range(6)]
    y = np.array(y)
    z = y / math.sqrt(np.sum(np.sqrt(y)))
    new_solution = solution + (z * temperature)
    for i in range(6):
        if new_solution[i] < C[i, iter] * 1.2 or new_solution[i] > C[i, iter] * 1.5:
            random_float = random.random()
            new_solution[i] = C[i, iter] * 1.1 + 0.4 * C[i, iter] * random_float
    return new_solution


# 目标函数
def objective_function(solution, iter):
    P = np.array(solution)
    y = (P - C[:, iter]) * Q[:, iter] * (1.0 - Loss) + (0.8 * solution - C[:, iter]) * Q[:, iter] * Loss
    return sum(y)


begin_solution = np.array([9, 9, 9, 9, 9, 9])

rows = 7
cols = 6
result = [[0] * cols for _ in range(rows)]
for iter in range(7):
    ans = simulated_annealing_maximize(begin_solution, 1000, 0.95, 200, iter)
    result[iter] = ans
print(result)

plt.figure()
price = np.array(result)
for i in range(6):
    x = range(1,8)
    plt.plot(x,price[:,i])




print('-----------------------------------------------------------------------------------------------------')



import pandas as pd

import numpy as np
import cvxpy as cp
import random
import math
from prophet import Prophet
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from prophet.diagnostics import cross_validation, performance_metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import statsmodels.api as sm
# 创建按品类划分的数据表
df_items = pd.read_excel("D://数模//国赛2023//C题//附件1.xlsx", engine='openpyxl') # 从附件 1 读取蔬菜单品的数据
df_sales = pd.read_excel("D://数模//国赛2023//C题//附件2.xlsx", engine='openpyxl') # 从附件 2 读取购买流水数据
df_merged = pd.merge(df_sales, df_items, on='单品编码', how='left') # 通过蔬菜编码连接两个数据表
df_merged['金额'] = df_merged['销量(千克)'] * df_merged['销售单价(元/千克)'] # 计算每笔订单的销售金额（考虑退货，所以使用负值）
df_merged.loc[df_merged['销售类型'] == '退货', '金额'] *= -1
df_merged.loc[df_merged['销售类型'] == '退货', '销量(千克)'] *= -1
# 获取蔬菜单品每日平均价格
daily_price = df_merged.groupby(['单品编码', '单品名称', '销售日期'])['销售单价(元/千克)'].mean().reset_index()
# 按照蔬菜单品和销售日期来计算每日销售总销量、总金额
daily_vol = df_merged.groupby(['单品编码', '单品名称', '销售日期'])['销量(千克)'].sum().reset_index()
daily_sales = df_merged.groupby(['单品编码', '单品名称', '销售日期'])['金额'].sum().reset_index()
# 根据退货和销售金额计算退货率
total_returned = df_merged[df_merged['销售类型'] == '退货'].groupby('单品编码')['金额'].sum()
total_sales = df_merged[df_merged['销售类型'] == '销售'].groupby('单品编码')['金额'].sum()
return_rate = (total_returned / total_sales).reset_index(name='退货率')
# 合并数据获取每日平均价格
pivot_price = daily_price.pivot_table(index=['单品编码', '单品名称'], columns='销售日期', values='销售单价(元/千克)', fill_value=0).reset_index()
finalprice_df = pd.merge(df_items[['单品编码', '单品名称', '分类名称']], return_rate, on='单品编码', how='left')
finalprice_df = pd.merge(finalprice_df, pivot_price, on=['单品编码', '单品名称'], how='left')
# 合并数据获取每日销量
pivot_vol = daily_vol.pivot_table(index=['单品编码', '单品名称'], columns='销售日期', values='销量(千克)', fill_value=0).reset_index()
finalvol_df = pd.merge(df_items[['单品编码', '单品名称', '分类名称']], return_rate, on='单品编码', how='left')
finalvol_df = pd.merge(finalvol_df, pivot_vol, on=['单品编码', '单品名称'],how='left')
# 合并数据以获取每日销售额
pivot_sales = daily_sales.pivot_table(index=['单品编码', '单品名称'], columns='销售日期', values='金额', fill_value=0).reset_index()
finalsales_df = pd.merge(df_items[['单品编码', '单品名称', '分类名称']], return_rate, on='单品编码', how='left')
finalsales_df = pd.merge(finalsales_df, pivot_sales, on=['单品编码', '单品名称'], how='left')

print(finalsales_df)

# 保存为新的 Excel 文件
finalprice_df.to_excel('D://数模//国赛2023//C题//output_price.xlsx', index=False, engine='openpyxl')
finalvol_df.to_excel('D://数模//国赛2023//C题//output_vol.xlsx', index=False, engine='openpyxl')
finalsales_df.to_excel('D://数模//国赛2023//C题//output_sales.xlsx', index=False, engine='openpyxl')
# 使用 Prophet 剔除季节因素，研究销售价格和销售总量的关系。X_1 和 X_2（可选）为外生解释变量价格



X_1='辣椒类'
X_2='茄类'
# 读取数据并设置列名
input_df_sales = pd.read_excel("D://数模//国赛2023//C题//output_vol.xlsx", sheet_name="销售量",skiprows=0)
input_df_sales.columns = ['ds'] + input_df_sales.columns[1:].tolist()
df_price = pd.read_excel("D://数模//国赛2023//C题//output_price.xlsx", skiprows=0)
df_price.columns = ['ds'] + df_price.columns[1:].tolist()
df_price[X_1].fillna(0, inplace=True)
df_price[X_2].fillna(0, inplace=True)
# num_cols = input_df_sales.select_dtypes(include=['number']).columns
# input_df_sales[num_cols] = input_df_sales[num_cols].where(input_df_sales[num_cols] > 0, 0)
for col in input_df_sales.columns[1:]:
    # 选择一个蔬菜品类
    df_sales = input_df_sales[['ds', col]]
    df_sales = df_sales[df_sales[col] > 0].rename(columns={col: 'y'})
    # 合并销售量和利润率数据
    merged_df = pd.merge(df_sales, df_price, on='ds')
    # merged_df = merged_df.drop(merged_df.index[0:1063]).reset_index(drop=True) # 控制时间范围
    # 初始化 Prophet
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.add_country_holidays(country_name='CN') # 添加中国的节假日
    # model.add_regressor(df_price.columns[1:].all()) # 添加全部价格作为外生解释变量
    # model.add_regressor(X_1)
    # model.add_regressor(X_2)
    model.add_regressor(col) # 添加对应价格作为外生解释变量
    model.fit(merged_df)
    # 代入 Prophet，分析利润率这一外生变量的关联
    future = model.make_future_dataframe(periods=0) # 不预测未来，只使用现有数据
    future = pd.merge(future, df_price, on='ds') # 确保 future 数据框也包含profit 列
    forecast = model.predict(future)
    # 绘制图像
    # print(forecast)
    # fig1 = model.plot(forecast)
    # fig2 = model.plot_components(forecast)
    print(col,evaluate_prophet_performance(merged_df,forecast)) # 评价拟合效果
    merged_df['y_adjusted'] = forecast['yhat'] - forecast['yearly'] - forecast['weekly'] - forecast['holidays']  # 剔除季节和节假日效应
    # ols_regression(col,merged_df['y_adjusted'],merged_df[X_1],merged_df[X_2])
    # plot_scatter_and_fit_line(col,merged_df[col],merged_df['y_adjusted'])
    # neighborhood_regression(col,merged_df[col],merged_df['y_adjusted'])
    # 读取 output_price.xlsx 和附件 3.xlsx
    price_df = pd.read_excel("D://数模//国赛2023//C题//output_price.xlsx", engine='openpyxl')
    cost_df = pd.read_excel("D://数模//国赛2023//C题//附件3.xlsx", engine='openpyxl')
    df_merged = pd.merge(price_df, cost_df, on='单品编码', how='left')  # 通过蔬菜编码连接两个数据表
    # 把附件 3 数据转换成宽格式，以便于合并
    pivot_cost = cost_df.pivot_table(index='单品编码', columns='日期', values='批发价格(元 / 千克)', fill_value=0).reset_index()
    # 合并数据
    merged_df = pd.merge(price_df[['单品编码']], pivot_cost, on='单品编码',how='left')
    # 从第五列开始计算成本利润率
for date in price_df.columns[4:]:
    merged_df[date] = price_df[date] / merged_df[date] - 1
    merged_df[date].replace({-1: None}, inplace=True)  # 剔除异常值
    merged_df[date].replace({0: None}, inplace=True)
    # 保存到新 Excel 文件
    merged_df.to_excel('cost_profit_margin.xlsx', index=False, engine='openpyxl')
    # 利用 Prophet 预测各品类蔬菜批发价格。
    # 读取数据并设置列名
input_df_sales = pd.read_excel("category_inprice.xlsx", skiprows=0)
input_df_sales.columns = ['ds'] + input_df_sales.columns[1:].tolist()
forecast_cost = pd.DataFrame({"时间": pd.date_range("20230701", periods=7)})
for col in input_df_sales.columns[1:]:
    # 选择一个蔬菜品类
    df_sales = input_df_sales[['ds', col]]
    df_sales = df_sales[df_sales[col] > 0].rename(columns={col: 'y'})
    # 合并销售量和利润率数据
    merged_df = pd.merge(df_sales, df_price, on='ds')
    # 初始化 Prophet
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True,daily_seasonality=False)
    model.add_country_holidays(country_name='CN')  # 添加中国的节假日
    model.fit(merged_df)
    # 代入 Prophet，分析利润率这一外生变量的关联
    future = model.make_future_dataframe(periods=7)  # 预测未来 7 天进货价格数据
    # future = pd.merge(future, df_price, on='ds') # 确保 future 数据框也包含profit列
    forecast = model.predict(future)
    # 绘制图像
    # fig1 = model.plot(forecast)
    # fig2 = model.plot_components(forecast)
    future_values = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7)
    print(col + ":")
    print(future_values)
    forecast_cost[col] = forecast[['yhat']].tail(7).values
    print(forecast_cost)


def mkt_demand(sale_price, history_df_price):


    # 读取销售量数据并设置列名
    input_df_sales = pd.read_excel("category_vol.xlsx", sheet_name="销售量",skiprows=0)
    input_df_sales.columns = ['ds'] + input_df_sales.columns[1:].tolist()
    print(sale_price)
    print(history_df_price)
    # 将 sale_price 添加到 history_df_price 的末尾
    sale_price['ds'] = history_df_price['ds'].iloc[-1] + pd.Timedelta(days=1)  # 假设 sale_price 是下一天的价格
    df_price = history_df_price.append(sale_price, ignore_index=True)
    # 初始化 Prophet
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True,daily_seasonality=False)
    model.add_country_holidays(country_name='CN')  # 添加中国的节假日
    model.add_regressor(df_price.columns[1:].all())  # 添加价格作为外生解释变量
    predictions = {}
    for col in input_df_sales.columns[1:]:
        # 选择一个蔬菜品类
        df_sales = input_df_sales[['ds', col]]
        df_sales = df_sales[df_sales[col] > 0].rename(columns={col: 'y'})
        # 合并销售量和价格数据
        merged_df = pd.merge(df_sales, df_price, on='ds')
        model.fit(merged_df)
        future = model.make_future_dataframe(periods=1)  # 预测 1 天
        future = pd.merge(future, df_price, on='ds', how='left')  # 确保
        future
        数据框也包含价格列
        forecast = model.predict(future)
        # 保存预测的销量
        predictions[col] = forecast['yhat'].iloc[-1]
        return predictions
