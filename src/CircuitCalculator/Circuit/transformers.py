import numpy as np
from ..Network import elements as elm
from ..Network import network as ntw
from typing import Callable, TypeVar
from .Components import components as cp
from ..SignalProcessing.periodic_functions import periodic_function, fourier_series

CircuitComponent = TypeVar("CircuitComponent", bound=cp.Component)
CircuitComponentTranslator = Callable[[cp.Component, float, float, bool], ntw.Branch]

def resistor(resistor: cp.Component, *_) -> ntw.Branch:
    R = float(resistor.value['R'])
    return ntw.Branch(resistor.nodes[0], resistor.nodes[1], elm.resistor(resistor.id, R))

def impedance(impedance: cp.Component, *_) -> ntw.Branch:
    Z = complex(
        float(impedance.value['R']),
        float(impedance.value['X'])
    )
    return ntw.Branch(impedance.nodes[0], impedance.nodes[1], elm.impedance(impedance.id, Z))

def capacitor(capacitor: cp.Component, w: float = 0, *_) -> ntw.Branch:
    C = float(capacitor.value['C'])
    return ntw.Branch(
        capacitor.nodes[0],
        capacitor.nodes[1],
        elm.admittance(capacitor.id, complex(0, w*C)))

def inductance(inductance: cp.Component, w: float = 0, *_) -> ntw.Branch:
    L = float(inductance.value['L'])
    return ntw.Branch(
        inductance.nodes[0],
        inductance.nodes[1],
        elm.impedance(inductance.id, complex(0, w*L))
    )

def dc_voltage_source(voltage_source: cp.Component, w: float = 0, w_resolution: float = 1e-3, *_) -> ntw.Branch:
    V = complex(float(voltage_source.value['V']), 0)
    Z = complex(float(voltage_source.value['R']), 0)
    element = elm.voltage_source(voltage_source.id, V, Z)
    if np.abs(w-float(voltage_source.value['w'])) > w_resolution:
        element = elm.short_circuit(voltage_source.id)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def ac_voltage_source(voltage_source: cp.Component, w: float = 0, w_resolution: float = 1e-3, rms:bool = True) -> ntw.Branch:
    if rms:
        vs_V = float(voltage_source.value['V'])/np.sqrt(2)
    vs_V = float(voltage_source.value['V'])
    vs_phi = float(voltage_source.value['phi'])
    vs_R = float(voltage_source.value['R'])
    element = elm.voltage_source(voltage_source.id, complex(vs_V*np.cos(vs_phi), vs_V*np.sin(vs_phi)), complex(vs_R, 0))
    if np.abs(w-float(voltage_source.value['w'])) > w_resolution:
        element = elm.short_circuit(voltage_source.id)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def complex_voltage_source(voltage_source: cp.Component, *_) -> ntw.Branch:
    cs_V = complex(
        float(voltage_source.value['V_real']),
        float(voltage_source.value['V_imag'])
    )
    cs_Z = complex(
        float(voltage_source.value['R']),
        float(voltage_source.value['X'])
    )
    element = elm.voltage_source(voltage_source.id, cs_V, cs_Z)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def periodic_voltage_source(source: cp.Component, w: float = 0, w_resolution: float = 1e-3, *_) -> ntw.Branch:
    wavetype = str(source.value['wavetype'])
    w0 = float(source.value['w'])
    V = float(source.value['V'])
    phi = float(source.value['phi'])
    frequency_properties = fourier_series(periodic_function(wavetype)(period=2*np.pi/w0, amplitude=V, phase=phi))
    n = np.round(w/w0)
    delta_n = np.abs(w/w0 - n)
    if delta_n > w_resolution/w0:
        return ntw.Branch(
            source.nodes[0],
            source.nodes[1],
            elm.short_circuit(source.id))
    single_frequency_source = cp.ac_voltage_source(
        id=source.id,
        nodes=(source.nodes[0], source.nodes[1]),
        w=w,
        phi=frequency_properties.phase(n),
        V=frequency_properties.amplitude(n)
    )
    return ac_voltage_source(single_frequency_source, w, w_resolution)

