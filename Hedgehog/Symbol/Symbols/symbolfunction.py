from Hedgehog.Symbol.Symbols.symboltype import *

class SymbolFunction(HedgehogType):

    @staticmethod
    def makeable(name, argstructure=None, statementblock=None):
        def getfunc(f):
            def callable(cls, interpreter, args, trace):
                f(cls, interpreter, args, trace)

            hhfunc = SymbolFunction(name, argstructure, statementblock)
            hhfunc.__hh_call__ = callable

            return hhfunc
        return getfunc

    def __hh_repr__(self):
        return f"<Hedgehog function {self.name}@{hhidentify(self)}>"

    def __init__(self, name, argstructure=None, statementblock=None):
        self.name = name
        self.argstructure = argstructure
        self.statementblock = statementblock
        super().__init__(self.name)

    def __hh_call__(self, interpreter, args, trace):
        # Get old, make new
        og = interpreter.context.symboltable()
        new = interpreter.context.symboltable().child()

        # Change current to new
        interpreter.context.changesymboltable(new)
        result, error = interpreter.goto(self.statementblock)
        if error: return None, error

        # Change back to old symboltable
        interpreter.context.changesymboltable(og)

        return result, None