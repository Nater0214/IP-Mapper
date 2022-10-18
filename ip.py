# ip.py
# Useful IP objects to do things easier
# I understand that these may be unnecessarily complex, but it will only make it easier for future projects where I may need something like this


# Imports
from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from global_methods import isntinstance, iter_2_items
from typing_ import IPOverflowError, IPValueError, OctetIndexError


# Definitions
class IP:
    """An IP object"""

    IP = object

    # Init
    def __init__(self, a: int, b: int, c: int, d: int, *, force_create=False) -> None:
        # Set values
        self.a, self.b, self.c, self.d = a, b, c, d

        # Validate Values
        if not force_create:
            if self.a not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")

            if self.b not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")

            if self.c not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")

            if self.d not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")
    

    @staticmethod
    def from_index(index: int) -> IP:
        return IP(0,0,0,0) + index

    
    # Properties and similar methods
    @property
    def to_index(self) -> int:
        return self.b + self.a*256 + self.d*256**2 + self.c*256**3


    def __iter__(self) -> Iterable:
        return iter((self.a, self.b, self.c, self.d))
    

    def __str__(self) -> str:
        return f"{self.a}.{self.b}.{self.c}.{self.d}"
    

    def __repr__(self) -> str:
        return f"IP({self.a},{self.b},{self.c},{self.d})"
    

    def __getitem__(self, octet: str) -> int:
        # Return
        if octet == 'a':
            return self.a
        elif octet == 'b':
            return self.b
        elif octet == 'c':
            return self.c
        elif octet == 'd':
            return self.d
        else:
            raise OctetIndexError(f"Invalid octet: {octet}")
    

    # Arithmetic operations
    def __add__(self, other: int) -> IP:
        if isinstance(other, int):
            # Raise error if other is negative
            if other < 0:
                return self - -other
            
            # Get octet values
            a, b, c, d = self.a, self.b, self.c, self.d

            # Add c
            v, r = divmod(other, 256**3)
            c += v

            # Add d
            v, r = divmod(r, 256**2)
            d += v

            # Add a
            v, r = divmod(r, 256)
            a += v

            # Add b
            b += r

            # Carry b
            if b >= 256:
                b -= 256
                a += 1
            
            # Carry a
            if a >= 256:
                a -= 256
                d += 1
            
            # Carry d
            if d >= 256:
                d -= 256
                c += 1

            # Raise error if c should be carried
            if c >= 256:
                raise IPOverflowError(f"Adding results in an ip greater than 255.255.255.255: ({str(IP(a,b,c,d, force_create=True))})")

            # Return
            return IP(a, b, c, d)

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'IP' and '{other.__class__.__name__}'")

    
    def __iadd__(self, other: int) -> None:
        if isinstance(other, int):
            self = self + other
            return self

        else:
            raise TypeError(f"unsupported operand type(s) for +=: 'IP' and '{other.__class__.__name__}'")


    def __sub__(self, other: int | IP) -> IP:
        if isinstance(other, int): # Returns an IP with a lowered value by other
            # Raise error if other is negative
            if other < 0:
                return self + -other
            
            # Get octet values
            a, b, c, d = self.a, self.b, self.c, self.d

            # Subtract c
            v, r = divmod(other, 256**3)
            c -= v

            # Subtract d
            v, r = divmod(r, 256**2)
            d -= v

            # Subtract a
            v, r = divmod(r, 256)
            a -= v

            # Subtract b
            b -= r

            # Carry b
            if b < 0:
                b += 256
                a -= 1
            
            # Carry a
            if a < 0:
                a += 256
                d -= 1
            
            # Carry d
            if d < 0:
                d += 256
                c -= 1

            # Raise error if c should be carried
            if c < 0:
                raise IPOverflowError(f"Subtracting results in an ip less than 0.0.0.0: {str(IP(a,b,c,d, force_create=True))}")

            # Return
            return IP(a, b, c, d)
        
        elif isinstance(other, IP): # Returns the difference of self and other
            return (self['b'] - other['b']) + ((self['a'] - other['a']) * 256) + ((self['d'] - other['d']) * (256 ** 2)) + ((self['c'] - other['c']) * (256 ** 3))
        
        else: # Raise an exception
            raise TypeError(f"unsupported operand type(s) for -: 'IP' and '{other.__class__.__name__}'")


    def __isub__(self, other: int) -> None:
        if isinstance(other, int):
            self = self - other
            return self
        
        else:
            raise TypeError(f"unsupported operand type(s) for -=: 'IP' and '{other.__class__.__name__}'")
    

    # Comparison
    def __eq__(self, other: IP | Any) -> bool:
        try:
            if isntinstance(other, IP):
                raise TypeError
            
            return tuple(self) == tuple(other)

        except TypeError:
            return False
    

    def __ne__(self, other: IP | Any) -> bool:
        try:
            if isntinstance(other, IP):
                raise TypeError
            
            return tuple(self) != tuple(other)

        except TypeError:
            return True


    def __lt__(self, other: IP | Any) -> bool:
        try:
            if isntinstance(other, IP):
                raise TypeError
            
            return self.to_index < other.to_index

        except TypeError:
            return False
    

    def __le__(self, other: IP | Any) -> bool:
        return self < other or self == other
    

    def __gt__(self, other: IP | Any) -> bool:
        try:
            if isntinstance(other, IP):
                raise TypeError
        
            return self.to_index > other.to_index

        except TypeError:
            return False
    

    def __ge__(self, other: IP | Any) -> bool:
        return self > other or self == other


