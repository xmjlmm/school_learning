'''说明：每个app中都存在一个url_map，
这个url_map中包含了url到endpoint的映射；
作用：当request请求传来一个url的时候，会在url_map中先通过rule找到endpoint，
然后再在view_functions中根据endpoint再找到对应的视图函数view_func
'''


from flask import Flask

app = Flask(__name__)

# endpoint默认为视图函数的名称
@app.route('/test')
def test():
    return 'test success!'
# 我们也可以在路由中修改endpoint（当视图函数名称很长时适用）
# 相当于为视图函数起别名
@app.route('/hello',endpoint='our_set')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    print(app.view_functions)
    print(app.url_map)
    app.run(debug = True, port = 8000, localhost = '127.0.0.0')

