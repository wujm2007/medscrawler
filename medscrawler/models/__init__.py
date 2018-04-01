import functools
from _threading_local import local
from contextlib import contextmanager
from inspect import signature

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_config

engine = create_engine('postgresql://{user}:{password}@{host}/{database}'.format(**db_config), echo=True)

Session = sessionmaker(bind=engine)

_session_ctx = local()


@contextmanager
def __session_scope():
    session = Session()
    try:
        _session_ctx.in_transaction = True
        _session_ctx.session = session
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        _session_ctx.in_transaction = False
        _session_ctx.session = None
        session.close()


def transactional(func):
    """
    Make the wrapped function call transactional and inject session object if necessary.
    :param func: function to be wrapped
    :return: transactional function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        for arg, param in zip(args, sig.parameters):
            kwargs[param] = arg
        if not getattr(_session_ctx, 'in_transaction', False):
            with __session_scope():
                if 'session' in sig.parameters:
                    kwargs['session'] = getattr(_session_ctx, 'session')
                return func(**kwargs)
        else:
            if 'session' in sig.parameters:
                kwargs['session'] = getattr(_session_ctx, 'session')
            return func(**kwargs)

    return wrapper
