from CircuitCalculator.Circuit.solution import TransientSolution
from CircuitCalculator.SignalProcessing.one_sided_functions import step
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit import components as cmp
import numpy as np

def test_transient_analysis_of_example_network_1() -> None:
    Vs = 1
    R1, R2, R3 = 10, 20, 30
    C = 1e-3
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
        cmp.resistor(id='R3', R=R3, nodes=('2', '3')),
        cmp.capacitor(id='C', C=C, nodes=('3', '0')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.0003
    t0 = 0.1
    t_max = 0.3
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0)}
    solution = TransientSolution(circuit, input=input, t_vec=t_vec)

    Ri = R1*R2/(R1+R2)+R3
    tau = Ri*C
    V = input['Vs'](solution.t)
    uC_ref = V*R2/(R1+R2)*(1-np.exp(-(solution.t-t0)/tau))
    iC_ref = C*V*R2/(R1+R2)/tau*np.exp(-(solution.t-t0)/tau)
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], uC_ref+R3*iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], R1*((uC_ref+R3*iC_ref)/R2+iC_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uC_ref+R3*iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R3')[1], R3*iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('C')[1], uC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -((uC_ref+R3*iC_ref)/R2+iC_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], ((uC_ref+R3*iC_ref)/R2+iC_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], (uC_ref+R3*iC_ref)/R2, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R3')[1], iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('C')[1], iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-((uC_ref+R3*iC_ref)/R2+iC_ref)), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], R1*((uC_ref+R3*iC_ref)/R2+iC_ref)*((uC_ref+R3*iC_ref)/R2+iC_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], (uC_ref+R3*iC_ref)*(uC_ref+R3*iC_ref)/R2, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R3')[1], R3*iC_ref*iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('C')[1], uC_ref*iC_ref, atol=1e-3)