# global_methods.py
# Some useful methods that are used by multiple files
# These are in no particular order, just the order I implemented them


# Imports
from collections.abc import Iterable
from itertools import chain, groupby
from typing import Any

from numpy import transpose, array


# Definitions
def isntinstance(object_: object, type_: type | tuple[type]) -> bool:
    """
    Short code for:
    >>> if not isinstance(obj, type_):
    ...     pass

    I just got tired of typing the above so I made this.
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
    >>> iter_ = [[1, 2], [3, 4]]
    >>> transpose_iter(iter_)
    [[1, 3], [2, 4]]
    """

    # Get iter classes
    out_cls = iter_.__class__
    if not all_same_type(iter_):
        raise TypeError("Inner iterables must all be the same type")
    in_cls = iter_[0].__class__

    # Return
    return in_cls([out_cls(item) for item in transpose(array(iter_, dtype=object))])


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


def iter_2_items(iter_: Iterable[Any], return_last: bool = False) -> tuple[Any, Any]:
    """
    Generates an iterable that returns an item and the item directly after it
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