import sys
import json
import csv
from data import db_session
from data.users import User
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from flask import Flask
from flask_login import LoginManager, login_user, current_user, login_required, \
    logout_user
from flask import render_template, request, redirect, Blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/main', methods=['GET', 'POST'])
    def main_page():
        if request.method == "POST":
            if request.form['button'] == "Профиль":
                if current_user.is_authenticated:
                    return redirect('profile')
                else:
                    return redirect('/register_or_login')
            elif request.form['button'] == "Обсуждения":
                return redirect('/threads')
        return render_template('main_page.html', title="Главная")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/register_or_login', methods=['POST', 'GET'])
    def register_or_login():
        if request.method == 'POST':
            if request.form['button'] == 'Вход':
                return redirect('/login')
            if request.form['button'] == 'Регистрация':
                return redirect('/register')
        return render_template('login_or_register.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if db_sess.query(User).filter(User.login == form.login.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            elif form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            elif len(form.password.data) < 8:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Короткий пароль")
            elif form.password.data.isdigit():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="В пароле нет букв")
            elif form.password.data.isalpha():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="В пароле нет цифр")
            elif form.password.data.lower() == form.password.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="В пароле нет букв разных регистров")
            f = form.photo.data
            t = f.read()
            user = User(
                login=form.login.data,
                photo=t
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.login == form.login.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @login_manager.user_loader
    def load_user(user_id):
        return db_sess.query(User).get(user_id)

    @app.route('/threads')
    def threads():
        list_of_threads = []
        for i in range(50):
            author_picture = None
            list_of_threads.append({"thread_name": f"Какое-то имя {i}",
                                    "author_picture": author_picture,
                                    "author_name": "Имя автора и прозвище",
                                    "thread_image": None,
                                    "thread_text": f"{i} тут текст треда и"
                                                   f" всякое такое {i} нужно "
                                                   f"написать побольше для "
                                                   f"наглядности, поэтому вот "
                                                   f"да{i}",
                                    "first_answer": {"answerer_name": f"1Тут имя и"
                                                                      " через "
                                                                      "запятую "
                                                                      "прозвище",
                                                     "answer_text": "Здесь должен "
                                                                    "быть какой-то "
                                                                    "текст ответа "
                                                                    "в тред"},
                                    "second_answer": {"answerer_name": f"2Тут имя "
                                                                       f"и через "
                                                                       "запятую "
                                                                       "прозвище",
                                                      "answer_text": "Здесь должен "
                                                                     "быть какой-то "
                                                                     "текст ответа "
                                                                     "в тред"},
                                    "third_answer": {"answerer_name": f"3Тут имя "
                                                                      f"и через "
                                                                      "запятую "
                                                                      "прозвище",
                                                     "answer_text": "Здесь должен "
                                                                    "быть какой-то "
                                                                    "текст ответа "
                                                                    "в тред"},
                                    "fourth_answer": {"answerer_name": f"4Тут имя "
                                                                       f"и через "
                                                                       "запятую "
                                                                       "прозвище",
                                                      "answer_text": "Здесь должен "
                                                                     "быть какой-то "
                                                                     "текст ответа "
                                                                     "в тред"}
                                    })
        return render_template('threads.html', title="Треды",
                               list_of_threads=list_of_threads)

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        last_threads = []
        profile_name = "Здесь имя профиля"
        post = "Тут какое-нибудь прозвище"
        for i in range(12):
            last_threads.append({"thread_name": "Свободное место",
                                 "thread_link": "Свободное место для ссылки"})
        if request.method == "POST":
            if request.form['button'] == "Главная":
                return redirect('/main')
            elif request.form['button'] == "Обсуждения":
                return redirect('/threads')
        return render_template('profile.html', title=profile_name,
                               profile_name=profile_name, last_threads=last_threads,
                               post=post)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
