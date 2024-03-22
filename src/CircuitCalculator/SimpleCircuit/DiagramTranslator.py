from dataclasses import dataclass
import schemdraw.elements
from ..Network.network import Network
from ..Circuit.circuit import Circuit, Component

from . import Elements as elm
from .CircuitComponentTranslators import circuit_translator_map
from .NetworkBranchTranslators import network_translator_map
from .SchemdrawTranslatorTypes import ElementTranslatorMap

from .DiagramParser import SchematicDiagramParser

class UnknownTranslator(Exception): pass

@dataclass
class DiagramTranslator:
    diagram_parser : SchematicDiagramParser
    translator_map : ElementTranslatorMap

    def __call__(self, element: schemdraw.elements.Element) -> Component | None:
        try:
            return self.translator_map[type(element)](element, tuple(map(self.diagram_parser._get_node_index, elm.get_nodes(element))))
        except KeyError:
            raise UnknownTranslator(f"Element '{type(element).__name__}' cannot be translated.")

def _remove_none(l: list) -> list:
    return [e for e in l if e is not None]

def circuit_translator(schematic: elm.Schematic) -> Circuit:
    parser = SchematicDiagramParser(schematic)
    translator = DiagramTranslator(parser, circuit_translator_map)
    return Circuit(_remove_none([translator(e) for e in parser.all_elements]))

def network_translator(schematic: elm.Schematic) -> Network:
    parser = SchematicDiagramParser(schematic)
    translator = DiagramTranslator(parser, network_translator_map)
    return Network(_remove_none([translator(e) for e in parser.all_elements]), parser.ground_label)