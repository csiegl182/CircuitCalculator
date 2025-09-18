from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.Components.components as cmp
from CircuitCalculator.Circuit.state_space_model import numeric_state_space_model
import numpy as np
from scipy import signal

def test_example_circuit_1() -> None:
    R1, R2, R3 = 10, 20, 30
    C = 1e-3
    V0 = 5
    t_max = 0.3
    t0 = 0.1
    Ts = 0.0003
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vs', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
            cmp.resistor(id='R3', R=R3, nodes=('2', '3')),
            cmp.capacitor(id='C', C=C, nodes=('3', '0'))
        ],
        ground_node='0')
    ss = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vs', 'R1', 'R2', 'R3', 'C'], current_ids=['Vs', 'R1', 'R2', 'R3', 'C'])
    sys = signal.StateSpace(ss.A, ss.B, ss.C, ss.D)

    tout, yout, _ = signal.lsim(sys, V, t)

    Ri = R1*R2/(R1+R2)+R3
    tau = Ri*C

    u2_ref = V*R2/(R1+R2)*(1+(R3*C/tau-1)*(np.exp(-(tout-t0)/tau)))
    uc_ref = V*R2/(R1+R2)*(1-np.exp(-(tout-t0)/tau))

    phi1_ref = V
    phi2_ref = u2_ref
    phi3_ref = uc_ref

    u1_ref = V - u2_ref
    u3_ref = u2_ref - uc_ref

    i1_ref = u1_ref/R1
    i2_ref = u2_ref/R2
    i3_ref = u3_ref/R3
    ic_ref = C*V*R2/(R1+R2)/tau*np.exp(-(tout-t0)/tau)

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], u1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], u2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], u3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], uc_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], -i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], i2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], i3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], ic_ref, atol=1e-2)

def test_example_circuit_2() -> None:
    R1, R2, R3 = 10, 20, 30
    C = 1e-3
    V0 = 5
    t_max = 0.3
    t0 = 0.1
    Ts = 0.0003
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vs', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
            cmp.capacitor(id='C', C=C, nodes=('2', '3')),
            cmp.resistor(id='R3', R=R3, nodes=('3', '0'))
        ],
        ground_node='0')

    ss = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vs', 'R1', 'R2', 'R3', 'C'], current_ids=['Vs', 'R1', 'R2', 'R3', 'C'])
    sys = signal.StateSpace(ss.A, ss.B, ss.C, ss.D)
    tout, yout, _ = signal.lsim(sys, V, t)

    tau = C*(R1*R2+R1*R3+R2*R3)/(R1+R2)

    uc_ref = V*R2/(R1+R2)*(1-np.exp(-(tout-t0)/tau))
    ic_ref = C*V*R2/(R1+R2)/tau*np.exp(-(tout-t0)/tau)

    u3_ref = ic_ref*R3
    u2_ref = uc_ref + u3_ref
    u1_ref = V - u2_ref

    phi1_ref = V
    phi2_ref = u2_ref
    phi3_ref = u3_ref

    i1_ref = u1_ref/R1
    i2_ref = u2_ref/R2
    i3_ref = u3_ref/R3

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], u1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], u2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], u3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], uc_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], -i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], i2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], i3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], ic_ref, atol=1e-2)

def test_example_circuit_3() -> None:
    R1, R2 = 10, 20
    C = 1e-3
    V0 = 5
    I0 = -0.1
    t_max = 0.3
    t0 = 0.1
    t1 = 0.2
    Ts = 0.0003
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    I = I0*np.heaviside(t-t1, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vs', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.capacitor(id='C', C=C, nodes=('2', '3')),
            cmp.resistor(id='R2', R=R2, nodes=('3', '0')),
            cmp.dc_current_source(id='Is', I=I0, nodes=('0', '3'))
        ],
        ground_node='0'
    )

    ss = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vs', 'R1', 'R2', 'C', 'Is'], current_ids=['Vs', 'R1', 'R2', 'C', 'Is'])
    sys = signal.StateSpace(ss.A, ss.B, ss.C, ss.D)
    tout, yout, _ = signal.lsim(sys, np.column_stack([I, V]), t)

    Ri = R1+R2
    tau = Ri*C

    uc_ref = np.zeros(t.size)
    uc_ref[t>t0] = V0*(1-np.exp(-(tout[t>t0]-t0)/tau))
    uc_ref[t>t1] = uc_ref[t>t1] - I0*R2*(1-np.exp(-(tout[t>t1]-t1)/tau))

    ic_ref = np.zeros(t.size)
    ic_ref[t>t0] = C*V0*(-np.exp(-(tout[t>0.1]-0.1)/tau))*(-1/tau)
    ic_ref[t>t1] = ic_ref[t>t1] - C*I0*R2*(-np.exp(-(tout[t>t1]-t1)/tau))*(-1/tau)

    phi1_ref = V
    phi2_ref = -ic_ref*R1 + V
    phi3_ref = (ic_ref + I)*R2

    u1_ref = V - phi2_ref
    u2_ref = phi3_ref

    i1_ref = u1_ref/R1
    i2_ref = u2_ref/R2

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], u1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], u2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], uc_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], -u2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], -i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], i2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], ic_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], I, atol=1e-2)

