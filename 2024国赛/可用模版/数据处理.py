import pandas as pd
import numpy as np

# 1. 从外部导入数据
def load_data(file_path):
    """
    从指定路径加载 Excel 文件中的数据
    :param file_path: Excel 文件的路径
    :return: pandas DataFrame
    """
    data = pd.read_excel(file_path)
    return data

# 2. 检测异常值
def detect_outliers(data):
    """
    使用 3-sigma 规则检测异常值
    :param data: pandas DataFrame
    :return: pandas DataFrame，其中异常值被标记
    """
    # 遍历每一列
    for column in data.select_dtypes(include=[np.number]).columns:
        # 计算列的均值和标准差
        mean = data[column].mean()
        std_dev = data[column].std()

        # 计算异常值的阈值（均值±3*标准差）
        threshold_upper = mean + 3 * std_dev
        threshold_lower = mean - 3 * std_dev

        # 标记异常值
        outliers = ((data[column] > threshold_upper) | (data[column] < threshold_lower))
        if outliers.any():
            print(f"列 '{column}' 中发现异常值：")
            print(data[outliers])

    return data

# 3. 填补空缺值
def fill_missing_values(data):
    """
    填补缺失值
    数值型数据用均值填补，非数值型数据用最频繁值填补
    :param data: pandas DataFrame
    :return: pandas DataFrame，缺失值已填补
    """
    # 使用列的均值填补数值型数据的空缺值
    for column in data.select_dtypes(include=[np.number]).columns:
        mean_value = data[column].mean()
        # 使用 fillna 填补空缺值，并将结果重新赋值给原列
        data[column] = data[column].fillna(mean_value)

    # 使用最频繁值填补非数值型数据的空缺值
    for column in data.select_dtypes(include=[object]).columns:
        mode_value = data[column].mode()[0]
        # 使用 fillna 填补空缺值，并将结果重新赋值给原列
        data[column] = data[column].fillna(mode_value)

    return data

# 4. 保存数据到新的 Excel 文件
def save_data(data, output_file_path):
    """
    将处理后的数据保存到新的 Excel 文件中
    :param data: pandas DataFrame
    :param output_file_path: 保存文件的路径
    """
    data.to_excel(output_file_path, index=False)
    print(f"数据已保存到 {output_file_path}")

# 5. 主函数
def main(input_file_path, output_file_path):
    """
    主函数，执行数据加载、异常值检测、空缺值填补和数据保存
    :param input_file_path: 输入 Excel 文件的路径
    :param output_file_path: 输出 Excel 文件的路径
    """
    # 加载数据
    data = load_data(input_file_path)

    # 检测异常值
    data = detect_outliers(data)

    # 填补空缺值
    data = fill_missing_values(data)

    # 保存处理后的数据到新的 Excel 文件
    save_data(data, output_file_path)

    # 打印处理后的数据前几行以供检查
    print("处理后的数据：")
    print(data.head())

# 执行主函数
if __name__ == "__main__":
    # 输入 Excel 文件路径
    input_file_path = "F:\\数模\\国赛\\国赛2023\\C题\\附件2.xlsx"
    # 输出 Excel 文件路径
    output_file_path = "F:\\数模\\国赛\\国赛2023\\C题\\附件211.xlsx"
    main(input_file_path, output_file_path)
