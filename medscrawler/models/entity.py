from sqlalchemy import Column, Integer, text
from sqlalchemy.ext.declarative import declarative_base

from medscrawler.models import DBSession
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
        return DBSession().query(mcs)

    @classmethod
    def all(mcs):
        return mcs.query().all()

    @classmethod
    def get(mcs, id_: int):
        return mcs.query().filter(mcs.id == id_).first()

    @classmethod
    def mget(mcs, ids_: list):
        subq = text('SELECT * FROM (VALUES {}) AS q (id_, order_)'.
                    format(','.join(['({},{})'.format(id_, order_) for order_, id_ in enumerate(ids_)]))). \
            columns(id_=Integer, order_=Integer). \
            alias('il')
        return mcs.query().join(subq, subq.c.id_ == mcs.id).order_by(subq.c.order_).all()

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
