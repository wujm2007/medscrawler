from sqlalchemy import Column, Integer, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import insert
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

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def unique_keys(self):
        table_args = getattr(self, '__table_args__', ())
        return [tuple(a.name for a in ta.columns) for ta in table_args if isinstance(ta, UniqueConstraint)]


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

    @classmethod
    def add(cls, **kwargs):
        attrs = {k: v for k, v in kwargs.items() if k in cls.columns}
        instance = cls(**attrs)
        DBSession().add(instance)
        DBSession().flush()
        return instance

    def update(self, **kwargs):
        cls = type(self)
        attrs = {k: v for k, v in kwargs.items() if k in cls.columns}
        for k, v in attrs.items():
            setattr(self, k, v)
        DBSession().add(self)
        DBSession().flush()
        return self

    @classmethod
    def upsert(cls, **kwargs):
        attrs = {k: v for k, v in kwargs.items() if k in cls.columns}

        for unique_keys in cls.unique_keys:
            if set(unique_keys) < set(attrs.keys()):
                upsert_keys = unique_keys
                break
        else:
            raise AttributeError

        upsert_stmt = insert(cls).values(**attrs).on_conflict_do_update(index_elements=upsert_keys, set_=attrs)
        DBSession().execute(upsert_stmt)
        DBSession().flush()

        # FIXME
        return cls.query_by_kwargs(**{k: v for k, v in attrs.items() if k in upsert_keys}).first().update(**attrs)

    @property
    def json_dict(self):
        cls = type(self)
        return {
            k: getattr(self, k) for k in cls.columns
        }

    def __repr__(self):
        return "<{clazz}({spec})>".format(
            clazz=type(self).__name__,
            spec=', '.join(
                '{} = {}'.format(k, v) for k, v in self.json_dict.items()
            )
        )
