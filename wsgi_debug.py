import logging
# Caminhos - recomendável ao invés disso usar links na produção
import sys

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

sys.path.append('.')
from app.config import Staging
from app.main import create_app

from ajna_commons.flask.user import DBUser

app = create_app(Staging)  # pragma: no cover Testing = SQLite
DBUser.dbsession = None  # Aceita autenticação fake (qqer username==password)

# Configura logs e proxy redirect
gunicorn_logger = logging.getLogger('gunicorn.debug')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
application = DispatcherMiddleware(app,
                                   {
                                       '/ajnabp': app
                                   })

if __name__ == '__main__':
    print(app.url_map)  # pragma: no cover
    run_simple('localhost', 5999, application, use_reloader=True, use_debugger=True)
