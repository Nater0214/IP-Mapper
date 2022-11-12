# global_methods.py
# Some useful methods that are used by multiple files
# These are in no particular order, just the order I implemented them


# Imports
from collections.abc import Iterable
from itertools import chain, groupby, tee
from typing import Any, Generator


# Definitions
class staticproperty(staticmethod):
    def __get__(self, *_):         
        return self.__func__()
    
    
def isntinstance(object_: object, type_: type | tuple[type]) -> bool:
    """
    Short for not isinstance()
    I just got tired of typing:
    >>> if not isinstance(obj_, type_):
    ...     pass
    So I made this
    
    Returns:
        bool # The opposite of isinstance(obj_, type_)
    
    Usage:
    >>> var1 = 1
    >>> var2 = '1'
    
    isntinstance(var1, int)
    False
    isntinstance(var2, int)
    True
    """
    
    return not isinstance(object_, type_)


def lazy_split(iter_: Iterable, split_num: int) -> list[Iterable]:
    
    """
    Splits an iterable lazily as not to use memory and computational power to store full list.
    Attempts to slice the iterable rather than actually iterating over it.

    Similar to:
    >>> import numpy
    >>> iter_ = [1, 2, 3, 4]
    >>> split_size = 2
    >>> numpy.array_split(iter_, split_size)
    [array([1, 2]), array([3, 4])]

    Credit to tixxit on Stack Overflow. https://stackoverflow.com/a/2135920
    """

    k, m = divmod(len(iter_), split_num)
    return [iter_[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(split_num)]


def all_equal(iter_: Iterable[Any]) -> bool:
    """
    Returns if all elements of a list are equal.

    Usage:
    >>> iter_ = [1, 1]
    >>> all_equal(iter_)
    True
    >>> iter_ = [1, 2]
    >>> all_equal(iter_)
    False

    Credit to kennytm on Stack Overflow. https://stackoverflow.com/a/3844832
    """
    
    g = groupby(iter_)
    return next(g, True) and not next(g, False)


def flatten_iter(iter_: Iterable[Iterable]) -> Iterable:
    """
    Flattens an iterable into an instance of itself.
    Output iterable type will be the type of the top iterable, regardless of the type(s) of inner iterables.
    Inner iterables can be of different types.

    Usage:
    >>> iter_ = [[1, 2], [3, 4]]
    >>> flatten_iter(iter_)
    [1, 2, 3, 4]
    """

    return iter_.__class__(chain.from_iterable(iter_))


def transpose_iter(iter_: Iterable[Iterable]) -> Iterable[Iterable]:
    """
    Transposes a 2d iterable into an instance of itself.
    Output types will be switched, so that the inner type is now the outer, and vice-versa.

    Usage:
    >>> iter_ = [(1, 2), (3, 4), (5, 6)]
    >>> transpose_iter(iter_)
    ([1, 3, 5], [2, 4, 6])
    """
    
    # Get classes
    out_cls = iter_.__class__
    if not all_same_type(iter_):
        raise TypeError("Inner iterables must have the same type")
    in_cls = iter_[0].__class__
    
    # Make sure all inner iterables have the same length
    if not all_equal([len(inner_iter) for inner_iter in iter_]):
        raise ValueError("Inner iterables must have the same length")
    
    out = []
    for i in range(len(iter_[0])):
        out.append(out_cls([inner_iter[i] for inner_iter in iter_]))
    
    return in_cls(out)


def all_same_type(iter_: Iterable[Any]) -> bool:
    """
    Returns if all the objects in an iterable are of the same type.

    Usage:
    >>> iter_ = [1, 1]
    >>> all_same_type(iter_)
    True
    >>> iter_ = [1, '1']
    >>> all_same_type(iter_)
    False
    """

    types = [type(item) for item in iter_]
    return all_equal(types)


def iter_2_items(iter_: Iterable[Any], *, return_last: bool = False) -> tuple[Any, Any]:
    """
    Yields an item from an iterable and the item after it
    
    Parameters:
        iter_: Iterable[Any] # The iterable to yield from
        return_last: bool = False # Return the last item of the iterable, along with None
    
    Yields:
        tuple[Any, Any] # The two elements of the iterable
    
    Usage:
    l = [1, 2, 3, 4]
    >>> for n, m in iter_2_items(l):
    ...     print(n, m)
    1 2
    2 3
    3 4
    """
    
    i = 0
    while i < len(iter_) - 1:
        yield iter_[i], iter_[i+1]
        i += 1
    
    if return_last:
        try:
            yield iter_[-1], None
        except IndexError:
            pass