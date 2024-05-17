from .exceptions import NegativeValueError


def validate_negative_args(*args):
    for arg in args:
        try:
            if arg < 0:
                raise NegativeValueError
        except TypeError:
            pass
