from typing import Callable

cache = {}

def sync_caching(func: Callable):
    def wrapper(*args, **kwargs):
        values = (func.__name__,)+args+tuple(kwargs.values())
        if kwargs.get('cache',False):
            if cache.get(values,False):
                return cache[values]
            cache[values] = func(*args,**kwargs)
            return cache[values]
        else:
            cache.pop(values,None)
        return func(*args,**kwargs)
    return wrapper
            
def async_caching(func: Callable):
    async def wrapper(*args, **kwargs):
        values = (func.__name__,)+args+tuple(kwargs.values())
        if kwargs.get('cache',False):
            if cache.get(values,False):
                return cache[values]
            cache[values] = await func(*args,**kwargs)
            return cache[values]
        else:
            cache.pop(values,None)
        return await func(*args,**kwargs)
    return wrapper