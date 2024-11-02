import json
import yaml
from typing import Optional
from CircuitCalculator.SimpleCircuit.DiagramSolution import real_network_dc_solution
import CircuitCalculator.SimpleCircuit.Elements as elm
from matplotlib.axes import Axes

element_handlers = {
    'resistor': lambda kwargs: element_factory(elm.Resistor, **kwargs),
    'line': lambda kwargs: element_factory(elm.LabeledLine, **kwargs) if 'name' in kwargs.keys() else element_factory(elm.Line, **kwargs),
    'node': lambda kwargs: element_factory(elm.Node, **kwargs),
    'ground': lambda kwargs: element_factory(elm.Ground, **kwargs),
    'voltage_source': lambda kwargs: element_factory(elm.VoltageSource, **kwargs),
    'current_source': lambda kwargs: element_factory(elm.CurrentSource, **kwargs),
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

def analyze_circuit(data: dict, ax: Optional[Axes] = None) -> None:
    def fill(schematic: elm.Schematic, elements: list[elm.Element], unit: float) -> None:
        for e in elements:
            se = transform_to_schematic_element(e)
            se = apply_direction_and_length(se, e.get('direction', ''), e.get('length', 1), unit)
            se = apply_position(se, get_placed_element(schematic, e.get('place_after', None)))
            schematic += se
        if dc_solution:
            schematic_solution = real_network_dc_solution(schematic=schematic)
            for v in dc_solution.get('voltages', []):
                schematic += schematic_solution.draw_voltage(**v)
            for c in dc_solution.get('currents', {}):
                schematic += schematic_solution.draw_current(**c)
            for p in dc_solution.get('potentials', {}):
                schematic += schematic_solution.draw_potential(**p)
            for p in dc_solution.get('powers', {}):
                schematic += schematic_solution.draw_power(**p)
    circuit_definiton = data.get('circuit', {'unit': 7, 'elements': []})
    unit = circuit_definiton['unit']
    elements = circuit_definiton['elements']
    if len(elements) == 0:
        raise ValueError('No elements in circuit definition')

    analysis = data.get('analysis', {})
    dc_solution = analysis.get('dc_solution', [])

    if ax is None:
        with elm.Schematic(unit=unit) as schematic:
            fill(schematic=schematic, elements=elements, unit=unit)
    else:
        schematic = elm.Schematic(unit=unit, canvas=ax)
        fill(schematic=schematic, elements=elements, unit=unit)
        schematic.draw(show=False)

def json_loader(file: str) -> dict:
    with open(file) as f:
        return json.load(f)

def yaml_loader(file: str) -> dict:
    with open(file) as f:
        return yaml.safe_load(f)

def load_simulation_data(file: str) -> dict:
    try:
        return json_loader(file)
    except json.JSONDecodeError:
        pass
    try:
        return yaml_loader(file)
    except yaml.YAMLError:
        pass
    raise ValueError('File has unknown data format')

def simulate(file: str) -> None:
    data = load_simulation_data(file)
    analyze_circuit(data)