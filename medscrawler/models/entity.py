from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

from medscrawler.models import Session, engine
from medscrawler.utils.str import decamelize

Base = declarative_base()
declarative_meta = type(Base)


class AutoTableMeta(declarative_meta):
    def __new__(cls, classname, bases, dict_):
        if '__tablename__' not in dict_ and not dict_.get('__abstract__', False):
            dict_['__tablename__'] = 'tb_{}'.format(decamelize(classname))
        return super().__new__(cls, classname, bases, dict_)


class Entity(Base, metaclass=AutoTableMeta):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @classmethod
    def query(mcs):
        return Session().query(mcs)

    @classmethod
    def all(mcs):
        return mcs.query().all()

    @classmethod
    def get(mcs, id_):
        return mcs.query().filter(mcs.id == id_).first()

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def json_dict(self):
        return {
            k: getattr(self, k) for k in self.columns
        }

    def __repr__(self):
        return "<{clazz}({spec})>".format(
            clazz=type(self).__name__,
            spec=', '.join(
                '{} = {}'.format(k, v) for k, v in self.json_dict.items()
            )
        )


Entity.metadata.create_all(engine)