def dc_current_source(current_source: cp.Component, w: float = 0, w_resolution: float = 1e-3, *_) -> ntw.Branch:
    cs_I = float(current_source.value['I'])
    cs_G = float(current_source.value['G'])
    cs_w = float(current_source.value['w'])
    element = elm.current_source(current_source.id, complex(cs_I, 0), complex(cs_G, 0))
    if np.abs(w-cs_w) > w_resolution:
        element = elm.open_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def ac_current_source(current_source: cp.Component, w: float = 0, w_resolution: float = 1e-3, rms: bool = True) -> ntw.Branch:
    if rms:
        cs_I = float(current_source.value['I'])/np.sqrt(2)
    cs_I = float(current_source.value['I'])
    cs_G = float(current_source.value['G'])
    cs_w = float(current_source.value['w'])
    cs_phi = float(current_source.value['phi'])
    element = elm.current_source(current_source.id, complex(cs_I*np.cos(cs_phi), cs_I*np.sin(cs_phi)), complex(cs_G, 0))
    if np.abs(w-cs_w) > w_resolution:
        element = elm.open_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def complex_current_source(current_source: cp.Component, w: float = 0, w_resolution: float = 1e-3, *_) -> ntw.Branch:
    cs_I = complex(
        float(current_source.value.get('I_real', 0)),
        float(current_source.value.get('I_imag', 0))
    )
    cs_Y = complex(
        float(current_source.value.get('G', 0)),
        float(current_source.value.get('B', 0))
    )
    cs_w = float(current_source.value.get('w', 0))
    element = elm.current_source(current_source.id, cs_I, cs_Y)
    if np.abs(w-cs_w) > w_resolution:
        element = elm.short_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element)

def periodic_current_source(source: cp.Component, w: float = 0, w_resolution: float = 1e-3, *_) -> ntw.Branch:
    wavetype = str(source.value['wavetype'])
    w0 = float(source.value['w'])
    I = float(source.value['I'])
    phi = float(source.value['phi'])
    frequency_properties = fourier_series(periodic_function(wavetype)(period=2*np.pi/w0, amplitude=I, phase=phi))
    n = np.round(w/w0)
    delta_n = np.abs(w/w0 - n)
    if delta_n > w_resolution/w0:
        return ntw.Branch(
            source.nodes[0],
            source.nodes[1],
            elm.open_circuit(source.id))
    single_frequency_source = cp.ac_current_source(
        id=source.id,
        nodes=(source.nodes[0], source.nodes[1]),
        w=w,
        phi=frequency_properties.phase(n),
        I=frequency_properties.amplitude(n)
    )
    return ac_current_source(single_frequency_source, w, w_resolution)

def short_circuit(short_circuit: cp.Component, *_) -> ntw.Branch:
    return ntw.Branch(
        short_circuit.nodes[0],
        short_circuit.nodes[1],
        elm.short_circuit(short_circuit.id)
    )

def open_circuit(open_circuit: cp.Component, *_) -> ntw.Branch:
    return ntw.Branch(
        open_circuit.nodes[0],
        open_circuit.nodes[1],
        elm.open_circuit(open_circuit.id)
    )

def resistive_load(load: cp.Component, *_) -> ntw.Branch:
    return ntw.Branch(
        load.nodes[0],
        load.nodes[1],
        elm.load(load.id, float(load.value['P']), float(load.value['V_ref']))
    )

transformers : dict[str, CircuitComponentTranslator] = {
    'resistor' : resistor,
    'impedance' : impedance,
    'capacitor' : capacitor,
    'inductance' : inductance,
    'dc_voltage_source' : dc_voltage_source,
    'ac_voltage_source' : ac_voltage_source,
    'complex_voltage_source' : complex_voltage_source,
    'dc_current_source' : dc_current_source,
    'ac_current_source' : ac_current_source,
    'complex_current_source' : complex_current_source,
    'periodic_voltage_source' : periodic_voltage_source,
    'periodic_current_source' : periodic_current_source,
    'short_circuit' : short_circuit,
    'open_circuit' : open_circuit,
    'resistive_load' : resistive_load,
    'lamp' : resistive_load
}