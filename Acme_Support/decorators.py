from functools import wraps
# custom_decorator

def method_decorator_adaptor(adapt_to, *decorator_args, **decorator_kwargs):
    print([i for i in decorator_args],decorator_kwargs)
    def decorator_outer(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            print([i for i in args])
            @adapt_to(*decorator_args, **decorator_kwargs)
            def adaptor(*args, **kwargs):
                return func(self, *args, **kwargs)
            return adaptor(*args, **kwargs)
        return decorator
    return decorator_outer