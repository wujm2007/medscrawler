import functools
from inspect import signature


def arg2kwarg(func, args, kwargs):
    sig = signature(func)
    res = {k: v for k, v in kwargs.items()}
    for arg, param in zip(args, sig.parameters):
        res[param] = arg
    return res


def inject_kwarg(func, kwargs, k, v):
    sig = signature(func)
    res = {k: v for k, v in kwargs.items()}
    if k in sig.parameters:
        res[k] = v
    return res


def adapt(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs = arg2kwarg(func, args, kwargs)
        return func(**kwargs)

    return wrapper