def test_example_circuit_4() -> None:
    V0 = 1
    R1, R2 = 10, 20
    C1 = 5e-3
    C2 = 1e-3
    t_max = 0.5
    t0 = 0.1
    Ts = 0.0003
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vs', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.capacitor(id='C1', C=C1, nodes=('2', '3')),
            cmp.resistor(id='R2', R=R2, nodes=('3', '0')),
            cmp.capacitor(id='C2', C=C2, nodes=('3', '0'))
        ],
        ground_node='0'
    )

    ss = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vs', 'R1', 'R2', 'C1', 'C2'], current_ids=['Vs', 'R1', 'R2', 'C1', 'C2'])
    sys = signal.StateSpace(ss.A, ss.B, ss.C, ss.D)
    tout, yout, _ = signal.lsim(sys, V, t)

    def quad_equation(a, b, c):
        D = np.sqrt(b**2-4*a*c)
        return ((-b+D)/2/a, (-b-D)/2/a)

    a = C2*R2
    b = C1*R1
    c = C1*R2
    s1, s2 = quad_equation(1, (a+b+c)/a/b, 1/a/b)
    s3, s4 = quad_equation(1, (a+b+c)/a/b, 1/a/b)

    t_ref = tout[t>t0]-t0

    uc1_ref = np.zeros(t.size)
    uc1_ref[t>t0] = V0/a/b * (1/s1/s2 + 1/(s2-s1)*(-1/s1*np.exp(s1*t_ref)+1/s2*np.exp(s2*t_ref))) + V0/b * 1/(s1-s2) * (np.exp(s1*t_ref)-np.exp(s2*t_ref))

    uc2_ref = np.zeros(t.size)
    uc2_ref[t>t0] = V0*c/a/b * (np.exp(s3*t_ref)-np.exp(s4*t_ref))/(s3-s4)

    phi1_ref = V
    phi2_ref = uc1_ref + uc2_ref
    phi3_ref = uc2_ref

    u1_ref = V - phi2_ref
    u2_ref = uc2_ref

    i1_ref = u1_ref/R1
    i2_ref = u2_ref/R2

    ic1_ref = np.zeros(t.size)
    ic1_ref[t>t0] = C1*V0/a/b * (1/(s2-s1)*(-np.exp(s1*t_ref)+np.exp(s2*t_ref))) + C1*V0/b * 1/(s1-s2) * (np.exp(s1*t_ref)*s1-np.exp(s2*t_ref)*s2)

    ic2_ref = np.zeros(t.size)
    ic2_ref[t>t0] = C2*V0*c/a/b * (np.exp(s3*t_ref)*s3-np.exp(s4*t_ref)*s4)/(s3-s4)

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], u1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], u2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], uc1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], uc2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], -i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], i1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], i2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], ic1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], ic2_ref, atol=1e-2)

def test_example_circuit_5() -> None:
    V0 = 5
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    t_max = 0.02
    t0 = 0.001
    Ts = t_max/5000
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vq', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
            cmp.resistor(id='R3', R=R3, nodes=('2', '3')),
            cmp.inductor(id='L', L=L, nodes=('3', '0'))
        ],
        ground_node='0'
    )

    ssm = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vq', 'R1', 'R2', 'R3', 'L'], current_ids=['R1', 'R2', 'R3', 'L', 'Vq'])
    sys = signal.StateSpace(ssm.A, ssm.B, ssm.C, ssm.D)
    tout, yout, _ = signal.lsim(sys, V, t)

    def pll(R1, R2):
        return R1*R2/(R1+R2)

    Ri = pll(R1, R2)+R3
    tau = L/Ri

    iL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*(1-np.exp(-(tout-t0)/tau))
    uL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*np.exp(-(tout-t0)/tau)*L/tau

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

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], uR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], uR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], uR3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], uL_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], iR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], iR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], iR3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], iL_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], iS_ref, atol=1e-2)

