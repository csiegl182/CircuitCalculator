from NodalAnalysis import calculate_branch_voltage, create_current_vector_from_network, calculate_node_voltages, create_node_admittance_matrix_from_network
from Network import load_network_from_json, load_network
import json
from SchemdrawWrapper import RealCurrentSource, Resistor, Line, Ground, SchemdrawNetwork, draw_voltage
from schemdraw import Drawing
import schemdraw.elements as elm

if __name__ == '__main__':
    with Drawing() as d:
        d += RealCurrentSource(I=1, R=100, name='I1').up()
        d += (R1:=Resistor(R=10, name='R1').right())
        d += Resistor(R=20, name='R2').down()
        d += Line().left()
        d += Ground()
        elm.CurrentLabel().at(R1).label('fjdlka')
        schemdraw_network = SchemdrawNetwork(d)
        network2 = load_network(schemdraw_network.dependency_list)
        d += draw_voltage(schemdraw_network, 'R1')
