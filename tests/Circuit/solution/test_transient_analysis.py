from CircuitCalculator.Circuit.solution import TransientSolution
from CircuitCalculator.SignalProcessing.one_sided_functions import step
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit import components as cmp
import numpy as np

def quad_equation(a, b, c):
    D = np.sqrt(b**2-4*a*c)
    return ((-b+D)/2/a, (-b-D)/2/a)

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
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    Ri = R1*R2/(R1+R2)+R3
    tau = Ri*C
    V = input['Vs'](solution.t)
    uC_ref = V*R2/(R1+R2)*(1-np.exp(-(solution.t-t0)/tau))
    iC_ref = C*V*R2/(R1+R2)/tau*np.exp(-(solution.t-t0)/tau)
    uR3_ref = R3*iC_ref
    uR2_ref = uR3_ref + uC_ref
    uR1_ref = V - uR2_ref
    iR1_ref = uR1_ref/R1
    iR2_ref = uR2_ref/R2
    iR3_ref = uR3_ref/R3
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('C')[1], uC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R3')[1], iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('C')[1], iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R3')[1], uR3_ref*iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('C')[1], uC_ref*iC_ref, atol=1e-3)

def test_transient_analysis_of_example_network_2() -> None:
    Vs = 5
    R1, R2, R3 = 10, 20, 30
    C = 1e-3
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
        cmp.capacitor(id='C', C=C, nodes=('2', '3')),
        cmp.resistor(id='R3', R=R3, nodes=('3', '0')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.00003
    t_max = 0.3
    t0 = 0.1
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    tau = C*(R1*R2+R1*R3+R2*R3)/(R1+R2)
    V = input['Vs'](solution.t)
    uC_ref = V*R2/(R1+R2)*(1-np.exp(-(solution.t-t0)/tau))
    iC_ref = C*V*R2/(R1+R2)/tau*np.exp(-(solution.t-t0)/tau)
    uR3_ref = iC_ref*R3
    uR2_ref = uC_ref + uR3_ref
    uR1_ref = V - uR2_ref
    iR1_ref = uR1_ref/R1
    iR2_ref = uR2_ref/R2
    iR3_ref = uR3_ref/R3
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('C')[1], uC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R3')[1], iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('C')[1], iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R3')[1], uR3_ref*iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('C')[1], uC_ref*iC_ref, atol=1e-3)

def test_transient_analysis_of_example_network_3() -> None:
    Vs = 5
    Is = -0.1
    R1, R2 = 10, 20
    C = 1e-3
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.capacitor(id='C', C=C, nodes=('2', '3')),
        cmp.resistor(id='R2', R=R2, nodes=('3', '0')),
        cmp.dc_current_source(id='Is', I=Is, nodes=('0', '3')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.00003
    t_max = 0.3
    t0 = 0.1
    t1 = 0.2
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0), 'Is': lambda t: Is*step(t, t0=t1)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    Ri = R1+R2
    tau = Ri*C
    V = input['Vs'](solution.t)
    I = input['Is'](solution.t)
    t = solution.t
    uC_ref = np.zeros(t.size)
    uC_ref[t>t0] = Vs*(1-np.exp(-(t[t>t0]-t0)/tau))
    uC_ref[t>t1] = uC_ref[t>t1] - Is*R2*(1-np.exp(-(t[t>t1]-t1)/tau))
    iC_ref = np.zeros(t.size)
    iC_ref[t>t0] = C*Vs*(-np.exp(-(t[t>t0]-t0)/tau))*(-1/tau)
    iC_ref[t>t1] = iC_ref[t>t1] - C*Is*R2*(-np.exp(-(t[t>t1]-t1)/tau))*(-1/tau)
    phi2_ref = -iC_ref*R1 + V
    uR1_ref = V - phi2_ref
    uR2_ref = (iC_ref + I)*R2
    iR1_ref = uR1_ref/R1
    iR2_ref = uR2_ref/R2
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], phi2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('C')[1], uC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Is')[1], -uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('C')[1], iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Is')[1], I, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('C')[1], uC_ref*iC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Is')[1], (-uR2_ref)*I, atol=1e-3)

