import matplotlib # type: ignore
matplotlib.use('Agg')
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramParser, UnknownElement
from CircuitCalculator.SimpleCircuit.Elements import CurrentSource, Resistor, Line, Schematic, round_node
import pytest

class SimpleDrawing:
    def __init__(self, show: bool = False) -> None:
        with Schematic(show=show) as d:
            d += (I1:=CurrentSource(I=1, name='I1').up())
            d += (R1:=Resistor(R=10, name='R1').right())
            d += (R2:=Resistor(R=20, name='R2').down())
            d += (R3:=Resistor(R=30, name='R3').at(R1.end).right())
            d += (L1:=Line().down())
            d += (L2:=Line().left())
            d += (L3:=Line().left())
        self.drawing = d
        self.I1 = I1
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3

def test_all_circuit_elements_can_be_accessed() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    circuit_elements = schemdraw_network.circuit_elements
    assert circuit_elements == [sd.I1, sd.R1, sd.R2, sd.R3, sd.L1, sd.L2, sd.L3]

def test_all_lines_can_be_accessed() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    lines = schemdraw_network.line_elements
    assert lines == [sd.L1, sd.L2, sd.L3]

def test_single_electrical_potential_node_is_identified() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    assert schemdraw_network._get_equal_electrical_potential_nodes(sd.I1.end) == set([sd.I1.end])


def test_equal_electrical_potential_nodes_are_identified() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    assert schemdraw_network._get_equal_electrical_potential_nodes(sd.I1.start) == set([round_node(n) for n in [sd.L1.start, sd.L1.end, sd.L2.start, sd.L2.end, sd.L3.start, sd.L3.end]])

def test_unique_nodes_are_identified() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    unique_nodes = schemdraw_network.unique_nodes
    assert len(unique_nodes) == 3

def test_unique_node_mapping_is_identified() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    node_mapping = schemdraw_network.unique_node_mapping
    assert len(set(node_mapping.values())) == 3

def test_mapping_for_all_nodes_is_generated() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    node_mapping = schemdraw_network.unique_node_mapping
    assert len(node_mapping) == 6

def test_element_identified_by_name() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    element = schemdraw_network.get_element('R1')
    assert type(element) == Resistor
    assert element.name == 'R1'

def test_unknown_element_name_raises_exception() -> None:
    sd = SimpleDrawing()
    schemdraw_network = SchematicDiagramParser(sd.drawing)
    with pytest.raises(UnknownElement):
        schemdraw_network.get_element('RX')
