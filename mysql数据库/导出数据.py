import pandas as pd
import mysql.connector


# 1. 连接到 MySQL 数据库
cnx = mysql.connector.connect(user='root', password='lmmlmm19980323',
                              host='127.0.0.1', database='database_learn')
cursor = cnx.cursor()

# 2. 执行 SQL 查询语句
query = "SELECT * FROM excel_data"  # 替换为你的查询语句
cursor.execute(query)

# 3. 获取查询结果并转换为 DataFrame
columns = [col[0] for col in cursor.description]
df = pd.DataFrame(cursor.fetchall(), columns=columns)

# 4. 将 DataFrame 导出到 Excel 文件
excel_file = "F:\\数模\\国赛\\国赛2023\\C题\\2.xlsx"  # 输出的 Excel 文件路径
df.to_excel(excel_file, index=False)

# 5. 关闭游标和数据库连接
cursor.close()
cnx.close()

print(f"数据已成功导出到 {excel_file}")
