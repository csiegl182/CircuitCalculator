from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor
from CircuitCalculator.Network.transformers import remove_unconnected_branches

def test_unconnected_branches_are_removed():
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('2', '3', resistor('R3', 30))
    branchD = Branch('3', '4', resistor('R4', 40))
    branchE = Branch('3', '5', resistor('R5', 50))
    branchF = Branch('a', 'b', resistor('R6', 60))
    network = Network([branchA, branchB, branchC, branchD, branchE, branchF])
    connected_network = remove_unconnected_branches(network)
    assert sorted(connected_network.branch_ids) == ['R1', 'R2', 'R3', 'R4', 'R5']

def test_empty_network_remains_empty():
    network = Network([])
    connected_network = remove_unconnected_branches(network)
    assert connected_network.branch_ids == []

def test_network_with_only_reference_node_remains_empty():
    network = Network([], reference_node_label='0')
    connected_network = remove_unconnected_branches(network)
    assert connected_network.branch_ids == []

def test_network_with_all_branches_connected():
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('1', '2', resistor('R2', 20))
    branchC = Branch('2', '3', resistor('R3', 30))
    network = Network([branchA, branchB, branchC])
    connected_network = remove_unconnected_branches(network)
    assert sorted(connected_network.branch_ids) == ['R1', 'R2', 'R3']

def test_network_with_unconnected_reference_node_is_empty():
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('1', '2', resistor('R2', 20))
    branchC = Branch('3', '4', resistor('R3', 30))  # Unconnected branch
    network = Network([branchA, branchB, branchC], reference_node_label='x')
    connected_network = remove_unconnected_branches(network)
    assert sorted(connected_network.branch_ids) == []