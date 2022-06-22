from NodalAnalysis import *
import numpy as np

if __name__ == '__main__':
    Y = create_node_admittance_matrix([1/100, 1/20], [1/10])
    I = np.array([1, 0])

    U = calculate_node_voltages(Y, I)
    print(U)

    n1, n2 = 1, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2)}')
    n1, n2 = 1, 2
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2)}')
    n1, n2 = 2, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2)}')

    network = Network()
    network.add_branch(Branch(1, 0, real_currentsource(I=1, R=100)))
    network.add_branch(Branch(1, 2, resistor(10)))
    network.add_branch(Branch(2, 0, resistor(20)))

    Y2 = create_node_admittance_matrix_from_network(network)
    I2 = create_current_vector_from_network(network)

