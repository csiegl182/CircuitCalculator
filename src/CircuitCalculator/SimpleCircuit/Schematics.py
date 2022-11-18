import schemdraw

from .Elements import CircuitElement, CircuitLabel

class UnsupportedElement(Exception): pass

class Schematic(schemdraw.Drawing):
    def __iadd__(self, element):
        if not isinstance(element, CircuitElement) and not isinstance(element, CircuitLabel):
            raise UnsupportedElement
        return super().__iadd__(element)