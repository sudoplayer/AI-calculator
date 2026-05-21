"""两数除法。"""


class DivisionByZeroError(Exception):
    pass


def divide(a: float, b: float) -> float:
    if b == 0:
        raise DivisionByZeroError("除数不能为零")
    return a / b