def test_example_circuit_6() -> None:
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    V0 = 5
    t_max = 0.02
    t0 = 0.001
    Ts = t_max/5000
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vq', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
            cmp.inductor(id='L', L=L, nodes=('2', '3')),
            cmp.resistor(id='R3', R=R3, nodes=('3', '0'))
        ],
        ground_node='0'
    )

    ssm = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vq', 'R1', 'R2', 'R3', 'L'], current_ids=['R1', 'R2', 'R3', 'L', 'Vq'])
    sys = signal.StateSpace(ssm.A, ssm.B, ssm.C, ssm.D)
    tout, yout, _ = signal.lsim(sys, V, t)

    def pll(R1, R2):
        return R1*R2/(R1+R2)

    Ri = pll(R1, R2)+R3
    tau = L/Ri

    iL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*(1-np.exp(-(tout-t0)/tau))
    uL_ref = V*R2/(R1*R2+R1*R3+R2*R3)*L/tau*np.exp(-(tout-t0)/tau)

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

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], uR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], uR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], uR3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], uL_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], iR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], iR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], iR3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], iL_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], iS_ref, atol=1e-2)

def test_example_circuit_7() -> None:
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    V0 = 5
    I0 = 1
    t_max = 0.02
    t0 = 0.001
    t1 = 0.01
    Ts = t_max/50000
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    I = I0*np.heaviside(t-t1, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vq', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.resistor(id='R2', R=R2, nodes=('2', '0')),
            cmp.inductor(id='L', L=L, nodes=('2', '3')),
            cmp.resistor(id='R3', R=R3, nodes=('3', '0')),
            cmp.dc_current_source(id='Iq', I=I0, nodes=('0', '3'))
        ],
        ground_node='0'
    )
    
    ssm = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vq', 'R1', 'R2', 'R3', 'L', 'Iq'], current_ids=['R1', 'R2', 'R3', 'L', 'Vq', 'Iq'])
    sys = signal.StateSpace(ssm.A, ssm.B, ssm.C, ssm.D)
    tout, yout, _ = signal.lsim(sys, np.column_stack((I,V)), t)

    def pll(R1, R2):
        return R1*R2/(R1+R2)

    Ri = pll(R1, R2)+R3
    tau = L/Ri

    iL_ref = np.zeros(tout.size)
    iL_ref[tout>t0] = V0*R2/(R1*R2+R1*R3+R2*R3)*(1-np.exp(-(tout[tout>t0]-t0)/tau))
    iL_ref[tout>t1] = iL_ref[tout>t1] - I0*R3/(pll(R1, R2)+R3)*(1-np.exp(-(tout[tout>t1]-t1)/tau))

    uL_ref = np.zeros(tout.size)
    uL_ref[tout>=t0] = V0*R2/(R1*R2+R1*R3+R2*R3)*np.exp(-(tout[tout>=t0]-t0)/tau)*L/tau
    uL_ref[tout>=t1] = uL_ref[tout>=t1] - I0*R3/(pll(R1, R2)+R3)*np.exp(-(tout[tout>=t1]-t1)/tau)*L/tau

    phi3_ref = R3*(iL_ref+I)
    phi2_ref = phi3_ref + uL_ref
    phi1_ref = V

    uR1_ref = phi1_ref-phi2_ref
    uR2_ref = phi2_ref
    uR3_ref = phi3_ref
    uIq_ref = -phi3_ref

    iS_ref = (phi2_ref-phi1_ref)/R1
    iR1_ref = -iS_ref
    iR2_ref = iR1_ref - iL_ref
    iR3_ref = iL_ref + I

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], uR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], uR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], uR3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], uL_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], uIq_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], iR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], iR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], iR3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], iL_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,13], iS_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,14], I, atol=1e-2)

