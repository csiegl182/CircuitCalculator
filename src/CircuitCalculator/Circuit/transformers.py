import numpy as np
from ..Network import elements as elm
from ..Network import network as ntw
from typing import Callable, TypeVar
from . import components as ccp
from ..SignalProcessing.periodic_functions import periodic_function, fourier_series

CircuitComponent = TypeVar("CircuitComponent", bound=ccp.Component)
CircuitComponentTranslator = Callable[[ccp.Component, float, float], ntw.Branch]

def resistor(resistor: ccp.Component, *_) -> ntw.Branch:
    return ntw.Branch(resistor.nodes[0], resistor.nodes[1], elm.resistor(resistor.id, float(resistor.value['R'])))

def impedance(impedance: ccp.Component, *_) -> ntw.Branch:
    return ntw.Branch(impedance.nodes[0], impedance.nodes[1], elm.impedance(impedance.id, complex(float(impedance.value['R']), float(impedance.value['X']))))

def capacitor(capacitor: ccp.Component, w: float = 0, *_) -> ntw.Branch:
    return ntw.Branch(
        capacitor.nodes[0],
        capacitor.nodes[1],
        elm.admittance(capacitor.id, elm.admittance_value(B=w*float(capacitor.value['C']))))

def inductance(inductance: ccp.Component, w: float = 0, *_) -> ntw.Branch:
    return ntw.Branch(
        inductance.nodes[0],
        inductance.nodes[1],
        elm.impedance(inductance.id, elm.impedance_value(X=w*float(inductance.value['L'])))
    )

def dc_voltage_source(voltage_source: ccp.Component, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.voltage_source(voltage_source.id, elm.complex_value(float(voltage_source.value['V']), 0), elm.complex_value(float(voltage_source.value['R']), 0))
    if np.abs(w-float(voltage_source.value['w'])) > w_resolution:
        element = elm.short_circuit(voltage_source.id)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def ac_voltage_source(voltage_source: ccp.Component, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.voltage_source(voltage_source.id, elm.complex_value(float(voltage_source.value['V']), float(voltage_source.value['phi'])), elm.complex_value(float(voltage_source.value['R']), 0))
    if np.abs(w-float(voltage_source.value['w'])) > w_resolution:
        element = elm.short_circuit(voltage_source.id)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def complex_voltage_source(voltage_source: ccp.Component, *_) -> ntw.Branch:
    element = elm.voltage_source(voltage_source.id, complex(float(voltage_source.value['V_real']), float(voltage_source.value['V_imag'])), complex(voltage_source.value['R'], voltage_source.value['X']))
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def periodic_voltage_source(source: ccp.Component, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch: # TODO
    pf = periodic_function(str(source.value['wavetype']))
    my_pf = pf(period=2*np.pi/float(source.value['w']), amplitude=float(source.value['V']), phase=float(source.value['phi']))
    frequency_properties = fourier_series(my_pf)
    n = np.round(w/float(source.value['w']))
    delta_n = np.abs(w/float(source.value['w']) - n)
    if delta_n > w_resolution/float(source.value['w']):
        return ntw.Branch(
            source.nodes[0],
            source.nodes[1],
            elm.short_circuit(source.id))
    single_frequency_source = ccp.ac_voltage_source(
        id=source.id,
        nodes=(source.nodes[0], source.nodes[1]),
        w=w,
        phi=frequency_properties.phase(n),
        V=frequency_properties.amplitude(n)
    )
    return ac_voltage_source(single_frequency_source, w, w_resolution)

def dc_current_source(current_source: ccp.Component, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.current_source(current_source.id, elm.complex_value(current_source.value['I'], 0), elm.complex_value(current_source.value['G'], 0))
    if np.abs(w-current_source.value['w']) > w_resolution:
        element = elm.open_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def ac_current_source(current_source: ccp.Component, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.current_source(current_source.id, elm.complex_value(current_source.value['I'], current_source.value['phi']), elm.complex_value(current_source.value['G']))
    if np.abs(w-current_source.value['w']) > w_resolution:
        element = elm.open_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def complex_current_source(current_source: ccp.Component, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.current_source(current_source.id, complex(current_source.value['I_real'], current_source.value['I_imag']), complex(current_source.value['G'], current_source.value['B']))
    if np.abs(w-current_source.value['w']) > w_resolution:
        element = elm.short_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element)

def periodic_current_source(source: ccp.Component, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch: # TODO
    pf = periodic_function(str(source.value['wavetype']))
    my_pf = pf(period=2*np.pi/float(source.value['w']), amplitude=float(source.value['I']), phase=float(source.value['phi']))
    frequency_properties = fourier_series(my_pf)
    n = np.round(w/float(source.value['w']))
    delta_n = np.abs(w/float(source.value['w']) - n)
    if delta_n > w_resolution/float(source.value['w']):
        return ntw.Branch(
            source.nodes[0],
            source.nodes[1],
            elm.open_circuit(source.id))
    single_frequency_source = ccp.ac_current_source(
        id=source.id,
        nodes=(source.nodes[0], source.nodes[1]),
        w=w,
        phi=frequency_properties.phase(n),
        I=frequency_properties.amplitude(n)
    )
    return ac_current_source(single_frequency_source, w, w_resolution)

def linear_current_source(current_source: ccp.LinearCurrentSource, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.linear_current_source(current_source.id, elm.complex_value(current_source.I, 0), elm.complex_value(current_source.G, 0))
    if np.abs(w-current_source.w) > w_resolution:
        element = elm.open_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element)

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
    # cmp.LinearCurrentSource : linear_current_source,
    # cmp.LinearVoltageSource : linear_voltage_source,
    # cmp.PeriodicVoltageSource : periodic_voltage_source,
}