import sys
import json
import csv
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main_page():
    param = {}
    param['title'] = "Главная"
    return render_template('main_page.html', **param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
