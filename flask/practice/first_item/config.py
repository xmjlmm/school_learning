# mysql所在的主机名
HOSTNAME = '127.0.0.1'
# mysql的端口号,默认是3306
PORT = 3306
# 连接mysql的用户名
USERNAME = 'root'
# 连接mysql的密码
PASSWORD = 'lmmlmm19980323'
# mysql上创建的数据库名称
DATABASE = 'flask_learning'

DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI


# # 邮箱配置
# MAIL_SERVER = 'smtp.qq.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USERNAME = '254152863@qq.com'
# MAIL_PASSWORD = 'vgjrqxgxfzgdbhid'
# MAIL_DEFAULT_SENDER = '254152863@qq.com'
