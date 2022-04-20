from data import db_session
from data.users import User
from data.threads import Threads
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from flask import Flask
from flask_login import LoginManager, login_user, current_user, login_required, \
    logout_user
from flask import render_template, request, redirect, url_for
import sqlite3
import base64
import json
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/main.db")
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
                db_sess.close_all()
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

    @app.route('/threads', methods=['GET', 'POST'])
    def threads():
        that = db_sess.query(Threads).all()
        list_of_threads = []
        for elem in that:
            answer = json.loads(elem.all_answers)['answers']
            photo = db_sess.query(User).filter(
                elem.author == User.login).first().photo
            if photo:
                f = open('static/img/profile.png', 'wb')
                f.write(photo)
                f.close()
            if len(answer) < 1:
                elem.first_answer = '-'
            else:
                elem.first_answer = answer[0]['text']
            if len(answer) < 2:
                elem.second_answer = '-'
            else:
                elem.second_answer = answer[1]['text']
            if len(answer) < 3:
                elem.third_answer = '-'
            else:
                elem.third_answer = answer[2]['text']
            if len(answer) < 4:
                elem.forth_answer = '-'
            else:
                elem.forth_answer = answer[3]['text']
            if len(answer) < 1:
                elem.first_author = '-'
            else:
                elem.first_author = answer[0]['author']
            if len(answer) < 2:
                elem.second_author = '-'
            else:
                elem.second_author = answer[1]['author']
            if len(answer) < 3:
                elem.third_author = '-'
            else:
                elem.third_author = answer[2]['author']
            if len(answer) < 4:
                elem.forth_author = '-'
            else:
                elem.forth_author = answer[3]['author']
            if db_sess.query(Threads).filter_by(title=elem.title).all()[0].photo:
                thread_image = base64.b64encode(db_sess.query(Threads).
                                                filter_by(title=elem.title).
                                                all()[0].photo).decode('utf-8')
            else:
                thread_image = None
            list_of_threads.append({"thread_name": elem.title,
                                    "author_picture": base64.
                                   b64encode(db_sess.query(User).
                                             filter_by(login=elem.author).all()[0].
                                             photo).decode('utf-8'),
                                    "author_name": elem.author,
                                    "thread_image": thread_image,
                                    "thread_text": elem.text,
                                    "first_answer": {
                                        "answerer_name": elem.first_answer,
                                        "answer_text": elem.first_author},
                                    "second_answer": {
                                        "answerer_name": elem.second_answer,
                                        "answer_text": elem.second_author},
                                    "third_answer": {
                                        "answerer_name": elem.third_answer,
                                        "answer_text": elem.third_author},
                                    "fourth_answer": {
                                        "answerer_name": elem.forth_answer,
                                        "answer_text": elem.forth_author}
                                    })
        if request.method == "POST":
            if request.form['button'] == "Главная":
                return redirect('/main')
            elif request.form['button'] == "Профиль":
                return redirect('/profile')
            elif request.form['button'] == "Создать тред":
                if current_user.is_authenticated:
                    return redirect('/make_thread')
                else:
                    return redirect('/register_or_login')
            elif "В тред" in request.form['button']:
                if current_user.is_authenticated:
                    return redirect(url_for('the_thread',
                                            number=request.form['button'][-1]))
                else:
                    return redirect('/register_or_login')
        return render_template('threads.html', title="Треды",
                               list_of_threads=list_of_threads)

    @app.route('/make_thread', methods=['GET', 'POST'])
    def make_thread():
        if request.method == "POST":
            f = request.files['file']
            t = f.read()
            thread_name = request.form['thread_name']
            thread_text = request.form['thread_text']
            answers = {'answers': []}
            if len(t) != 0:
                thread_new = Threads(title=thread_name,
                                     author=current_user.login,
                                     text=thread_text,
                                     photo=t,
                                     all_answers=json.dumps(answers))
            else:
                thread_new = Threads(title=thread_name,
                                     author=current_user.login,
                                     text=thread_text,
                                     all_answers=json.dumps(answers))
            db_sess.add(thread_new)
            db_sess.commit()
            return redirect('/threads')
        return render_template('make_thread.html', title="Создать тред")

    @app.route('/the_thread/<number>', methods=['GET', 'POST'])
    def the_thread(number):
        that = db_sess.query(Threads).filter_by(id=int(number)).all()[0]
        name = that.title
        users = db_sess.query(User).filter_by(login=that.author).all()[0]
        if that.photo:
            photo = base64.b64encode(that.photo).decode('utf-8')
        else:
            photo = None
        thread_head = {"author": that.author,
                       "avatar": base64.b64encode(users.photo).decode('utf-8'),
                       "text": that.text,
                       "photo": photo}
        answers_dict = json.loads(that.all_answers)
        thread_content = answers_dict["answers"]
        for elem in thread_content:
            elem["avatar"] = base64.b64encode(db_sess.query(User).
                                              filter_by(login=elem["author"]).
                                              all()[0].photo).decode('utf-8')
        if request.method == "POST":
            if "Ответить" in request.form['button']:
                listener = request.form['button'][9:]
                text = f"{listener},\n {request.form['answer']}"
                print(request.files)
                f = request.files['file']
                t = f.read()
                if len(t) != 0:
                    t = base64.b64encode(t).decode('utf-8')
                else:
                    t = None
                answers_dict["answers"].append({"author": current_user.login,
                                                "text": text, "photo": t})
                e = db_sess.query(Threads).get(number)
                e.all_answers = json.dumps(answers_dict)
                db_sess.add(e)
                db_sess.commit()
                return redirect(url_for('the_thread',
                                        number=number))

        return render_template('the_thread.html', title=name,
                               thread_head=thread_head,
                               thread_content=thread_content)

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        last_threads = []
        profile_name = current_user.login
        f = open('static/img/profile.png', 'wb')
        f.write(current_user.photo)
        f.close()
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
