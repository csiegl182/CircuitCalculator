from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis import nodal_analysis_solver
from CircuitCalculator.EquivalentSources import NortenEquivalentSource, TheveninEquivalentSource
from CircuitCalculator.PlottingTemplates import plot_norten_source, plot_thevenin_source

if __name__ == '__main__':
    network = load_network_from_json('./examples/example_network_10.json')
    solution = nodal_analysis_solver(network)
    for branch in network.branch_ids:
        print(f'{network[branch].node1}->{network[branch].node2} U={solution.get_voltage(branch):2.2f}V')
        print(f'{network[branch].node1}->{network[branch].node2} I={solution.get_current(branch):2.2f}A')

    plot_thevenin_source(
        source=TheveninEquivalentSource(network, node1='0', node2='3'),
        R_load=10
    )
    plot_norten_source(
        source=NortenEquivalentSource(network, node1='0', node2='3'),
        R_load=10
    )


    