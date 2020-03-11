from flask import Flask, redirect, render_template, session
from flask_login import LoginManager, login_user

from data import db_session
from data import news_api
from data.news import News
from data.users import User
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(news_api.blueprint)
    # добавление первого пользователя в бд
    # user = User()
    # user.name = "user1"
    # user.about = "биография пользователя 1"
    # user.email = "1@e.ru"
    # session = db_session.create_session()
    # session.add(user)
    # session.commit()
    # добавление первой новости первого пользователя в бд
    # news = News(title="Первая новость", content="Привет блог!",
    #             user_id=1, is_private=False)
    # session = db_session.create_session()
    # session.add(news)
    # session.commit()

    # session = db_session.create_session()
    # user = session.query(User).filter(User.id == 1).first()
    # news = News(title="Личная запись", content="Эта запись личная",
    #             is_private=True)
    # user.news.append(news)
    # session.commit()
    app.run()


if __name__ == '__main__':
    main()