import CircuitCalculator.Circuit.Components.components as ccp
import CircuitCalculator.Circuit.transformers as transform
import numpy as np

def test_resistor_transformer() -> None:
    nodes = ('0', '1')
    id = 'R'
    R = 100
    res = ccp.resistor(nodes=nodes, id=id, R=R)
    transformed_resistor = transform.resistor(res)
    assert (transformed_resistor.node1, transformed_resistor.node2) == nodes
    assert transformed_resistor.id == id
    assert transformed_resistor.element.Z == R 

def test_voltage_source_transformer_transforms_dc_voltage_source() -> None:
    nodes = ('0', '1')
    id = 'U'
    V = 100
    voltage_source = ccp.dc_voltage_source(nodes=nodes, id=id, V=V)
    transformed_voltage_source = transform.dc_voltage_source(voltage_source)
    assert (transformed_voltage_source.node1, transformed_voltage_source.node2) == nodes
    assert transformed_voltage_source.id == id
    np.testing.assert_almost_equal(transformed_voltage_source.element.V, V)

def test_voltage_source_transformer_transforms_voltage_source_at_its_frequency() -> None:
    nodes = ('0', '1')
    id = 'U'
    V = 100
    w = 100
    voltage_source = ccp.ac_voltage_source(nodes=nodes, id=id, V=V, w=w)
    transformed_voltage_source = transform.ac_voltage_source(voltage_source, w=w)
    assert (transformed_voltage_source.node1, transformed_voltage_source.node2) == nodes
    assert transformed_voltage_source.id == id
    np.testing.assert_almost_equal(transformed_voltage_source.element.V, V)

def test_voltage_source_transformer_transforms_voltage_source_at_another_frequency() -> None:
    nodes = ('0', '1')
    id = 'U'
    V = 100
    w = 100
    voltage_source = ccp.ac_voltage_source(nodes=nodes, id=id, V=V, w=w)
    transformed_voltage_source = transform.ac_voltage_source(voltage_source, w=200)
    assert (transformed_voltage_source.node1, transformed_voltage_source.node2) == nodes
    assert transformed_voltage_source.id == id
    np.testing.assert_almost_equal(transformed_voltage_source.element.V, 0)

def test_current_source_transformer_transforms_dc_current_source() -> None:
    nodes = ('0', '1')
    id = 'I'
    I = 1
    current_source = ccp.dc_current_source(nodes=nodes, id=id, I=I)
    transformed_current_source = transform.dc_current_source(current_source)
    assert (transformed_current_source.node1, transformed_current_source.node2) == nodes
    assert transformed_current_source.id == id
    np.testing.assert_almost_equal(transformed_current_source.element.I, I)

def test_current_source_transformer_transforms_current_source_at_its_frequency() -> None:
    nodes = ('0', '1')
    id = 'I'
    I = 100
    w = 100
    current_source = ccp.ac_current_source(nodes=nodes, id=id, I=I, w=w)
    transformed_current_source = transform.ac_current_source(current_source, w=w)
    assert (transformed_current_source.node1, transformed_current_source.node2) == nodes
    assert transformed_current_source.id == id
    np.testing.assert_almost_equal(transformed_current_source.element.I, I)

def test_current_source_transformer_transforms_current_source_at_another_frequency() -> None:
    nodes = ('0', '1')
    id = 'I'
    I = 100
    w = 100
    current_source = ccp.ac_current_source(nodes=nodes, id=id, I=I, w=w)
    transformed_current_source = transform.ac_current_source(current_source, w=200)
    assert (transformed_current_source.node1, transformed_current_source.node2) == nodes
    assert transformed_current_source.id == id
    np.testing.assert_almost_equal(transformed_current_source.element.I, 0)

def test_capacitor_is_transformed_to_impedance() -> None:
    nodes = ('0', '1')
    id = 'C'
    C = 1e-3
    w = 100
    capacitor = ccp.capacitor(nodes=nodes, id=id, C=C)
    transformed_capacitor = transform.capacitor(capacitor, w=w)
    assert (transformed_capacitor.node1, transformed_capacitor.node2) == nodes
    assert transformed_capacitor.id == id
    np.testing.assert_almost_equal(transformed_capacitor.element.Z, 1/(1j*w*C))

def test_capacitor_is_transformed_to_open_circuit_at_zero_frequency() -> None:
    nodes = ('0', '1')
    id = 'C'
    C = 1e-3
    w = 0
    capacitor = ccp.capacitor(nodes=nodes, id=id, C=C)
    transformed_capacitor = transform.capacitor(capacitor, w=w)
    assert (transformed_capacitor.node1, transformed_capacitor.node2) == nodes
    assert transformed_capacitor.id == id
    np.testing.assert_almost_equal(transformed_capacitor.element.Y, 0)

def test_capacitor_is_transformed_to_short_circuit_at_infinite_frequency() -> None:
    nodes = ('0', '1')
    id = 'C'
    C = 1e-3
    w = np.inf
    capacitor = ccp.capacitor(nodes=nodes, id=id, C=C)
    transformed_capacitor = transform.capacitor(capacitor, w=w)
    assert (transformed_capacitor.node1, transformed_capacitor.node2) == nodes
    assert transformed_capacitor.id == id
    np.testing.assert_almost_equal(transformed_capacitor.element.Z, 0)

def test_inductance_is_transformed_to_impedance() -> None:
    nodes = ('0', '1')
    id = 'L'
    L = 1e-3
    w = 100
    inductance = ccp.inductance(nodes=nodes, id=id, L=L)
    transformed_inductance = transform.inductance(inductance, w=w)
    assert (transformed_inductance.node1, transformed_inductance.node2) == nodes
    assert transformed_inductance.id == id
    np.testing.assert_almost_equal(transformed_inductance.element.Z, 1j*w*L)

def test_inductance_is_transformed_to_short_circuit_at_zero_frequency() -> None:
    nodes = ('0', '1')
    id = 'L'
    L = 1e-3
    w = 0
    inductance = ccp.inductance(nodes=nodes, id=id, L=L)
    transformed_inductance = transform.inductance(inductance, w=w)
    assert (transformed_inductance.node1, transformed_inductance.node2) == nodes
    assert transformed_inductance.id == id
    np.testing.assert_almost_equal(transformed_inductance.element.Z, 0)

def test_inductance_is_transformed_to_open_circuit_at_infinite_frequency() -> None:
    nodes = ('0', '1')
    id = 'L'
    L = 1e-3
    w = np.inf
    inductance = ccp.inductance(nodes=nodes, id=id, L=L)
    transformed_inductance = transform.inductance(inductance, w=w)
    assert (transformed_inductance.node1, transformed_inductance.node2) == nodes
    assert transformed_inductance.id == id
    np.testing.assert_almost_equal(transformed_inductance.element.Y, 0)
