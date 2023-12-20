from CircuitCalculator.Network.NodalAnalysis.transient_analysis import TransientAnalysisSolution
from CircuitCalculator.Network.NodalAnalysis.state_space_model import BranchValues
from CircuitCalculator.SignalProcessing.one_sided_functions import step
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, open_circuit, resistor
import functools
import numpy as np

def test_solution_of_example_network_1() -> None:
    Vs = 1
    R1, R2, R3 = 10, 20, 30
    C = 1e-3
    network = Network([
        Branch('1', '0', voltage_source('Vs', V=Vs)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '0', resistor('R2', R=R2)),
        Branch('2', '3', resistor('R3', R=R3)),
        Branch('3', '0', open_circuit('C'))
    ])
    Ri = R3+R1*R2/(R1+R2)
    tau = Ri*C
    solution = TransientAnalysisSolution(network, c_values=[BranchValues(C, '3', '0')], input={'Vs': functools.partial(step, t0=0.1)}, t_lim=(0, 0.5), Ts=1e-4)
    t = solution.time
    uc_ref = np.zeros(t.size)
    uc_ref[t>0.1] = Vs*R2/(R1+R2)*(1-np.exp(-(t[t>0.1]-0.1)/tau))
    ic_ref = np.zeros(t.size)
    ic_ref[t>0.1] = Vs*R2/(R1+R2)*C/tau*np.exp(-(t[t>0.1]-0.1)/tau)
    np.testing.assert_allclose(solution.get_voltage('C'), uc_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1'), R1*((uc_ref+R3*ic_ref)/R2+ic_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2'), uc_ref+R3*ic_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R3'), R3*ic_ref, atol=1e-3)