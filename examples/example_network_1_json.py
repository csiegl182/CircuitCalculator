from CircuitCalculator.Network import load_network_from_json
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver
from CircuitCalculator.EquivalentSources import TheveninEquivalentSource, NortenEquivalentSource

if __name__ == '__main__':
    network = load_network_from_json('./examples/example_network_1.json')
    solution = nodal_analysis_solver(network)
    for branch in network.branches:
        print(f'{branch.node1}->{branch.node2} U={solution.get_voltage(branch):2.2f}V')
        print(f'{branch.node1}->{branch.node2} I={solution.get_current(branch):2.2f}A')


    print('Thevenin-equivalent sources')
    n1, n2 = '1', '0'
    thevenin = TheveninEquivalentSource(network, n1, n2)
    U, R = thevenin.U, thevenin.Z
    print(f'{n1}->{n2}: {U=:4.2f}V {R=:4.2f}Ohm')
    
    print('')
    print('Norten-equivalent sources')
    n1, n2 = '1', '0'
    norten = NortenEquivalentSource(network, n1, n2)
    I, G = norten.I, norten.Y
    print(f'{n1}->{n2}: {I=:4.2f}A {G=:4.2f}S')

    
    