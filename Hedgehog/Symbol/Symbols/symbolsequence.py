from Hedgehog.Symbol.Symbols.symboltype import *


class SymbolTupleSequence(HedgehogType):

    def __hh_repr__(self):
        return f'({", ".join([_.__hh_repr__() for _ in self.value])})'

    def __init__(self, value):
        super().__init__(value)


class SymbolListSequence(HedgehogType):

    def __hh_repr__(self):
        return f'[{", ".join([_.__hh_repr__() for _ in self.value])}]'

    def __init__(self, value):
        super().__init__(value)


class SymbolArraySequence(HedgehogType):

    def __hh_repr__(self):
        return f'<{", ".join([_.__hh_repr__() for _ in self.value])}>'

    def __init__(self, value, arraytype):
        self.arraytype = arraytype
        super().__init__(value)
