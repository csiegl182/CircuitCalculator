import matplotlib
matplotlib.use('Agg')
from CircuitCalculator.SimpleCircuit.Elements import Resistor, Schematic, LabelNode
from CircuitCalculator.SimpleCircuit.DiagramTranslator import circuit_translator

def test_network_transformation_keeps_node_names() -> None:
    with Schematic(show=False) as d:
        d += LabelNode(name='4', id_loc='S')
        d += Resistor(R=10, name='R1').right()
        d += LabelNode(name='5', id_loc='S')
        d += Resistor(R=20, name='R2').down()
        d += Resistor(R=20, name='R3').left()
        d += Resistor(R=20, name='R4').up()
    circuit = circuit_translator(d)
    assert circuit['R1'].nodes == ('4', '5')