def test_example_circuit_8() -> None:
    R1, R2 = 10, 20
    L1, L2 = 0.1, 0.2
    V0 = 5
    t_max = 0.02
    t0 = 0.001
    Ts = t_max/5000
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vq', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R1', R=R1, nodes=('1', '2')),
            cmp.inductor(id='L1', L=L1, nodes=('2', '3')),
            cmp.resistor(id='R2', R=R2, nodes=('3', '0')),
            cmp.inductor(id='L2', L=L2, nodes=('3', '0'))
        ],
        ground_node='0'
    )

    ssm = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vq', 'R1', 'R2', 'L1', 'L2'], current_ids=['R1', 'R2', 'L1', 'L2', 'Vq'])
    sys = signal.StateSpace(ssm.A, ssm.B, ssm.C, ssm.D)
    tout, yout, _ = signal.lsim(sys, V, t)

    def quad_equation(b, c):
        return (-b+np.sqrt(b**2-4*c))/2, (-b-np.sqrt(b**2-4*c))/2

    x1, x2 = quad_equation(R2/L1+R1/L1+R2/L2, R1*R2/L1/L2)

    t_ref = tout[tout>t0]-t0

    phi3_ref = np.zeros(tout.size)
    phi3_ref[tout>t0] = V0*R2/L1 * (np.exp(x1*t_ref)-np.exp(x2*t_ref))/(x1-x2)

    iL1_ref = np.zeros(tout.size)
    iL1_ref[tout>t0] = V0*R2/L1/L2*(x2*np.exp(x1*t_ref)-x1*np.exp(x2*t_ref)-x2+x1)/(x1*x2*(x1-x2)) + V0/L1*(np.exp(x2*t_ref)-np.exp(x1*t_ref))/(x2-x1)

    iL2_ref = iL1_ref - phi3_ref/R2

    iR1_ref = iL1_ref
    iR2_ref = iL1_ref - iL2_ref

    phi2_ref = V-iL1_ref*R1
    phi1_ref = V

    uR1_ref = phi1_ref - phi2_ref
    uR2_ref = phi3_ref

    uL1_ref = phi2_ref - phi3_ref
    uL2_ref = phi3_ref

    iS_ref = -iL1_ref

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], uR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], uR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], uL1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], uL2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], iR1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], iR2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], iL1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,11], iL2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,12], iS_ref, atol=1e-2)

def test_example_circuit_9() -> None:
    R = 2
    L = 2e-3
    C = 0.5e-3
    t_max = 0.02
    V0 = 5
    t0 = 0.001
    Ts = t_max/5000
    t = np.arange(0, t_max, Ts)
    V = V0*np.heaviside(t-t0, 1)
    circuit = Circuit(
        components=[
            cmp.dc_voltage_source(id='Vq', V=V0, nodes=('1', '0')),
            cmp.resistor(id='R', R=R, nodes=('1', '2')),
            cmp.inductor(id='L', L=L, nodes=('2', '3')),
            cmp.capacitor(id='C', C=C, nodes=('3', '0'))
        ],
        ground_node='0'
    )

    ssm = numeric_state_space_model(circuit=circuit, potential_nodes=['1', '2', '3'], voltage_ids=['Vq', 'R', 'L', 'C'], current_ids=['R', 'L', 'C', 'Vq'])
    sys = signal.StateSpace(ssm.A, ssm.B, ssm.C, ssm.D)
    tout, yout, xout = signal.lsim(sys, V, t)

    w0 = 1/np.sqrt(L*C)
    d = R/2/L
    we = np.sqrt(w0**2-d**2)

    tref = tout-t0

    i_ref = V/we/L*np.exp(-d*tref)*np.sin(we*tref)

    uR_ref = i_ref*R
    uL_ref = V/we*(-d*np.exp(-d*tref)*np.sin(we*tref)+np.exp(-d*tref)*np.cos(we*tref)*we)

    phi1_ref = V
    phi2_ref = V-i_ref*R
    phi3_ref = phi2_ref-uL_ref

    uC_ref = phi3_ref

    np.testing.assert_allclose(yout[:,0], phi1_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,1], phi2_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,2], phi3_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,3], V, atol=1e-2)
    np.testing.assert_allclose(yout[:,4], uR_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,5], uL_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,6], uC_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,7], i_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,8], i_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,9], i_ref, atol=1e-2)
    np.testing.assert_allclose(yout[:,10], -i_ref, atol=1e-2)