from SchemdrawWrapper import SchemdrawNetwork
from SchemdrawWrapper import RealCurrentSource, Resistor, Ground, Line
import schemdraw

def setup_simple_drawing(show: bool = False) -> schemdraw.Drawing:
    with schemdraw.Drawing(show=show) as d:
        d += RealCurrentSource(I=1, R=1, name='I1').up()
        d += Resistor(R=1, name='R1').right()
        d += Resistor(R=1, name='R2').down()
        d += Line().left()
        d += Ground()
    return d

def test_unique_nodes_are_identified() -> None:
    schemdraw_network = SchemdrawNetwork(setup_simple_drawing())
    node_mapping = schemdraw_network.unique_node_mapping
    assert len(set(node_mapping.values())) == 3

def test_mapping_for_all_nodes_is_generated() -> None:
    schemdraw_network = SchemdrawNetwork(setup_simple_drawing())
    node_mapping = schemdraw_network.unique_node_mapping
    assert len(node_mapping) == 4
