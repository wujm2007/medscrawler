from sqlalchemy import Column, Integer, text
from sqlalchemy.ext.declarative import declarative_base

from medscrawler.models import DBSession, db_engine
from medscrawler.utils.str import decamelize

Base = declarative_base()
declarative_meta = type(Base)


class AutoTableMeta(declarative_meta):
    def __new__(cls, classname, bases, dict_):
        if '__tablename__' not in dict_ and not dict_.get('__abstract__', False):
            dict_['__tablename__'] = 'tb_{}'.format(decamelize(classname))
        return super().__new__(cls, classname, bases, dict_)

    def __init__(self, classname, bases, dict_):
        super().__init__(classname, bases, dict_)
        if not dict_.get('__abstract__', False):
            self.metadata.tables[self.__tablename__].create(db_engine, checkfirst=True)


class Entity(Base, metaclass=AutoTableMeta):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @classmethod
    def query(cls):
        return DBSession().query(cls)

    @classmethod
    def query_by_kwargs(cls, **kwargs):
        q = DBSession().query(cls)
        for k, v in kwargs.items():
            q = q.filter(getattr(cls, k) == v)
        return q

    @classmethod
    def all(cls):
        return cls.query().all()

    @classmethod
    def get(cls, id_: int):
        return cls.query().filter(cls.id == id_).first()

    @classmethod
    def mget(cls, ids_: list):
        il = text('SELECT * FROM (VALUES {}) AS q (id_, order_)'.
                  format(','.join(['({},{})'.format(id_, order_) for order_, id_ in enumerate(ids_)]))). \
            columns(id_=Integer, order_=Integer). \
            alias('il')
        return cls.query().join(il, il.c.id_ == cls.id).order_by(il.c.order_).all()

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
