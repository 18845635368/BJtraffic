from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def hello_world():
    return 'hello world'

@app.route('/api/1')
def g():
    with open('echarts_test_data.json', 'r') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)

