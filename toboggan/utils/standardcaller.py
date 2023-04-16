# Standard
from functools import wraps

__all__ = ('StandardCaller',)


class StandardCaller:
    """Represents the standard caller for toboggan.decos that attach to methods.
    """
    
    def __call__(self, func):
        @wraps(func)
        def arg_handler(*args, **kwargs):
            args = args + (self,)
            return func(*args, **kwargs)
        return arg_handler
