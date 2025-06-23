from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis.node_analysis import open_circuit_impedance

if __name__ == '__main__':
    network = load_network_from_json('./examples/test-networks/01_json-network/example_network_8.json')
    Rges = complex(open_circuit_impedance(network, '1', '2')).real
    print(f'{Rges=:4.2f}Ω')