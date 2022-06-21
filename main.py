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

