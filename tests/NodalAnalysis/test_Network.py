from NodalAnalysis import Network, resistor, Branch

def test_Network_knows_about_its_node_number() -> None:
    network = Network()
    network.add_branch(Branch(0, 1, resistor(10)))
    assert network.number_of_nodes == 2

def test_Network_returns_branches_connected_to_node() -> None:
    network = Network()
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    network.add_branch(branchA)
    network.add_branch(branchB)
    network.add_branch(branchC)
    assert network.branches_connected_to_node(2) == [branchB, branchC]
    