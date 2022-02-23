def allow_acces():
    def decorator(func):
        setattr(func, 'allow', True)
        return func

    return decorator
