import types
import sklearn.externals.joblib

default_memory = sklearn.externals.joblib.Memory(cachedir = 'cache')

def return_self_from_bound(f):
    def f_return_self(*args, **kwargs):
        return f(*args, **kwargs), f.__self__
    return f_return_self

def cachable_with_self(mutable, attr, f, memory):

    def f_cached(*args, **kwargs):
        func = memory.cache(return_self_from_bound(f))
        ret, self = func(*args, **kwargs)
        mutable.__setattr__(attr, self)
        return ret

    return f_cached


class Cached(object):
    PROXIED = '__proxied__'

    def __init__(self, proxied):
        self.__dict__[self.__class__.PROXIED] = proxied

    def get_params(self, deep = False):
        return { 'proxied' : self.__getattr__(self.__class__.PROXIED) }

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
            return

        return setattr(self.__getattr__(self.__class__.PROXIED), name, value)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        attribute = getattr(self.__getattr__(self.__class__.PROXIED), name)

        if type(attribute) != types.MethodType:
            return attribute

        self.__dict__[name] = cachable_with_self( self
                                                , self.__class__.PROXIED
                                                , attribute
                                                , default_memory )

        return self.__dict__[name]
