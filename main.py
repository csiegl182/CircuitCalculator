from NodalAnalysis import *

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
