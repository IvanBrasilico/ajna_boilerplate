from ajna_commons.flask.log import logger
from ajna_commons.utils.api_utils import get_filtro_alchemy
from flask import Blueprint, current_app, request, jsonify

from app.forms.k9_forms import DogFiltroForm
from app.model.k9 import Dog

k9api = Blueprint('k9api', __name__)


@k9api.route('/api/pesquisa_dog', methods=['POST'])
def pesquisa_dog_api():
    session = current_app.config['db_session']
    dogs_dump = []
    status_code = 200
    try:
        print(request.json)
        oform = DogFiltroForm(**request.json)
        dogs = session.query(Dog).filter(
            Dog.nome.ilike(oform.nome.data + '%')).all()
        if len(dogs) == 0:
            status_code = 404
        dogs_dump = [dog.dump() for dog in dogs]
        print(dogs_dump)
    except Exception as err:
        logger.error(err, exc_info=True)
        return jsonify({'dogs': dogs_dump, 'error': str(err)}), 500
    return jsonify({'dogs': dogs_dump}), status_code


# Exemplo - utilizando uma rotina do ajna_commons
@k9api.route('/api/dogs', methods=['POST'])
def fichas():
    return get_filtro_alchemy(Dog, request.json)
