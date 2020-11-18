from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

from app.model.k9 import Dog


class DogModel(ModelView):
    column_searchable_list = ['nome']
    column_list = ('nome', )
    form_columns = ('nome', 'formatura')


def admin_app(app, session):
    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'pt'

    admin = Admin(app, name='K9 RFB', template_mode='bootstrap3')
    # Add administrative views here
    admin.add_view(DogModel(Dog, session))
