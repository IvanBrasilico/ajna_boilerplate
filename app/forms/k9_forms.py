from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField, IntegerField


class DogFiltroForm(FlaskForm):
    nome = StringField(u'Nome do cachorro',
                             default='')
    datainicio = DateField(u'Data de formatura - inicio periodo')
    datafim = DateField(u'Data de formatura - final periodo')


class DogForm(FlaskForm):
    id = IntegerField()
    nome = StringField(u'Nome do cachorro',
                             default='')
    formatura = DateField(u'Data de formatura')
