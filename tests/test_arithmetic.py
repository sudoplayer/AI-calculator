"""离线单元测试（不依赖 LLM / deepagents）。"""

import pytest

from skills.add.scripts.add import add
from skills.divide.scripts.divide import DivisionByZeroError, divide
from skills.multiply.scripts.multiply import multiply
from skills.subtract.scripts.subtract import subtract


def test_add():
    assert add(3, 5) == 8


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(8, 2) == 16


def test_divide():
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    with pytest.raises(DivisionByZeroError):
        divide(10, 0)