class IPrange:
    """An iterable range of ips"""

    # Init
    def __init__(self, start_ip: IP, stop_ip: IP, *, no_stop_sub_1: bool = False) -> None:
        # Ensure arguments are of valid type
        if isntinstance(start_ip, IP):
            raise TypeError(f"IPrange start ip must be of type IP, not {start_ip.__class__.__name__}")
        
        if isntinstance(stop_ip, IP):
            raise TypeError(f"IPrange stop ip must be of type IP, not {stop_ip.__class__.__name__}")

        # Set range values
        self._start_ip = start_ip
        self._stop_ip = stop_ip - int(not no_stop_sub_1)
        self._no_stop_sub_1 = no_stop_sub_1

        # Raise exception if start ip is ahead of stop ip; this object doesn't like that very much
        if start_ip > stop_ip:
            raise IPValueError(f"Start ip cannot be ahead in range than stop ip: ({str(start_ip)} > {str(stop_ip)})")
    

    # Properties and similar methods
    @property
    def start_ip(self) -> IP:
        return self._start_ip
    

    @property
    def stop_ip(self) -> IP:
        return self._stop_ip
    

    def __repr__(self) -> str:
        return f"IPrange({repr(self._start_ip)}, {repr(self._stop_ip + int(not self._no_stop_sub_1))}{', no_stop_sub_1=True' if self._no_stop_sub_1 else ''})"
    

    # Comparison
    def __eq__(self, other: IPrange) -> bool:
        try:
            if isntinstance(other, IPrange):
                raise TypeError
            
            return (self._start_ip == other._start_ip) and (self._stop_ip == other._stop_ip) and (self._no_stop_sub_1 == other._no_stop_sub_1)
        
        except TypeError:
            return False
    

    def __ne__(self, other: IPrange) -> bool:
        try:
            if isntinstance(other, IPrange):
                raise TypeError
            
            return (self._start_ip != other._start_ip) and (self._stop_ip != other._stop_ip) and (self._no_stop_sub_1 != other._no_stop_sub_1)
        
        except TypeError:
            return True
    

    # Iteration methods
    def __iter__(self) -> Iterable:
        self.iter_index = 0
        return self

    
    def __next__(self) -> IP:
        # Stop iteration if end
        if self.iter_index == len(self) - 1:
            raise StopIteration
        
        # Set out value
        out = self[self.iter_index]
        
        # Increment index
        self.iter_index += 1

        # Return
        return out
    

    # List-like methods
    def __getitem__(self, other: int | slice) -> IP | IPrange:
        # Return IP at index
        if isinstance(other, int):
            # Positive index
            if other >= 0:
                if other > len(self) - 1:
                    raise IndexError(f"Index out of range: {other}")
                
                return self._start_ip + other
            
            # Negative index
            elif other < 0:
                if other < -len(self):
                    raise IndexError(f"Index out of range: {other}")

                return self.stop_ip + other + 1
        
        elif isinstance(other, slice): # Return IPrange with indexes
            # Raise exception if slice has step; It doesn't work
            if other.step != None:
                raise IndexError("IPrange does not support stepped slicing")
            
            # Get start and end indexes from slice object
            start_index = other.start if other.start != None else 0
            stop_index = other.stop if other.stop != None else len(self) - 1
            if stop_index == len(self):
                if self[stop_index-1] == IP(255,255,255,255):
                    stop_index -= 1
                    last_ip = True
                else:
                    last_ip = False
            else:
                last_ip = False

            # Raise exception if slice is a reverse slice; It also doesn't work
            if start_index > stop_index:
                raise IndexError("IPrange does not support reverse slicing")
            
            # Return IPrange with indexes
            return IPrange(self[start_index], self[stop_index] + int(not self._no_stop_sub_1), no_stop_sub_1=last_ip)
        
        else:
            raise IndexError(f"Unsupported index type for IPrange: {other.__class__.__name__}")
    

    def __contains__(self, other: IP) -> bool:
        # Other must be an IP
        if isntinstance(other, IP):
            raise TypeError(f"IPrange can only check for IP inside of itself, not {other.__class__.__name__}")
        
        return self[0] <= other <= self[-1]
    

    def __len__(self) -> int:
        return self._stop_ip - self._start_ip + 1
        

