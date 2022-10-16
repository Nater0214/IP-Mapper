# listb1.py
# Holds a 1 Based list class

# Imports
from collections.abc import Iterable
from typing import Any


# Definitions
class Listb1(list):
    """Creates a 1 based list, instead of the usual 0 based one"""
    
    def __getitem__(self, i: int) -> Any:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            return super().__getitem__(i-1)
        else:
            return super().__getitem__(i)
    
    def __setitem__(self, i: int, val: Any) -> None:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            super().__setitem__(i-1)
        else:
            self.l[i] = val
       
    def copy(self) -> Any:
        return Listb1(super().copy()())
    
    def index(self, val: Any) -> int:
        return super().index(val) + 1

    def insert(self, i: int, val: Any) -> None:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            super().insert(i-1, val)
        else:
            super().insert(i, val)
    
    def pop(self, i: int) -> None:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            super().pop(i-1)
        else:
            super().pop(i)