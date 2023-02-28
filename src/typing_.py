# typing.py.
# Contains dummy classes to make things look nicer


# Definitions
class IPValueError(ValueError): ...
class IPOverflowError(OverflowError): ...
class OctetIndexError(IndexError): ...

class SettingsError(ValueError): ...
class SliceError(Exception): ...
class IndexTypeError(TypeError, IndexError): ...