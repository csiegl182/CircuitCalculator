from CircuitCalculator.Circuit.circuit import Resistor, VoltageSource, Ground, transform

def test_list_of_circuit_elements_can_be_transformed_into_network_with_same_node_labels() -> None:
    elem1_nodes = ('1', '0')
    elem2_nodes = ('0', '1')
    circuit = [VoltageSource(V=1, nodes=elem1_nodes, id='V1'), Resistor(R=100, nodes=elem2_nodes, id='R1'), Ground(('0', ))]

    network = transform(circuit)
    assert elem1_nodes in [(b.node1, b.node2) for b in network.branches]
    assert elem2_nodes in [(b.node1, b.node2) for b in network.branches]

def test_list_of_circuit_elements_can_be_transformed_into_network_with_same_element_names() -> None:
    R = 100
    U = 1
    elem1_nodes = ('1', '0')
    elem2_nodes = ('0', '1')
    circuit = [VoltageSource(V=U, nodes=elem1_nodes, id='V1'), Resistor(R=R, nodes=elem2_nodes, id='R1'), Ground(('0', ))]

    network = transform(circuit)
    assert 'V1' in network.branch_ids
    assert 'R1' in network.branch_ids

def test_list_of_circuit_elements_can_be_transformed_into_network_with_same_element_values() -> None:
    R = 100
    U = 1
    elem1_nodes = ('1', '0')
    elem2_nodes = ('0', '1')
    circuit = [VoltageSource(V=U, nodes=elem1_nodes, id='V1'), Resistor(R=R, nodes=elem2_nodes, id='R1'), Ground(('0', ))]

    network = transform(circuit)
    assert network['R1'].element.Z == R
    assert network['V1'].element.U == U

def test_ground_node_is_transformed_into_network() -> None:
    R = 100
    U = 1
    elem1_nodes = ('1', '0')
    elem2_nodes = ('0', '1')
    circuit = [VoltageSource(V=U, nodes=elem1_nodes, id='V1'), Resistor(R=R, nodes=elem2_nodes, id='R1'), Ground(('1', ))]

    network = transform(circuit)
    assert network.is_zero_node('1') == True
