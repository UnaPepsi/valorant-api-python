from typing import Callable

cache = {}

def sync_caching(func: Callable):
	def wrapper(*args, **kwargs):
		is_cached = kwargs.pop('cache',None)
		values = (func.__name__,)+args+tuple(kwargs.values())
		if is_cached:
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
		is_cached = kwargs.pop('cache',None)
		values = (func.__name__,)+args+tuple(kwargs.values())
		if is_cached:
			if cache.get(values,False):
				return cache[values]
			cache[values] = await func(*args,**kwargs)
			return cache[values]
		else:
			cache.pop(values,None)
		return await func(*args,**kwargs)
	return wrapper