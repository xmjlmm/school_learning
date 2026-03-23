from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import render_template
from flask_migrate import Migrate


app = Flask(__name__)

# mysql所在的主机名
HOSTNAME = '127.0.0.1'
# mysql的端口号,默认是3306
PORT = 3306
# 连接mysql的用户名
USERNAME = 'root'
# 连接mysql的密码
PASSWORD = 'lmmlmm19980323'
# mysql上创建的数据库名称
DATABASE = 'database_learn'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

@app.route('/')

def main_first():
    return 'hello world!'

# 然后用SQLAlchemy(app)创建一个db对象
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# ORM模型映射成表的三步：
# 1. flask db init : 这一步只需要执行一次
# 2. flask db migrate : 识别ORM模型的改变，生成迁移脚本
# 3. flask db upgrade : 执行迁移脚本，将迁移脚本生成的表结构更新到数据库中

'''
flask db init 报错信息处理方法：

$env:FLASK_APP='realproject'

$env:FLASK_ENV = "development"

flask db init'''

# SQLAlchemy会自动读取App.config
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text('select 1'))
        print(rs.fetchone())  # (1, )

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# user = User(username='舒彤', password='031225')
# sql : insert user(username, password) values ('舒彤', '031225')

class Lo(db.Model):
    __tablename__ = 'lover'
    name = db.Column(db.String(100), nullable = False)
    num = db.Column(db.Integer, primary_key = True, autoincrement = True)
    char = db.Column(db.String(100), nullable = False)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text, nullable = False)

    # 添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # backref: 会自动的给user模型添加一个articles的属性,用来获取文章列表
    author = db.relationship('User', backref='articles')

# with app.app_context():
#     db.create_all()

@app.route('/data/add')
def data_add():
    # 1. 创建ORM对象
    user = User(username = '舒彤', password = '031225')
    # 2. 添加到session
    db.session.add(user)
    # 3. 将db.session中的改变同步到数据库中
    db.session.commit()
    return '干的漂亮，创建了一个数据库'

@app.route('/data/query')
def data_query():
    # # 1. get 查找：根据主键查找
    # user = User.query.get(1)
    # print(f'{user.id} : {user.username} - {user.password}')
    # 2. filter_by 查找 ,  查找所有满足条件的数据
    users = User.query.filter_by(username = '舒彤')
    for user in users:
        print(f'{user.id} : {user.username} - {user.password}')
    return '查询成功'

@app.route('/data/update')
def data_update():
    user = User.query.filter_by(username = '舒彤').first()
    user.password = '123456'
    db.session.commit()
    return '更新成功'

@app.route('/data/delete')
def data_delete():
    user = User.query.filter_by(username = '舒彤').first()
    db.session.delete(user)
    db.session.commit()
    return '删除成功'

@app.route('/article/add')
def article_add():
    article1 = Article(title='flask学习', content='flask是一个web框架')
    article1.author = User.query.get(2)

    article2 = Article(title='rapter学习', content='rapter是一个rapper')
    article2.author = User.query.get(2)

    db.session.add_all([article1, article2])
    # 同步更新数据库
    db.session.commit()
    return '文章创建成功'

@app.route('/article/query')
def article_query():
    user = User.query.get(2)
    for article in user.articles:
        print(article.title)
    return '文章查询成功'

@app.route('/article/delete')
def article_delete():
    user = Article.query.filter_by(title = 'flask学习').first()
    db.session.delete(user)
    db.session.commit()
    return '文章删除成功'

if __name__ == '__main__':
    app.run(debug = True, port = 8000)