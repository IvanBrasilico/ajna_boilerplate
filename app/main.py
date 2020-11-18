import os
import sys

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_login import current_user
from flask_nav import Nav
from flask_nav.elements import View, Navbar
from flask_wtf import CSRFProtect
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.utils import redirect

from ajna_commons.flask import login
from ajna_commons.flask.user import DBUser
from app.config import Production


def create_app(config_class=Production):
    """Cria app básica e vincula todos os blueprints e módulos/extensões."""
    app = Flask(__name__)
    app.logger.info('Criando app')
    Bootstrap(app)
    nav = Nav(app)
    csrf = CSRFProtect(app)
    app.secret_key = config_class.SECRET
    app.config['SECRET_KEY'] = config_class.SECRET
    app.config['sql'] = config_class.sql
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=config_class.sql))
    app.config['db_session'] = db_session

    # app.register_blueprint(lambda)

    app.logger.info('Configurando login...')
    login.configure(app)
    # DBUser.alchemy_class = Usuario
    # DBUser.dbsession = db_session
    DBUser.dbsession = None

    app.logger.info('Configurando / e redirects')

    @nav.navigation()
    def mynavbar():
        """Menu da aplicação."""
        items = [View('Home', 'index')]
        if current_user.is_authenticated:
            items.append(View('Sair', 'commons.logout'))
        return Navbar('teste', *items)

    @app.route('/')
    def index():  # pragma: no cover
        if current_user.is_authenticated:
            return render_template('index.html')
        else:
            return redirect(url_for('commons.login'))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session = app.config.get('db_session')
        if db_session:
            db_session.remove()

    return app


if __name__ == '__main__':  # pragma: no cover
    app = create_app()
    print(app.url_map)
    app.run(port=5999)
