from ..Network.network import Network
from ..Circuit.circuit import Circuit, transform

from . import Elements as elm
from .CircuitComponentTranslators import circuit_translator_map

from .DiagramParser import SchematicDiagramParser

from typing import List

def circuit_translator(schematic: elm.Schematic) -> Circuit:
    schematic_diagram = SchematicDiagramParser(schematic)
    return schematic_diagram.translate_elements(circuit_translator_map)