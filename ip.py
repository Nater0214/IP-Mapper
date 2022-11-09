# ip.py
# Useful IP objects to do things easier
# I understand that these may be unnecessarily complex, but it will only make it easier for future projects where I may need something like this


# Imports
from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from global_methods import isntinstance, iter_2_items
from typing_ import IndexTypeError, IPOverflowError, IPValueError, OctetIndexError, SliceError


# Definitions
class IP:
    """An IP object"""


    # Init
    def __init__(self, a: int, b: int, c: int, d: int, *, _force_create=False) -> None:
        """
        Creates an IP object with the given octet values
        
        Parameters:
            a: int # First octet
            b: int # Second octet
            c: int # Third octet
            d: int # Fourth octet
            _force_create: bool = False # Forces the creation of the object even if an octet is out of range
        
        Raises:
            ValueError # If an octet is out of range
        
        Usage:
        >>> IP(0,0,0,0)
        IP(0,0,0,0)
        >>> IP(1,0,0,0)
        IP(1,0,0,0)
        """
        # Set values
        self.a, self.b, self.c, self.d = a, b, c, d

        # Validate Values
        if not _force_create:
            if self.a not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")

            if self.b not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")

            if self.c not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")

            if self.d not in range(0, 256):
                raise ValueError("IP octet value must be in range: 0-255")


    @staticmethod
    def from_index(other: int) -> IP:
        """
        Returns an IP from a big index
        
        Parameters:
            other: int # The index of the IP
        
        Returns:
            IP # The out IP
        
        Raises:
            TypeError # If the index is not an integer
            IndexError # If the index is not in range 0-4294967295
        
        Usage:
        >>> IP.from_index(256)
        IP(1,0,0,0)
        >>> IP.from_index(4294967295)
        IP(255,255,255,255)
        """
        
        # Check for correct type
        if isntinstance(other, int):
            raise TypeError(f"Index must be of type int, not {other.__class__.__name__}")
        
        # Raise error if index not in valid range
        if other not in range(256**4):
            raise IndexError(f"Index expected to be in range 0-4294967295, not {other}")

        # Return IP
        return IP(0,0,0,0) + other
    
    
    @staticmethod
    @property
    def last_ip() -> IP:
        """
        Returns a dummy last IP
        
        Returns:
            IP # The dummy IP
        
        Usage:
        >>> IP.last_ip
        IP(0,0,256,0)
        """
        
        return IP(0,0,256,0, _force_create=True)


    # Properties and similar methods
    @property
    def to_index(self) -> int:
        """
        Converts the IP to an index
        
        Returns:
            int # The index of the IP
        
        Usage:
        >>> IP(0,0,0,0).to_index
        0
        >>> IP(1,0,0,0).to_index
        256
        """
        
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
                raise IPOverflowError(f"Adding results in an ip greater than 255.255.255.255: ({str(IP(a,b,c,d, _force_create=True))})")

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
                raise IPOverflowError(f"Subtracting results in an ip less than 0.0.0.0: {str(IP(a,b,c,d, _force_create=True))}")

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
    def __init__(self, start_ip: IP, stop_ip: IP) -> None:
        """
        Creates an iterable range of IPs
        
        Parameters:
            start_ip: IP # The start IP
            stop_ip: IP # The end IP
        
        Raises:
            TypeError # If either IP is not an IP
            IPValueError # If the start IP is ahead of the stop IP
        
        Usage:
        >>> ip1 = IP(0,0,0,0)
        >>> ip2 = IP(1,0,0,0)
        >>> for ip in IPrange(ip1, ip2):
        ...     print(ip)
        "0.0.0.0"
        "0.1.0.0"
        ...
        "0.254.0.0"
        "0.255.0.0"
        """
        
        # Ensure arguments are of valid type
        if isntinstance(start_ip, IP):
            raise TypeError(f"IPrange start ip must be of type IP, not {start_ip.__class__.__name__}")

        if isntinstance(stop_ip, IP):
            raise TypeError(f"IPrange stop ip must be of type IP, not {stop_ip.__class__.__name__}")

        # Set range values
        self._start_ip = start_ip
        self._stop_ip = stop_ip

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
        return f"IPrange({repr(self._start_ip)}, {repr(self._stop_ip)})"


    # Comparison
    def __eq__(self, other: IPrange) -> bool:
        try:
            if isntinstance(other, IPrange):
                raise TypeError

            return (self._start_ip == other._start_ip) and (self._stop_ip == other._stop_ip)

        except TypeError:
            return False


    def __ne__(self, other: IPrange) -> bool:
        try:
            if isntinstance(other, IPrange):
                raise TypeError

            return (self._start_ip != other._start_ip) and (self._stop_ip != other._stop_ip)

        except TypeError:
            return True


    # Iteration methods
    def __iter__(self) -> Iterable:
        self.iter_index = -1
        return self


    def __next__(self) -> IP:
        # Increment iter index
        self.iter_index += 1

        # Stop iteration if end
        if len(self) == 0:
            raise StopIteration
        if self.stop_ip == self[self.iter_index]:
            raise StopIteration

        # Return IP
        return self[self.iter_index]


    # List-like methods
    def __getitem__(self, other: int | slice) -> IP | IPrange:
        # Index
        if isinstance(other, int):
            # Positive index
            if other >= 0:
                # Check for out of range index
                if other > len(self) - 1:
                    raise IndexError(f"Index out of range: {other}")

                # Return IP
                return self._start_ip + other

            # Negative index
            elif other < 0:
                # Check for out of range index
                if other < -len(self):
                    raise IndexError(f"Index out of range: {other}")

                # Return IP
                return self.stop_ip + other

        # Slice
        elif isinstance(other, slice): # Return IPrange with indexes
            # Raise exception if slice has step; It doesn't work
            if other.step != None:
                raise SliceError("IPrange does not support stepped slicing")

            # Set original values
            og_start_index = other.start
            og_stop_index = other.stop

            # Get and adjust start and stop indexes from slice object
            start_index = og_start_index if other.start != None else 0
            stop_index = og_stop_index if other.stop != None else -1
            
            # Return IPrange with indexes
            try:
                return IPrange(self[start_index], self[stop_index])

            # Raise Slice Error if out of range
            except IndexError:
                raise SliceError(f"Slice invalid: [{og_start_index if og_start_index != None else ''}:{og_stop_index if og_stop_index != None else ''}]")

        # Type Error
        else:
            raise IndexTypeError(f"Unsupported index type for IPrange: {other.__class__.__name__}")


    def __contains__(self, other: IP) -> bool:
        # Other must be an IP
        if isntinstance(other, IP):
            raise TypeError(f"IPrange can only check for IP inside of itself, not {other.__class__.__name__}")

        return self[0] <= other <= self[-1]


    def __len__(self) -> int:
        return self._stop_ip - self._start_ip


