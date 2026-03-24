import random
import math
import numpy as np
import matplotlib.pyplot as plt

# 读取Excel文件
cost_data = pd.read_excel('cost.xlsx')
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