class ComplexIPrange:
    """A complex range of multiple IPranges"""

    _ranges = []
    
    # Init
    def __init__(self, ranges: list[IPrange]) -> None:
        # Raise exception if any range is not an IPrange
        for range_ in ranges:
            if isntinstance(range_, IPrange):
                raise TypeError(f"Range type must be IPrange, not {range_.__class__.__name__}")
        
        # Add ranges one-by-one and check if any contain each other
        self._ranges = []
        for range_ in ranges:
            if self._ranges == []:
                self._ranges.append(range_)
            
            else:
                if range_[0] in self or range_[-1] in self or self[0] in range_ or self[-1] in range_:
                    raise IPValueError("Ranges cannot contain each other or parts of each other")
                else:
                    self._ranges.append(range_)
        
        self._ranges = sorted(self._ranges, key=lambda r: r[0])
        
        self._merge()


    # Properties and similar methods
    @property
    def ranges(self) -> list[IPrange]:
        return self._ranges
    

    def __repr__(self) -> str:
        return f"ComplexIPrange([{', '.join([repr(range_) for range_ in self._ranges])}])"
    

    # Iteration methods
    def __iter__(self) -> Iterable:
        self.iter_index = 0
        return self
    
    
    def __next__(self) -> IP:
        # Stop iteration if end
        if self.iter_index > len(self) - 1:
            raise StopIteration
        
        # Set out value
        out = self[self.iter_index]
        
        # Increment index
        self.iter_index += 1

        # Return
        return out


    # List-like methods
    def __getitem__(self, other: int | slice) -> IP | IPrange | ComplexIPrange:
        if isinstance(other, int):
            # Support negative indexing
            if other < 0:
                other = len(self) + other

            # Raise exception if index is out of range
            if other > len(self):
                raise IndexError(f"Index out of range: {other}")

            for range_ in self._ranges:
                if other > (len_ := len(range_)) - 1: # I <3 walrus operator. I rarely get to use it so im happy :D
                    other -= len_
                else:
                    return range_[other] 

        elif isinstance(other, slice):
            # Raise exception if slice has step; It doesn't work
            if other.step != None:
                raise IndexError("ComplexIPrange does not support stepped slicing")
            
            # Get start and end indexes from slice object
            start_index = other.start if other.start != None else 0
            stop_index = other.stop if other.stop != None else len(self) - 1
            if stop_index == len(self):
                if self[stop_index-1] == IP(255,255,255,255):
                    stop_index -= 1
                    last_ip = True
                else:
                    last_ip = False
            else:
                last_ip = False

            # Support negative indexing
            if start_index < 0:
                start_index = len(self) + start_index
            if stop_index < 0:
                stop_index = len(self) + stop_index
            
            # Raise exception if index is out of range
            if start_index > len(self) - 1:
                raise IndexError(f"Index out of range: {start_index}")
            if start_index < 0:
                raise IndexError(f"Index out of range: {start_index - len(self)}")
            if stop_index > len(self) - 1:
                raise IndexError(f"Index out of range: {stop_index}")
            if stop_index < 0:
                raise IndexError(f"Index out of range: {stop_index - len(self)}")

            # Raise exception if slice is a reverse slice; It also doesn't work
            if start_index > stop_index:
                raise IndexError("ComplexIPrange does not support reverse slicing")

            # Get start range and change start index appropriately
            for range_index, range_ in enumerate(self._ranges):
                if start_index > (len_ := len(range_)) - 1:
                    start_index -= len_
                else:
                    start_range = range_
                    start_range_index = range_index
                    break

            # Get stop range and change stop index appropriately
            for range_index, range_ in enumerate(self._ranges):
                if stop_index > (len_ := len(range_)) - 1:
                    stop_index -= len_
                else:
                    stop_range = range_
                    stop_range_index = range_index
                    break

            # If indexes are in same range return IPrange
            if start_range == stop_range:
                return IPrange(start_range[start_index], stop_range[stop_index], no_stop_sub_1=True)
            
            # Else return complex range
            else:
                # Create out list
                out_ranges: list[IPrange] = []

                # Append start range
                out_ranges.append(start_range[start_index:])
                
                # Append middle ranges
                for range_index in range(start_range_index + 1, stop_range_index):
                    out_ranges.append(self._ranges[range_index])
                
                # Append stop range
                out_ranges.append(stop_range[:stop_index])
                out_ranges[-1]._no_stop_sub_1 = last_ip

                return ComplexIPrange(out_ranges)
        
        else:
            raise IndexError(f"Unsupported index type for ComplexIPrange: {other.__class__.__name__}")
    

    def __contains__(self, other: IP) -> bool:
        # Other must be an IP
        if isntinstance(other, IP):
            raise TypeError(f"IPrange can only check for IP inside of itself, not {other.__class__.__name__}")
       
        return any([other in range_ for range_ in self._ranges])


    def __len__(self) -> int:
        return sum(len(range_) for range_ in self._ranges)
    

    def _merge(self) -> None:
        """Merges subranges that are directly next to each other"""

        def _(old_ranges: list[IPrange]) -> list[IPrange]:
            if len(old_ranges) == 1:
                return old_ranges
            
            else:
                new_ranges = []
                for range1, range2 in iter_2_items(old_ranges, True):
                    if range2 == None:
                        new_ranges.append(range1)
                    
                    elif range1[-1] + 1 == range2[0]:
                        new_ranges.append(IPrange(range1[0], range2[-1], no_stop_sub_1=True))
                        old_ranges.remove(range1)
                        old_ranges.remove(range2)
                    
                    else:
                        new_ranges.append(range1)
            
                return new_ranges
        
        new_ranges = _(self._ranges)
        prev_new_ranges = self._ranges
        while new_ranges != prev_new_ranges:
            prev_new_ranges = new_ranges
            new_ranges = _(new_ranges)
        
        self._ranges = new_ranges


    def inverted(self) -> ComplexIPrange:
        """Returns an inverted range that includes every ip not in the existing range"""

        out_ranges = []
        if self._ranges[0][0] != IP(0,0,0,0):
            out_ranges.append(IPrange(IP(0,0,0,0), self._ranges[0][0]))

        for range1, range2 in iter_2_items(self._ranges):
            out_ranges.append(IPrange(range1[-1]+1, range2[0]))
        
        if self._ranges[-1][-1] != IP(255,255,255,255):
            out_ranges.append(IPrange(self._ranges[-1][-1]+1, IP(255,255,255,255), no_stop_sub_1=True))
        
        return ComplexIPrange(out_ranges)