class NegativeValueError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__("Non negative value.")


class PlayerResourceNonFoundError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__("Player resource not found.")
