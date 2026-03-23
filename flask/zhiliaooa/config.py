
SECRET_KEY = "asdfasdfjasdfjasd;lf"

# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_learning'
USERNAME = 'root'
PASSWORD = 'lmmlmm19980323'
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2651094755@qq.com"
MAIL_PASSWORD = "lmmlmm19980323"
MAIL_DEFAULT_SENDER = "2156988655@qq.com"