"""Opções de configuração da aplicação."""

import os
import sys

from app.model.k9 import Usuario

COMMONS_PATH = os.path.join('..', 'ajna', 'commons')
sys.path.append(COMMONS_PATH)

from ajna_commons.flask.conf import SECRET, SQL_URI
from ajna_commons.flask.log import logger
from sqlalchemy import create_engine


class Production:  # pragma: no cover
    """Configuração do ambiente Produção."""

    TESTING = False
    SECRET = SECRET
    alchemy_class = Usuario
    try:
        sql = create_engine(SQL_URI,
                            pool_size=5, max_overflow=5, pool_recycle=3600)
    except TypeError as err:
        logger.error('Erro ao conectar no Banco de Dados (config.py - Production):')
        logger.error(str(err))


class Staging:
    """Configuração do ambiente de Staging (Servidor stage)."""

    TESTING = True
    SECRET = 'fraco'  # nosec
    sql = create_engine('sqlite:///teste.db')
    alchemy_class = Usuario


class Testing:
    """Configuração do ambiente de Testes."""

    TESTING = True
    SECRET = 'fraco'  # nosec
    sql = create_engine('sqlite:///:memory:')
    alchemy_class = Usuario
