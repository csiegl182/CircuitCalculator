from Network import Network, resistor, Branch

def test_Network_knows_about_its_node_number() -> None:
    network = Network([Branch(0, 1, resistor(10))])
    assert network.number_of_nodes == 2

def test_Network_returns_branches_connected_to_node() -> None:
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    network = Network([branchA, branchB, branchC])
    assert network.branches_connected_to(node=2) == [branchB, branchC]

def test_Network_returns_branches_between_nodes() -> None:
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    branchD = Branch(0, 2, resistor(30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.branches_between(node1=0, node2=2) == [branchB, branchD]
    