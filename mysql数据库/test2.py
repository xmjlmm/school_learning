# import mysql.connector
#
# # 配置数据库连接参数
# config = {
#   'user': 'root',
#   'password': 'lmmlmm19980323',
#   'host': '127.0.0.1',  # 数据库主机地址
#   'database': 'database_learn',  # 数据库名称
#   'raise_on_warnings': True
# }
#
# # 连接到数据库
# try:
#     cnx = mysql.connector.connect(**config)
#     print("Connected to MySQL database!")
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#     cnx = None
#
#
# def append_table():
#     if cnx:
#         cursor = cnx.cursor()
#
#         # 定义创建表的 SQL 语句
#         create_table_sql = """
#         CREATE TABLE IF NOT EXISTS excel3_data (
#             日期 VARCHAR(20),
#             单品编码 VARCHAR(100),
#             批发价格 float
#         )
#         """
#
#         # 执行创建表的 SQL 语句
#         try:
#             cursor.execute(create_table_sql)
#             print("创建表 'excel3_data' 成功！")
#         except mysql.connector.Error as err:
#             print(f"创建表错误: {err}")
#
#         cursor.close()
#
#
# def delete_table():
#     if cnx:
#         cursor = cnx.cursor()
#
#         # 定义删除表的 SQL 语句
#         drop_table_sql = "DROP TABLE IF EXISTS excel2_data"
#
#         # 执行删除表的 SQL 语句
#         try:
#             cursor.execute(drop_table_sql)
#             print("删除表 'excel2_data' 成功！")
#         except mysql.connector.Error as err:
#             print(f"删除表错误: {err}")
#
#         cursor.close()
#
# def main():
#     append_table()
#     # delete_table()
#     if cnx:
#         cnx.close()
#         print("MySQL 连接已关闭。")
#
# if __name__ == "__main__":
#     main()




# import pandas as pd
# import mysql.connector
#
# # 1. 导入 Excel 文件
# excel_file = "F:\\数模\\国赛\\国赛2023\\C题\\附件3.xlsx"  # 替换为你的 Excel 文件路径
# df = pd.read_excel(excel_file, header = 0)
# print(df.columns)
#
# # 2. 连接到 MySQL 数据库
# # 假设 MySQL 数据库在本地，用户名为 'root'，密码为 'lmmlmm19980323'，数据库名为 'database_learn'
# cnx = mysql.connector.connect(user='root', password='lmmlmm19980323', host='127.0.0.1', database='database_learn')
# cursor = cnx.cursor()
#
# # 3. 将数据插入到数据库表中
# # 假设要将数据插入到名为 'excel_data' 的数据表中
# table_name = 'excel3_data'  # 替换为你的数据表名
#
# # 创建插入数据的 SQL 语句
# insert_sql = f"INSERT INTO {table_name} (日期, 单品编码, 批发价格) VALUES (%s, %s, %s)"
#
# # 将 DataFrame 中的每一行数据插入到数据库表中
# for index, row in df.iterrows():
#     data_tuple = (row['日期'], row['单品编码'], row['批发价格(元/千克)'])
#     cursor.execute(insert_sql, data_tuple)
#
# # 提交更改并关闭游标和数据库连接
# cnx.commit()
# cursor.close()
# cnx.close()
#
# print(f"{len(df)} 条数据成功插入到数据库表 '{table_name}' 中。")
#


# import mysql.connector
# import pandas as pd
#
# # 配置数据库连接参数
# config = {
#   'user': 'root',
#   'password': 'lmmlmm19980323',
#   'host': '127.0.0.1',  # 数据库主机地址
#   'database': 'database_learn',  # 数据库名称
#   'raise_on_warnings': True
# }
#
# # 连接到数据库
# try:
#     cnx = mysql.connector.connect(**config)
#     print("Connected to MySQL database!")
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#     cnx = None
#
#     if cnx:
#         cursor = cnx.cursor()
#
# query = """
#     SELECT excel_data.销售日期, excel_data.扫码销售时间, excel_data.单品编码, excel_data.销量,excel_data.销售单价,excel_data.销售类型,excel_data.是否打折销售,excel3_data.批发价格
#     FROM excel_data
#     LEFT JOIN excel3_data ON excel_data.单品编码 = excel3_data.单品编码;
#     """
#
# # 执行查询并获取结果
# result = pd.read_sql_query(query, cnx)
# print(result)
#
# # 关闭数据库连接
# cnx.close()


import mysql.connector
import pandas as pd

# 配置数据库连接参数
config = {
  'user': 'root',
  'password': 'lmmlmm19980323',
  'host': '127.0.0.1',  # 数据库主机地址
  'database': 'database_learn',  # 数据库名称
  'raise_on_warnings': True
}

# 连接到数据库
try:
    cnx = mysql.connector.connect(**config)
    print("Connected to MySQL database!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    cnx = None

# 定义查询语句
query = """
    SELECT excel_data.销售日期, excel_data.扫码销售时间, excel_data.单品编码, excel_data.销量, excel_data.销售单价, excel_data.销售类型, excel_data.是否打折销售, excel3_data.批发价格
    FROM excel_data
    LEFT JOIN excel3_data ON excel_data.单品编码 = excel3_data.单品编码
"""

# 使用pandas的read_sql_query函数逐批次处理数据
chunk_size = 10000  # 每次查询的行数
offset = 0
while True:
    query_chunk = f"{query} LIMIT {offset}, {chunk_size}"
    df_chunk = pd.read_sql_query(query_chunk, cnx)

    # 处理数据，可以在这里进行你的操作

    # 检查是否还有更多数据需要处理
    if len(df_chunk) < chunk_size:
        break

    offset += chunk_size

# 关闭数据库连接
cnx.close()

print("数据处理完成！")
