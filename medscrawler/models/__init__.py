import functools
from contextlib import contextmanager
from threading import local

from sqlalchemy import (
    create_engine as _create_engine,
    event,
)
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import (
    Session as _Session,
    sessionmaker as _sessionmaker,
    scoped_session
)

from config import db_config
from medscrawler.utils.func import arg2kwarg, inject_kwarg, adapt


def create_engine(username, password, host, port, database, drivername='postgres', echo=True, **kwargs):
    db_url = URL(
        drivername=drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
        query=kwargs,
    )
    return _create_engine(db_url, echo=echo)


db_engine = create_engine(**db_config, echo=True)


def scoped_sessionmaker(engine):
    class Session(_Session):
        def after_commit(self, func):
            event.listens_for(self, 'after_commit', once=True)(adapt(func))

        def after_rollback(self, func):
            event.listens_for(self, 'after_soft_rollback', once=True)(adapt(func))

    return scoped_session(
        _sessionmaker(
            class_=Session,
            bind=engine
        )
    )


DBSession = scoped_sessionmaker(db_engine)

_session_ctx = local()


@contextmanager
def transaction(session=None):
    session = session or DBSession()
    try:
        _session_ctx.in_transaction = True
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        _session_ctx.in_transaction = False
        session.close()


def transactional(func):
    """
    Make the wrapped function call transactional and inject session object if necessary.
    :param func: function to be wrapped
    :return: transactional function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs = arg2kwarg(func, args, kwargs)
        session = DBSession()
        if not getattr(_session_ctx, 'in_transaction', False):
            with transaction(session):
                kwargs = inject_kwarg(func, kwargs, 'session', session)
                return func(**kwargs)
        else:
            kwargs = inject_kwarg(func, kwargs, 'session', session)
            return func(**kwargs)

    return wrapper
