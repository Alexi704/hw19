from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.user import User
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns
from views.protected import protected_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def create_data(app, db):
    with app.app_context():
        db.create_all()

        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])


def register_extensions(app):
    db.init_app(app)
    api = Api(app)

    # api = Api(app, prefix='/api', doc='/docs')
    # prefix='/api' - дополнительный префикс, если надо вынести Api отдельно,
    # doc - ссылка по которой расположена документация по Api (swagger) (по умолчанию см. в корне)

    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(protected_ns)
    # create_data(app, db)


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True, use_reloader=False)
    # use_reloader=False предотвращает повторную запись в базу данных функции create_data()