def test_transient_analysis_of_example_network_4() -> None:
    Vs = 1
    R1, R2 = 10, 20
    C1 = 5e-3
    C2 = 1e-3
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.capacitor(id='C1', C=C1, nodes=('2', '3')),
        cmp.resistor(id='R2', R=R2, nodes=('3', '0')),
        cmp.capacitor(id='C2', C=C2, nodes=('3', '0')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.00003
    t_max = 0.5
    t0 = 0.1
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)
    
    a = C2*R2
    b = C1*R1
    c = C1*R2
    s1, s2 = quad_equation(1, (a+b+c)/a/b, 1/a/b)
    s3, s4 = quad_equation(1, (a+b+c)/a/b, 1/a/b)
    t = solution.t
    t_ref = t[t>t0]-t0
    V = input['Vs'](t)
    uC1_ref = np.zeros(t.size)
    uC1_ref[t>t0] = Vs/a/b * (1/s1/s2 + 1/(s2-s1)*(-1/s1*np.exp(s1*t_ref)+1/s2*np.exp(s2*t_ref))) + Vs/b * 1/(s1-s2) * (np.exp(s1*t_ref)-np.exp(s2*t_ref))
    uC2_ref = np.zeros(t.size)
    uC2_ref[t>t0] = Vs*c/a/b * (np.exp(s3*t_ref)-np.exp(s4*t_ref))/(s3-s4)
    phi2_ref = uC1_ref + uC2_ref
    uR1_ref = V - phi2_ref
    uR2_ref = uC2_ref
    iR1_ref = uR1_ref/R1
    iR2_ref = uR2_ref/R2
    iC1_ref = np.zeros(t.size)
    iC1_ref[t>t0] = C1*Vs/a/b * (1/(s2-s1)*(-np.exp(s1*t_ref)+np.exp(s2*t_ref))) + C1*Vs/b * 1/(s1-s2) * (np.exp(s1*t_ref)*s1-np.exp(s2*t_ref)*s2)
    iC2_ref = np.zeros(t.size)
    iC2_ref[t>t0] = C2*Vs*c/a/b * (np.exp(s3*t_ref)*s3-np.exp(s4*t_ref)*s4)/(s3-s4)
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], phi2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uC2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('C1')[1], uC1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('C2')[1], uC2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('C1')[1], iC1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('C2')[1], iC2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('C1')[1], uC1_ref*iC1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('C2')[1], uC2_ref*iC2_ref, atol=1e-3)

def test_transient_analysis_of_example_network_5() -> None:
    Vs = 5
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
        cmp.resistor(id='R3', R=R3, nodes=('2', '3')),
        cmp.inductance(id='L', L=L, nodes=('3', '0')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.000001
    t_max = 0.02
    t0 = 0.001
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    Ri = R1*R2/(R1+R2)+R3
    tau = L/Ri
    t = solution.t
    V = input['Vs'](t)
    iL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*(1-np.exp(-(t-t0)/tau))
    uL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*np.exp(-(t-t0)/tau)*L/tau
    phi3_ref = uL_ref
    phi2_ref = R3*iL_ref+phi3_ref
    phi1_ref = V
    uR1_ref = phi1_ref-phi2_ref
    uR2_ref = phi2_ref
    uR3_ref = phi2_ref-phi3_ref
    iS_ref = (phi2_ref-phi1_ref)/R1
    iR1_ref = -iS_ref
    iR2_ref = iR1_ref - iL_ref
    iR3_ref = iL_ref
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('L')[1], uL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R3')[1], iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('L')[1], iL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R3')[1], uR3_ref*iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('L')[1], uL_ref*iL_ref, atol=1e-3)

def test_transient_analysis_of_example_network_6() -> None:
    Vs = 5
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
        cmp.inductance(id='L', L=L, nodes=('2', '3')),
        cmp.resistor(id='R3', R=R3, nodes=('3', '0')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.000001
    t_max = 0.02
    t0 = 0.001
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    Ri = R1*R2/(R1+R2)+R3
    tau = L/Ri
    t = solution.t
    V = input['Vs'](t)
    iL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*(1-np.exp(-(t-t0)/tau))
    uL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*L/tau*np.exp(-(t-t0)/tau)
    phi3_ref = R3*iL_ref
    phi2_ref = phi3_ref + uL_ref
    phi1_ref = V
    uR1_ref = phi1_ref - phi2_ref
    uR2_ref = phi2_ref
    uR3_ref = phi3_ref
    iS_ref = (phi2_ref-phi1_ref)/R1
    iR1_ref = -iS_ref
    iR2_ref = uR2_ref/R2
    iR3_ref = iL_ref
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('L')[1], uL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R3')[1], iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('L')[1], iL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R3')[1], uR3_ref*iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('L')[1], uL_ref*iL_ref, atol=1e-3)

def test_transient_analysis_of_example_network_7() -> None:
    Vs = 5
    Is = 1
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
        cmp.inductance(id='L', L=L, nodes=('2', '3')),
        cmp.resistor(id='R3', R=R3, nodes=('3', '0')),
        cmp.dc_current_source(id='Is', I=Is, nodes=('0', '3')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.0000001
    t_max = 0.02
    t0 = 0.001
    t1 = 0.01
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0), 'Is': lambda t: Is*step(t, t0=t1)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    Ri = R1*R2/(R1+R2)+R3
    tau = L/Ri
    t = solution.t
    V = input['Vs'](t)
    I = input['Is'](t)
    iL_ref = np.zeros(t.size)
    iL_ref[t>t0] = Vs*R2/(R1*R2+R1*R3+R2*R3)*(1-np.exp(-(t[t>t0]-t0)/tau))
    iL_ref[t>t1] = iL_ref[t>t1] - Is*R3/(R1*R2/(R1+R2)+R3)*(1-np.exp(-(t[t>t1]-t1)/tau))
    uL_ref = np.zeros(t.size)
    uL_ref[t>t0] = Vs*R2/(R1*R2+R1*R3+R2*R3)*np.exp(-(t[t>t0]-t0)/tau)*L/tau
    uL_ref[t>t1] = uL_ref[t>t1] - Is*R3/(R1*R2/(R1+R2)+R3)*np.exp(-(t[t>t1]-t1)/tau)*L/tau
    phi3_ref = R3*(iL_ref+I)
    phi2_ref = phi3_ref + uL_ref
    phi1_ref = V
    uR1_ref = phi1_ref-phi2_ref
    uR2_ref = phi2_ref
    uR3_ref = phi3_ref
    uIs_ref = -phi3_ref
    iS_ref = (phi2_ref-phi1_ref)/R1
    iR1_ref = -iS_ref
    iR2_ref = iR1_ref - iL_ref
    iR3_ref = iL_ref + I
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R3')[1], uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('L')[1], uL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Is')[1], -uR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R3')[1], iR3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('L')[1], iL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Is')[1], I, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('L')[1], uL_ref*iL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Is')[1], (-uR3_ref)*I, atol=1e-3)

