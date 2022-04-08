from flask import Flask, render_template, redirect, request
from forms.login_form import LoginForm
from flask_login import LoginManager, login_user
from data import db_session
from data.users import User
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()

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

    @login_manager.user_loader
    def load_user(user_id):
        return db_sess.query(User).get(user_id)

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

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
