from CircuitCalculator.Circuit.dump_load import generate_component

def test_resistor_translator() -> None:
    resistor_dict = {
        'type': 'resistor',
        'id': 'R',
        'nodes': ('0', '1'),
        'value': {'R': 100}
    }
    resistor = generate_component(resistor_dict)
    assert resistor.type == resistor_dict['type']
    assert resistor.id == resistor_dict['id']
    assert resistor.nodes == resistor_dict['nodes']
    assert resistor.value['R'] == resistor_dict['value']['R']

def test_conductance_translator() -> None:
    conductance_dict = {
        'type': 'conductance',
        'id': 'G',
        'nodes': ('0', '1'),
        'value': {'G': 100}
    }
    conductance = generate_component(conductance_dict)
    assert conductance.type == conductance_dict['type']
    assert conductance.id == conductance_dict['id']
    assert conductance.nodes == conductance_dict['nodes']
    assert conductance.value['G'] == conductance_dict['value']['G']

def test_voltage_source_translator() -> None:
    voltage_source_dict = {
        'type': 'dc_voltage_source',
        'id': 'voltage_source',
        'nodes': ('0', '1'),
        'value': {'V': 100}
    }
    voltage_source = generate_component(voltage_source_dict)
    assert voltage_source.type == voltage_source_dict['type']
    assert voltage_source.id == voltage_source_dict['id']
    assert voltage_source.nodes == voltage_source_dict['nodes']
    assert voltage_source.value['V'] == voltage_source_dict['value']['V']

def test_current_source_translator() -> None:
    current_source_dict = {
        'type': 'dc_current_source',
        'id': 'current_source',
        'nodes': ('0', '1'),
        'value': {'I': 100}
    }
    current_source = generate_component(current_source_dict)
    assert current_source.type == current_source_dict['type']
    assert current_source.id == current_source_dict['id']
    assert current_source.nodes == current_source_dict['nodes']
    assert current_source.value['I'] == current_source_dict['value']['I']

def test_complex_voltage_source_translator() -> None:
    voltage_source_dict = {
        'type': 'complex_voltage_source',
        'id': 'voltage_source',
        'nodes': ('0', '1'),
        'value': {'V': '100 + 50j'}
    }
    voltage_source = generate_component(voltage_source_dict)
    assert voltage_source.id == voltage_source_dict['id']
    assert voltage_source.nodes == voltage_source_dict['nodes']
    assert voltage_source.value['V_real'] == complex(voltage_source_dict['value']['V'].replace(' ', '')).real
    assert voltage_source.value['V_imag'] == complex(voltage_source_dict['value']['V'].replace(' ', '')).imag

def test_complex_current_source_translator() -> None:
    current_source_dict = {
        'type': 'complex_current_source',
        'id': 'current_source',
        'nodes': ('0', '1'),
        'value': {'I': "100 + 50j"}
    }
    current_source = generate_component(current_source_dict)
    assert current_source.id == current_source_dict['id']
    assert current_source.nodes == current_source_dict['nodes']
    assert current_source.value['I_real'] == complex(current_source_dict['value']['I'].replace(' ', '')).real
    assert current_source.value['I_imag'] == complex(current_source_dict['value']['I'].replace(' ', '')).imag

def test_ground() -> None:
    ground_dict = {
        'type': 'ground',
        'id': 'gnd',
        'nodes': ('0', ),
        'value': {}
    }
    ground = generate_component(ground_dict)
    assert ground.type == ground_dict['type']
    assert ground.id == ground_dict['id']
    assert ground.nodes == ground_dict['nodes']
    assert ground.value == {}