"""
Tools
-----
General-purpose functions which can be used to simplify
expressions, the following tools are available:
- repeat
"""

from typing import Callable


def repeat(func: Callable, n_times: int) -> list[Callable]:
    return [func for _ in range(n_times)]