def test_transient_analysis_of_example_network_8() -> None:
    Vs = 5
    R1, R2 = 10, 20
    L1, L2 = 0.1, 0.2
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
        cmp.inductance(id='L1', L=L1, nodes=('2', '3')),
        cmp.resistor(id='R2', R=R2, nodes=('3', '0')),
        cmp.inductance(id='L2', L=L2, nodes=('3', '0')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.000001
    t_max = 0.02
    t0 = 0.001
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    x1, x2 = quad_equation(1, R2/L1+R1/L1+R2/L2, R1*R2/L1/L2)
    t = solution.t
    V = input['Vs'](t)
    t_ref = t[t>t0]-t0
    phi3_ref = np.zeros(t.size)
    phi3_ref[t>t0] = Vs*R2/L1 * (np.exp(x1*t_ref)-np.exp(x2*t_ref))/(x1-x2)
    iL1_ref = np.zeros(t.size)
    iL1_ref[t>t0] = Vs*R2/L1/L2*(x2*np.exp(x1*t_ref)-x1*np.exp(x2*t_ref)-x2+x1)/(x1*x2*(x1-x2)) + Vs/L1*(np.exp(x2*t_ref)-np.exp(x1*t_ref))/(x2-x1)
    iL2_ref = iL1_ref - phi3_ref/R2
    iR1_ref = iL1_ref
    iR2_ref = iL1_ref - iL2_ref
    phi2_ref = V-iL1_ref*R1
    phi1_ref = V
    uR1_ref = phi1_ref - phi2_ref
    uR2_ref = phi3_ref
    uL1_ref = phi2_ref - phi3_ref
    uL2_ref = phi3_ref
    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], phi2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], uL2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R1')[1], uR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R2')[1], uR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('L1')[1], uL1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('L2')[1], uL2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R1')[1], iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R2')[1], iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('L1')[1], iL1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('L2')[1], iL2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-iR1_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R1')[1], uR1_ref*iR1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R2')[1], uR2_ref*iR2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('L1')[1], uL1_ref*iL1_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('L2')[1], uL2_ref*iL2_ref, atol=1e-3)

def test_transient_analysis_of_example_network_9() -> None:
    Vs = 5
    R = 2
    L = 2e-3
    C = 0.5e-3
    circuit = Circuit([
        cmp.dc_voltage_source(id='Vs', V=Vs, nodes=('1', '0')),
        cmp.resistor(id='R', R=R, nodes=('1', '2')),
        cmp.inductance(id='L', L=L, nodes=('2', '3')),
        cmp.capacitor(id='C', C=C, nodes=('3', '0')),
        cmp.ground(nodes=('0',))
    ])
    Ts = 0.0000001
    t_max = 0.02
    t0 = 0.001
    t_vec = np.arange(0, t_max, Ts)
    input = {'Vs': lambda t: Vs*step(t, t0=t0)}
    solution = TransientSolution(circuit, input=input, tin=t_vec)

    w0 = 1/np.sqrt(L*C)
    d = R/2/L
    we = np.sqrt(w0**2-d**2)
    t = solution.t
    V = input['Vs'](t)
    tref = t-t0
    i_ref = V/we/L*np.exp(-d*tref)*np.sin(we*tref)
    uR_ref = i_ref*R
    uL_ref = V/we*(-d*np.exp(-d*tref)*np.sin(we*tref)+np.exp(-d*tref)*np.cos(we*tref)*we)
    phi1_ref = V
    phi2_ref = V-i_ref*R
    phi3_ref = phi2_ref-uL_ref
    uC_ref = phi3_ref

    np.testing.assert_allclose(solution.get_potential('0')[1], np.zeros(solution.t.size), atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('1')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('2')[1], phi2_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_potential('3')[1], phi3_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('Vs')[1], V, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('R')[1], uR_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('L')[1], uL_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_voltage('C')[1], uC_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('Vs')[1], -i_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('R')[1], i_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('L')[1], i_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_current('C')[1], i_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('Vs')[1], V*(-i_ref), atol=1e-3)
    np.testing.assert_allclose(solution.get_power('R')[1], uR_ref*i_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('L')[1], uL_ref*i_ref, atol=1e-3)
    np.testing.assert_allclose(solution.get_power('C')[1], uC_ref*i_ref, atol=1e-3)