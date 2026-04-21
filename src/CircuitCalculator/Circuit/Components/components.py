from dataclasses import dataclass, field

@dataclass(frozen=True)
class Component:
    type : str
    id : str = field(default='0')
    nodes : tuple[str, ...] = field(default=('0',))
    value: dict[str, float | str | tuple[str, str]] = field(default_factory=dict)

def resistor(id: str, nodes: tuple[str, str], R: float, **_) -> Component:
    if R < 0:
        raise ValueError('R must be greater than zero.')
    return Component(
        type='resistor',
        id=id,
        value={'R': R},
        nodes=nodes
        )

def conductance(id: str, nodes: tuple[str, str], G: float, **_) -> Component:
    if G < 0:
        raise ValueError('G must be greater than zero.')
    return Component(
        type='conductance',
        id=id,
        value={'G': G},
        nodes=nodes
        )

def capacitor(id: str, nodes: tuple[str, str], C: float, **_) -> Component:
    if C < 0:
        raise ValueError('C must be greater than zero.')
    return Component(
        type='capacitor',
        id=id,
        value={'C': C},
        nodes=nodes
    )

def inductor(id: str, nodes: tuple[str, str], L: float, **_) -> Component:
    if L < 0:
        raise ValueError('L must be greater than zero.')
    return Component(
        type='inductance',
        id=id,
        value={'L': L},
        nodes=nodes
    )

def impedance(id: str, nodes: tuple[str, str], Z: complex, **_) -> Component:
    return Component(
        type='impedance',
        id=id,
        value={'R': Z.real, 'X': Z.imag},
        nodes=nodes
        )

def admittance(id: str, nodes: tuple[str, str], Y: complex, **_) -> Component:
    return Component(
        type='admittance',
        id=id,
        value={'G': Y.real, 'B': Y.imag},
        nodes=nodes
        )

def dc_voltage_source(id: str, nodes: tuple[str, str], V: float, R: float = 0, **_) -> Component:
    if R < 0:
        raise ValueError('R must be greater than zero.')
    return Component(
        type='dc_voltage_source',
        id=id,
        value={'V': V, 'R': R, 'w': 0, 'phi': 0},
        nodes=nodes
        )

def ac_voltage_source(id: str, nodes: tuple[str, str], V: float, R: float = 0, w: float = 0, phi: float = 0, **_) -> Component:
    if R < 0:
        raise ValueError('R must be greater than zero.')
    if w < 0:
        raise ValueError('w must be greater than zero.')
    return Component(
        type='ac_voltage_source',
        id=id,
        value={'V': V, 'R': R, 'w': w, 'phi': phi},
        nodes=nodes
        )

def complex_voltage_source(id: str, nodes: tuple[str, str], V: complex, Z: complex = 0, **_) -> Component:
    return Component(
        type='complex_voltage_source',
        id=id,
        value={'V_real': V.real, 'V_imag': V.imag, 'R': Z.real, 'X': Z.imag},
        nodes=nodes
        )

def periodic_voltage_source(id: str, nodes: tuple[str, str], wavetype: str, V: float, w: float, phi: float = 0, R: float = 0, **_) ->Component:
    if R < 0:
        raise ValueError('R must be greater than zero.')
    if w < 0:
        raise ValueError('w must be greater than zero.')
    return Component(
        type='periodic_voltage_source',
        id=id,
        value={'wavetype': wavetype,
               'V': V,
               'w': w,
               'phi': phi,
               'R': R},
        nodes=nodes
        )

def dc_current_source(id: str, nodes: tuple[str, str], I: float, G: float = 0, **_) -> Component:
    if G < 0:
        raise ValueError('G must be greater than zero.')
    return Component(
        type='dc_current_source',
        id=id,
        value={'I': I, 'G': G, 'w': 0, 'phi': 0},
        nodes=nodes
        )

def ac_current_source(id: str, nodes: tuple[str, str], I: float, G: float = 0, w: float = 0, phi: float = 0, **_) -> Component:
    if G < 0:
        raise ValueError('G must be greater than zero.')
    if w < 0:
        raise ValueError('w must be greater than zero.')
    return Component(
        type='ac_current_source',
        id=id,
        value={'I': I, 'G': G, 'w': w, 'phi': phi},
        nodes=nodes
        )

def complex_current_source(id: str, nodes: tuple[str, str], I: complex, Y: complex = 0, **_) -> Component:
    return Component(
        type='complex_current_source',
        id=id,
        value={'I_real': I.real, 'I_imag': I.imag, 'G': Y.real, 'B': Y.imag},
        nodes=nodes
        )

