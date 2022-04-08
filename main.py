import sys
import json
import csv
import login
from data import db_session
from flask import Flask
from flask import render_template, request, redirect, Blueprint
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
#@app.route('/main', methods=['GET', 'POST'])
def main_page():
    if request.method == "POST":
        if request.form['button'] == "Профиль":
            return redirect('/puk')
        elif request.form['button'] == "Обсуждения":
            return redirect('/puk')
    return render_template('main_page.html', title="Главная")


@app.route('/puk')
def puk():
    return "Пук-пук-пук"


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')
