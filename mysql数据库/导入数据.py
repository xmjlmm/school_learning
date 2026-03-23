import pandas as pd
import mysql.connector

# 1. 导入 Excel 文件
excel_file = "F:\\数模\\国赛\\国赛2023\\C题\\附件2.xlsx"  # 替换为你的 Excel 文件路径
df = pd.read_excel(excel_file)

# 2. 连接到 MySQL 数据库
# 假设 MySQL 数据库在本地，用户名为 'root'，密码为 'lmmlmm19980323'，数据库名为 'database_learn'
cnx = mysql.connector.connect(user='root', password='lmmlmm19980323', host='127.0.0.1', database='database_learn')
cursor = cnx.cursor()

# 3. 将数据插入到数据库表中
# 假设要将数据插入到名为 'excel_data' 的数据表中
table_name = 'excel_data'  # 替换为你的数据表名

# 创建插入数据的 SQL 语句
insert_sql = f"INSERT INTO {table_name} (销售日期, 扫码销售时间, 单品编码, 销量, 销售单价, 销售类型, 是否打折销售) VALUES (%s, %s, %s, %s, %s, %s, %s)"

# 将 DataFrame 中的每一行数据插入到数据库表中
for index, row in df.iterrows():
    data_tuple = (row['销售日期'], row['扫码销售时间'], row['单品编码'], row['销量(千克)'], row['销售单价(元/千克)'], row['销售类型'], row['是否打折销售'])
    cursor.execute(insert_sql, data_tuple)

# 提交更改并关闭游标和数据库连接
cnx.commit()
cursor.close()
cnx.close()

print(f"{len(df)} 条数据成功插入到数据库表 '{table_name}' 中。")
