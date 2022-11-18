import schemdraw

from .Elements import CircuitElement

class UnsupportedElement(Exception): pass

class Schematic(schemdraw.Drawing):
    def __iadd__(self, element):
        if not isinstance(element, CircuitElement) and not isinstance(element, schemdraw.elements.Element):
            raise UnsupportedElement
        return super().__iadd__(element)