import sys
import json
import csv
from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main_page():
    return "Главная страница"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
