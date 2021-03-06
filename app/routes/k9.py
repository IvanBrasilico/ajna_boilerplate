from ajna_commons.flask.log import logger
from flask import Blueprint, current_app, flash, render_template, request
from flask_login import login_required, current_user

from app.forms.k9_forms import DogForm, DogFiltroForm
from app.model.k9 import Dog

k9views = Blueprint('k9views', __name__)

NAOGOSTADECACHORRO = ['ogro', 'shrek']


@k9views.route('/dog', methods=['GET', 'POST'])
@login_required
def dog_id():
    session = current_app.config['db_session']
    dog = None
    oform = DogForm()
    try:
        if current_user.name in NAOGOSTADECACHORRO:
            raise Exception('Usuário proibido. Não gosta de cachorro!')
        if request.method == 'POST':
            oform = DogForm(request.form)
            if oform.validate():
                dog = Dog()
                dog.nome = oform.nome
                dog.formatura = oform.formatura
                session.add(dog)
                try:
                    session.commit()
                except Exception as err:
                    session.rollback()
                    raise err
            else:
                flash(oform)
        else:
            dog_id = request.args.get('id')
            if dog_id:
                dog = session.query(Dog).filter(Dog.id == dog_id).one_or_none()
                oform = DogForm(**dog.__dict__)
            if dog is None:
                flash('Cachorro não encontrado!')
    except Exception as err:
        logger.error(err, exc_info=True)
        flash(str(err))
    return render_template('dog.html', oform=oform)


@k9views.route('/pesquisa_dog', methods=['GET', 'POST'])
@login_required
def pesquisa_dog():
    session = current_app.config['db_session']
    oform = DogFiltroForm()
    dogs = []
    try:
        if request.method == 'POST':
            oform = DogFiltroForm(request.form)
            if oform.validate():
                dogs = session.query(Dog).filter(
                    Dog.nome.ilike(oform.nome.data + '%')).filter(
                    Dog.formatura.between(oform.datainicio.data, oform.datafim.data)
                ).all()
    except Exception as err:
        logger.error(err, exc_info=True)
        flash(str(err))
    return render_template('pesquisa_dog.html', oform=oform, dogs=dogs)


