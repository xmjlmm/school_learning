# 通过创建路由并关联函数，实现一个基本的网页：
from flask import Flask

# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)


# 程序实例需要知道每个url请求所对应的运行代码是谁。
# 所以程序中必须要创建一个url请求地址到python运行函数的一个映射。
# 处理url和视图函数之间的关系的程序就是"路由"，在Flask中，路由是通过@app.route装饰器(以@开头)来表示的
@app.route("/")
# url映射的函数，要传参则在上述route（路由）中添加参数申明
def index():
    return "Hello World!"


# 直属的第一个作为视图函数被绑定，第二个就是普通函数
# 路由与视图函数需要一一对应
@app.route("/not")
def not_index():
    return "Not Hello World!"

# 启动一个本地开发服务器，激活该网页
def main():
    app.run()


if __name__ == '__main__':
    main()



#
# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route("/")
# def index():
#     return "Hello World!"
#
# @app.route("/not")
# def not_index():
#     return "Not Hello World!"
#
# def main():
#     app.run()
#
# if __name__ == '__main__':
#     main()
