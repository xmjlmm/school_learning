from flask import Flask

app = Flask(__name__)

@app.route('/')


def hell():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug = True, port = 8000)


# import random
# x = random.randint(1,2)
# print(x)
