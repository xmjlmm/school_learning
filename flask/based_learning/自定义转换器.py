from werkzeug.routing import BaseConverter  # 导入转换器的基类，用于继承方法
from flask import Flask

app = Flask(__name__)


# 自定义转换器类
class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 重写父类定义方法
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex

    def to_python(self, value):
        # 重写父类方法，后续功能已经实现好了
        print('to_python方法被调用')
        return value


# 将自定义的转换器类添加到flask应用中
# 具体过程是添加到Flask类下url_map属性（一个Map类的实例）包含的转换器字典属性中
app.url_map.converters['re'] = RegexConverter


# 此处re后括号内的匹配语句，被自动传给我们定义的转换器中的regex属性
# value值会与该语句匹配，匹配成功则传达给url映射的视图函数
# 以1为开头，11位的关键字，例如http:127.0.0.1:5000/index/12345678901
@app.route("/index/<re('1\d{10}'):value>")
def index(value):
    print(value)
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
