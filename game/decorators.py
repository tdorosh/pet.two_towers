from .validators import validate_negative_args


def non_negative(func):
    def wrapper(*args, **kwargs):
        validate_negative_args(*args)
        return func(*args, **kwargs)

    return wrapper
