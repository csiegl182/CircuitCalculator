from ..Network.network import Network
from ..Circuit.circuit import Circuit, transform

from . import Elements as elm
from .CircuitComponentTranslators import circuit_translator_map

from .DiagramParser import SchematicDiagramParser

from typing import List

def circuit_translator(schematic: elm.Schematic) -> Circuit:
    schematic_diagram = SchematicDiagramParser(schematic)
    return schematic_diagram.translate_elements(circuit_translator_map)

def network_translator(schematic: elm.Schematic, w: List[float] = []) -> List[Network]:
    circuit = circuit_translator(schematic)
    if len(w) == 0:
        w = circuit.w
    return transform(circuit=circuit, w=w)

def dc_network_translator(schematic: elm.Schematic) -> Network:
    return network_translator(schematic, w=[0])[0]