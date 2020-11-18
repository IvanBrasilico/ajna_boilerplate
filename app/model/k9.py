from sqlalchemy import Column, BigInteger, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Dog(Base):
    __tablename__ = 'k9_dogs'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(BigInteger().with_variant(Integer, 'sqlite'),
                primary_key=True)
    nome = Column(String(50))
    formatura = Column(DateTime)


if __name__ == '__main__':
    import sys

    sys.path.append('.')
    from app.config import Staging

    engine = Staging.sql
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
