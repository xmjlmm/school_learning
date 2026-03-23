from flask import Flask, render_template

app = Flask(__name__)

def lover_name_switch(name):
    if  name == 'dich':
        return '舒彤'

app.add_template_filter(lover_name_switch, 'lover_name_switch')

class mylover():
    def __init__(self, name, email):
        self.name = name
        self.email = email



@app.route('/')
def hello_world():
    my_lover = mylover('舒彤', '123456789@qq.com')
    person = {
        'name': '舒彤',
        'email': '123456789@qq.com'
    }
    return render_template('index.html', my_lover = my_lover, person = person)

@app.route('/blog/<blog_id>')
def blog_id(blog_id):
    return render_template('blog.html', blog_id = blog_id, use_name = '舒彤')


@app.route('/filter')
def filter():
    person = {
        'name': '舒彤',
        'email': '123456789@qq.com'
    }
    person2 = {
        'name' : 'dich',
        'email' : '123456789@qq.com'
    }
    return render_template('filter.html', person = person, person2 = person2)

@app.route('/control')
def control_statement():
    name = '舒彤'
    success = [
        '大物考试顺利,记得明天早上起来看看公式纸上的公式,考的都会,蒙的全对，考试的时候就老老实实,记得仔细看题,把题目看完了再做',
        '电路二顺利',
        '嵌入式顺利',
        '算法顺利',
    ]
    return render_template('control.html', name = name, success = success)

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/child1')
def child1():
    return render_template('child1.html')

@app.route('/child2')
def child2():
    return render_template('child2.html')

@app.route('/static')
def static_statement():
    return render_template('static.html')



if __name__ == '__main__':
    app.run(debug = True, port = 8000)
