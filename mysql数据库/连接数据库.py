import mysql.connector

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


def append_table():
    if cnx:
        cursor = cnx.cursor()

        # 定义创建表的 SQL 语句
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS excel_data (
            销售日期 VARCHAR(20),
            扫码销售时间 VARCHAR(20),
            单品编码 VARCHAR(20),
            销量 float,
            销售单价 float,
            销售类型 VARCHAR(20),
            是否打折销售 VARCHAR(20)
        )
        """

        # 执行创建表的 SQL 语句
        try:
            cursor.execute(create_table_sql)
            print("创建表 'excel_data' 成功！")
        except mysql.connector.Error as err:
            print(f"创建表错误: {err}")

        cursor.close()


def delete_table():
    if cnx:
        cursor = cnx.cursor()

        # 定义删除表的 SQL 语句
        drop_table_sql = "DROP TABLE IF EXISTS excel_data"

        # 执行删除表的 SQL 语句
        try:
            cursor.execute(drop_table_sql)
            print("删除表 'excel_data' 成功！")
        except mysql.connector.Error as err:
            print(f"删除表错误: {err}")

        cursor.close()

def main():
    append_table()
    # delete_table()
    if cnx:
        cnx.close()
        print("MySQL 连接已关闭。")

if __name__ == "__main__":
    main()