class ComplexIPrange:
    """A complex range of multiple IPranges"""

    _ranges = []

    # Init
    def __init__(self, ranges: list[IPrange]) -> None:
        """
        Creates a complex range of multiple IPranges
        
        Parameters:
            ranges: list[IPrange] # A list of the ranges
        
        Raises:
            TypeError # If any of the ranges are not IPranges
            IPValueError # If any of the ranges contain each other
        
        Usage:
        >>> range1 = IPrange(IP(0,0,0,0), IP(1,0,0,0))
        >>> range2 = IPrange(IP(2,0,0,0), IP(3,0,0,0))
        >>> for ip in ComplexIPrange([range1, range2]):
        ...     print(ip)
        "0.0.0.0"
        "0.1.0.0"
        ...
        "0.255.0.0"
        "2.0.0.0"
        ...
        "2.254.0.0"
        "2.255.0.0"
        """
        
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
        # Index
        if isinstance(other, int):
            # Set original value
            og_other = other

            # Positive index
            if other >= 0:
                # Get out range and index
                out_range = None
                for range_ in self._ranges:
                    if other > ((len_ := len(range_)) - 1):
                        other -= len_
                    else:
                        out_range = range_
                        break

                # Check for error
                if out_range == None:
                    raise IndexError(f"Index out of range: {og_other}")

                # Return IP
                return out_range[other]

            # Negative index
            elif other < 0:
                # Get out range and index
                og_other = other
                out_range = None
                for range_ in self._ranges[::-1]:
                    if -other > ((len_ := len(range_)) - 1):
                        other += len_
                    else:
                        out_range = range_
                        break

                # Check for error
                if out_range == None:
                    raise IndexError(f"Index out of range: {og_other}")

                # Return IP
                return out_range[other]

        # Slice
        elif isinstance(other, slice):
            # Raise exception if slice has step; It doesn't work
            if other.step != None:
                raise IndexError("ComplexIPrange does not support stepped slicing")

            # Set original values
            og_start_index = other.start
            og_stop_index = other.stop

            # Get start and stop indexes from slice object
            start_index = og_start_index if og_start_index != None else 0
            stop_index = None if og_stop_index == 0 else og_stop_index - 1 if og_stop_index != None else len(self) - 1

            # Get ranges and indexes
            start_range = None
            stop_range = None

            # Start index and range
            # Positive start index
            if start_index >= 0:
                # Get range and index
                for range_ in self._ranges:
                    if start_index > ((len_ := len(range_)) - 1):
                        start_index -= len_
                    else:
                        start_range = range_
                        break

            # Negative start index
            elif start_index < 0:
                # Get range and index
                for range_ in self._ranges[::-1]:
                    if -start_index > ((len_ := len(range_)) - 1):
                        start_index += len_
                    else:
                        start_range = range_
                        break

            # Stop index and range
            # Positive stop index
            if stop_index >= 0:
                # Get range and index
                for range_ in self._ranges:
                    if stop_index > ((len_ := len(range_)) - 1):
                        stop_index -= len_
                    else:
                        stop_range = range_
                        break

            # Negative stop index
            elif stop_index < 0:
                # Get range and index
                for range_ in self._ranges[::-1]:
                    if -stop_index > ((len_ := len(range_)) - 1):
                        stop_index += len_
                    else:
                        stop_range = range_
                        break

            # Check for errors
            if start_range == None or stop_range == None:
                raise SliceError(f"Slice out of range [{og_start_index if og_start_index != None else ''}:{og_stop_index if og_stop_index != None else ''}]")

            # If ranges are the same then return an IPrange
            if start_range == stop_range:
                return IPrange(start_range[start_index], stop_range[stop_index])

            # Else return a ComplexIPrange
            else:
                # Initialize out ranges
                out_ranges = []

                # Append first range
                out_ranges.append(start_range[start_index:])

                # Append middle ranges
                for i in range(self._ranges.index(start_range) + 1, self._ranges.index(stop_range)):
                    out_ranges.append(self._ranges[i])

                # Append stop range
                out_ranges.append(stop_range[:stop_index])

                # Return ComplexIPrange with out ranges
                return ComplexIPrange(out_ranges)

        # Type Error
        else:
            raise IndexTypeError(f"Unsupported index type for ComplexIPrange: {other.__class__.__name__}")


    def __contains__(self, other: IP) -> bool:
        # Other must be an IP
        if isntinstance(other, IP):
            raise TypeError(f"IPrange can only check for IP inside of itself, not {other.__class__.__name__}")

        return any([other in range_ for range_ in self._ranges])


    def __len__(self) -> int:
        return sum(len(range_) for range_ in self._ranges)


    def _merge(self) -> None:
        """
        Merges subranges that are directly next to each other
        """

        def _(old_ranges: list[IPrange]) -> list[IPrange]:
            if len(old_ranges) == 1:
                return old_ranges

            else:
                new_ranges = []
                for range1, range2 in iter_2_items(old_ranges, True):
                    if range2 == None:
                        new_ranges.append(range1)

                    elif range1[-1] + 1 == range2[0]:
                        new_ranges.append(IPrange(range1[0], range2[-1] + 1))
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
        """
        Returns an inverted range that includes every ip not in the existing range
        
        Returns:
            ComplexIPrange # The inverted range
        
        Usage:
        crange1 = ComplexIPrange(IPrange(IP(1,0,0,0), IP(2,0,0,0)), IPrange(IP(3,0,0,0), IP(4,0,0,0)))
        """

        out_ranges = []
        if self._ranges[0][0] != IP(0,0,0,0):
            out_ranges.append(IPrange(IP(0,0,0,0), self._ranges[0][0]))

        for range1, range2 in iter_2_items(self._ranges):
            out_ranges.append(IPrange(range1[-1]+1, range2[0]))

        if self._ranges[-1][-1] != IP(255,255,255,255):
            out_ranges.append(IPrange(self._ranges[-1][-1]+1, IP.last_ip))

        return ComplexIPrange(out_ranges)
