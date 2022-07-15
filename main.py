from NodalAnalysis import calculate_branch_voltage, create_current_vector_from_network, calculate_node_voltages, create_node_admittance_matrix_from_network
from Network import load_network_from_json, load_network
import json
from SchemdrawWrapper import RealCurrentSource, Resistor, Line, Ground, parse_drawing, draw_volatages
from schemdraw import Drawing
import schemdraw

if __name__ == '__main__':

    network = load_network_from_json('./example_network_1.json')
    Y = create_node_admittance_matrix_from_network(network)
    I = create_current_vector_from_network(network)
    U = calculate_node_voltages(Y, I)

    n1, n2 = 1, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2):.2f}')
    n1, n2 = 1, 2
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2):.2f}')
    n1, n2 = 2, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2):.2f}')

    with open('./example_network_1.json', 'r') as json_file:
        network_definition = json.load(json_file)

    for branch in network_definition:
        branch['U'] = calculate_branch_voltage(U, branch['N1'], branch['N2'])
        if branch['type'] == "resistor":
            branch['I'] = branch['U']/branch['R']
        elif branch['type'] == "real_current_source":
            branch['Ui'] = branch['I'] * branch['R']
            branch['Us'] = branch['Ui'] + branch['U']
    print(json.dumps(network_definition, indent=2))

    
    with Drawing() as d:
        d += RealCurrentSource(I=1, R=100, name='I1').up()
        d += Resistor(R=10, name='R1').right()
        d += Resistor(R=20, name='R2').down()
        d += Line().left()
        d += Ground()
    #d.draw()
    network2 = load_network(parse_drawing(d))

    Y2 = create_node_admittance_matrix_from_network(network2)
    I2 = create_current_vector_from_network(network2)
    U2 = calculate_node_voltages(Y2, I2)

    n1, n2 = 1, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U2, n1, n2):.2f}')
    n1, n2 = 1, 2
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U2, n1, n2):.2f}')
    n1, n2 = 2, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U2, n1, n2):.2f}')

    draw_voltages()