def voltage_controlled_current_source(id: str, nodes: tuple[str, str], G: float, *, control_nodes: tuple[str, str], **_) -> Component:
    if len(nodes) != 2:
        raise ValueError('Voltage controlled current source output nodes must contain two nodes.')
    if len(control_nodes) != 2:
        raise ValueError('Voltage controlled current source control nodes must contain two nodes.')
    control_nodes = tuple(control_nodes)
    return Component(
        type='voltage_controlled_current_source',
        id=id,
        value={'G': G, 'control_nodes': control_nodes},
        nodes=nodes
    )

def current_controlled_current_source(id: str, nodes: tuple[str, str], current_gain: float, *, control_branch: str, **_) -> Component:
    if len(nodes) != 2:
        raise ValueError('Current controlled current source output nodes must contain two nodes.')
    if len(control_branch) == 0:
        raise ValueError('Current controlled current source control branch must not be empty.')
    return Component(
        type='current_controlled_current_source',
        id=id,
        value={'current_gain': current_gain, 'control_branch': control_branch},
        nodes=nodes
    )

def voltage_controlled_voltage_source(id: str, nodes: tuple[str, str], voltage_gain: float, *, control_nodes: tuple[str, str], **_) -> Component:
    if len(nodes) != 2:
        raise ValueError('Voltage controlled voltage source output nodes must contain two nodes.')
    if len(control_nodes) != 2:
        raise ValueError('Voltage controlled voltage source control nodes must contain two nodes.')
    control_nodes = tuple(control_nodes)
    return Component(
        type='voltage_controlled_voltage_source',
        id=id,
        value={'voltage_gain': voltage_gain, 'control_nodes': control_nodes},
        nodes=nodes
    )

def operational_amplifier(id: str, nodes: tuple[str, str], *, input_nodes: tuple[str, str], gain: float = 100_000, **_) -> Component:
    if len(nodes) != 2:
        raise ValueError('Operational amplifier output nodes must contain two nodes.')
    if len(input_nodes) != 2:
        raise ValueError('Operational amplifier input nodes must contain two nodes.')
    input_nodes = tuple(input_nodes)
    return Component(
        type='operational_amplifier',
        id=id,
        value={'gain': gain, 'input_nodes': input_nodes},
        nodes=nodes
    )

def current_controlled_voltage_source(id: str, nodes: tuple[str, str], transresistance: float, *, control_branch: str, **_) -> Component:
    if len(nodes) != 2:
        raise ValueError('Current controlled voltage source output nodes must contain two nodes.')
    if len(control_branch) == 0:
        raise ValueError('Current controlled voltage source control branch must not be empty.')
    return Component(
        type='current_controlled_voltage_source',
        id=id,
        value={'transresistance': transresistance, 'control_branch': control_branch},
        nodes=nodes
    )

def periodic_current_source(id: str, nodes: tuple[str, str], wavetype: str, I: float, w: float, phi: float, G: float = 0, **_) -> Component:
    return Component(
        type='periodic_current_source',
        id=id,
        value={'wavetype': wavetype,
               'I': I,
               'w': w,
               'phi': phi,
               'G': G},
        nodes=nodes
        )

def lamp(id: str, nodes: tuple[str, str], P: float, V_ref: float, **_) -> Component:
    if P < 0:
        raise ValueError('P must be greater than zero.')
    if V_ref < 0:
        raise ValueError('V_ref must be greater than zero.')
    return Component(
        type='lamp',
        id=id,
        value={'P': P, 'V_ref': V_ref},
        nodes=nodes
        )

def resistive_load(id: str, nodes: tuple[str, str], P: float, V_ref: float, **_) -> Component:
    if P < 0:
        raise ValueError('P must be greater than zero.')
    if V_ref < 0:
        raise ValueError('V_ref must be greater than zero.')
    return Component(
        type='resistive_load',
        id=id,
        value={'P': P, 'V_ref': V_ref},
        nodes=nodes
        )

def switch(id: str, nodes: tuple[str, str], state: str = 'open', **_) -> Component:
    if state not in ['open', 'closed']:
        raise ValueError("Switch state must be 'open' or 'closed'.")
    return Component(
        type='switch',
        id=id,
        value={'state': state},
        nodes=nodes
    )

def short_circuit(id: str, nodes: tuple[str, str], **_) -> Component:
    return Component(
        type='short_circuit',
        id=id,
        nodes=nodes
    )        

def open_circuit(id: str, nodes: tuple[str, str], **_) -> Component:
    return Component(
        type='open_circuit',
        id=id,
        nodes=nodes
    )        
