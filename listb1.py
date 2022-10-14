# listb1.py
# Holds a 1 Based list class

# Imports
from collections.abc import Iterable
from typing import Any


# Definitions
class Listb1:
    """Creates a 1 based list, instead of the usual 0 based one"""

    # Variables
    l = []
    

    # Definitions
    def __init__(self, l: Iterable) -> None:
        self.l = list(l)
    
    def __iter__(self) -> list:
        return self.l
    
    def __getitem__(self, i: int) -> Any:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            return self.l[i-1]
        else:
            return self.l[i]
    
    def __setitem__(self, i: int, v: Any) -> None:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            self.l[i-1] = v
        else:
            self.l[i] = v
    
    def __str__(self) -> str:
        return f"Listb1({self.l})"
    
    def append(self, v: Any) -> None:
        self.l.append(v)
    
    def clear(self) -> None:
        self.l = []
    
    def copy(self) -> Any:
        return Listb1(self.l)
    
    def count(self, v: Any) -> int:
        return self.l.count(v)

    def extend(self, l: Iterable) -> None:
        self.l += list(l)
    
    def index(self, v: Any) -> int:
        return self.l.index(v) + 1

    def insert(self, i: int, v: Any) -> None:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            self.l.insert(i-1, v)
        else:
            self.l.insert(i, v)
    
    def pop(self, i: int) -> None:
        if i == 0:
            raise IndexError("list index out of range")
        elif i > 0:
            self.l.pop(i-1)
        else:
            self.l.pop(i)
    
    def remove(self, v: Any) -> None:
        self.l.remove(v)
    
    def reverse(self) -> None:
        self.l.reverse()
    
    def sort(self) -> None:
        self.l.sort()
