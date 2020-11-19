from collections import OrderedDict
from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, CHAR, event
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash

Base = declarative_base()


class BaseDumpable(Base):
    __abstract__ = True

    def dump(self, exclude=None, explode=False):
        dump = OrderedDict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        if exclude:
            for key in exclude:
                if dump.get(key):
                    dump.pop(key)
        return dump


class Usuario(Base):
    __tablename__ = 'ovr_usuarios'
    cpf = Column(CHAR(11), primary_key=True)
    nome = Column(CHAR(50), index=True)
    password = Column(CHAR(200))

    def __str__(self):
        return '{} - {}'.format(self.cpf, self.nome)

    def user_dict(self):
        return {'password': self.password, 'nome': self.nome}


@event.listens_for(Usuario.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


class Dog(BaseDumpable):
    __tablename__ = 'k9_dogs'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(BigInteger().with_variant(Integer, 'sqlite'),
                primary_key=True)
    nome = Column(String(50))
    formatura = Column(DateTime)

    @property
    def formatura_iso(self):
        return datetime.strftime(self.formatura, '%d-%m-%YT%H:%M:%S')

    def dump(self, exclude=None, explode=False):
        dumped = super().dump(exclude)
        dumped['formatura'] = self.formatura_iso
        return dumped


if __name__ == '__main__':
    import sys

    sys.path.append('.')
    from app.config import Staging

    engine = Staging.sql
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
