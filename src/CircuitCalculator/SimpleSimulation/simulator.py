from typing import Optional
from .schematic import create_schematic
import CircuitCalculator.SimpleCircuit.Elements as elm
from matplotlib.axes import Axes
from CircuitCalculator.dump_load import load

element_handlers = {
    'resistor': lambda kwargs: element_factory(elm.Resistor, **kwargs),
    'conductance': lambda kwargs: element_factory(elm.Conductance, **kwargs),
    'impedance': lambda kwargs: element_factory(elm.Impedance, **kwargs),
    'admittance': lambda kwargs: element_factory(elm.Admittance, **kwargs),
    'capacitor': lambda kwargs: element_factory(elm.Capacitor, **kwargs),
    'inductance': lambda kwargs: element_factory(elm.Inductance, **kwargs),
    'line': lambda kwargs: element_factory(elm.LabeledLine, **kwargs) if 'name' in kwargs.keys() else element_factory(elm.Line, **kwargs),
    'node': lambda kwargs: element_factory(elm.Node, **kwargs),
    'lamp': lambda kwargs: element_factory(elm.Lamp, **kwargs),
    'ground': lambda kwargs: element_factory(elm.Ground, **kwargs),
    'voltage_source': lambda kwargs: element_factory(elm.VoltageSource, **kwargs),
    'ac_voltage_source': lambda kwargs: element_factory(elm.ACVoltageSource, **kwargs),
    'complex_voltage_source': lambda kwargs: element_factory(elm.ComplexVoltageSource, **kwargs),
    'current_source': lambda kwargs: element_factory(elm.CurrentSource, **kwargs),
    'ac_current_source': lambda kwargs: element_factory(elm.ACCurrentSource, **kwargs),
    'complex_current_source': lambda kwargs: element_factory(elm.ComplexCurrentSource, **kwargs),
}

def element_factory(element: type[elm.Element], name: str = '', reverse: bool = False, **kwargs) -> elm.Element:
    return element(name=name, reverse=reverse, **kwargs)

def transform_to_schematic_element(element: dict) -> elm.Element:
    try:
        return element_handlers[element['type']](element)
    except KeyError:
        raise ValueError(f'No handler for element type {element["type"]}')

def apply_direction_and_length(element: elm.Element, direction: str = '', length: float = 1, unit: float = 1) -> elm.Element:
    if direction == 'right':
        element.right(length*unit)
    elif direction == 'left':
        element.left(length*unit)
    elif direction == 'up':
        element.up(length*unit)
    elif direction == 'down':
        element.down(length*unit)
    return element

def apply_position(element: elm.Element, origin_element: Optional[elm.schemdraw.elements.Element] = None) -> elm.Element:
    if origin_element is None:
        return element
    return element.at(origin_element.end)

def get_placed_element(schematic: elm.Schematic, label: Optional[str] = None) -> Optional[elm.schemdraw.elements.Element]:
    if label is None:
        return None
    return schematic.elements[[se.name for se in schematic.elements].index(label)]

def simulate(data: dict, circuit_ax: Optional[Axes] = None) -> None:
    circuit_definiton = data.get('circuit', {'unit': 7, 'elements': [], 'solution': {'type': None}})
    if len(circuit_definiton['elements']) == 0:
        raise ValueError('No elements in circuit definition')
    create_schematic(circuit_definiton, circuit_ax)

def simulate_file(name: str) -> None:
    data = load(name)
    simulate(data)