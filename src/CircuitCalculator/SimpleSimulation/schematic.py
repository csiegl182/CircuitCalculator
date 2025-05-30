from typing import Optional
from matplotlib.axes import Axes
from typing import Callable
import CircuitCalculator.SimpleCircuit.Elements as elm
import CircuitCalculator.SimpleCircuit.DiagramParser as dp
import CircuitCalculator.SimpleCircuit.DiagramSolution as ds
import CircuitCalculator.SimpleCircuit.LampLighter as ll
from dataclasses import dataclass
from inspect import signature
from . import errors


solutions = {
    'dc': ds.real_solution,
    'real': ds.real_solution,
    'complex': ds.single_frequency_complex_solution,
    'single_frequency_time_domain': ds.single_frequency_complex_solution
}

@dataclass
class SolutionDefinition:
    data : dict

    @property
    def diagram_solution_creator(self) -> Callable[[elm.Schematic], ds.SchematicDiagramSolution]:
        solution_type = self.data.get('type', 'unknown')
        solution_fcn = solutions.get(solution_type, ds.empty_solution)
        feasible_solution_params = signature(solution_fcn).parameters.keys()
        solution_parameters = {k: v for k, v in self.data.items() if k in feasible_solution_params}
        return lambda schematic: solution_fcn(schematic=schematic, **solution_parameters)

    @property
    def voltages(self) -> list[dict]:
        voltages = self.data.get('voltages', [])
        if voltages is None:
            return []
        return voltages

    @property
    def currents(self) -> list[dict]:
        currents = self.data.get('currents', [])
        if currents is None:
            return []
        return currents

    @property
    def potentials(self) -> list[dict]:
        potentials = self.data.get('potentials', [])
        if potentials is None:
            return []
        return potentials

    @property
    def powers(self) -> list[dict]:
        powers = self.data.get('powers', [])
        if powers is None:
            return []
        return powers

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
    try:
        return element(name=name, reverse=reverse, **kwargs)
    except TypeError as e:
        missing_argument = str(e).split(":")[-1].strip()
        provided_arguments = {}
        if name != '':
            provided_arguments = {'name': name}
        provided_arguments.update(kwargs)
        raise errors.MissingArgument(missing_argument, str(provided_arguments)) from e

def transform_to_schematic_element(element: dict) -> elm.Element:
    try:
        element_type = element['type']
    except KeyError as e:
        raise errors.MissingArgument('type', str(element)) from e
    try:
        return element_handlers[element_type](element)
    except KeyError as e:
        raise errors.UnknownCircuitElement(element_type) from e

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

def fill_schematic(schematic: elm.Schematic, elements: list[elm.Element], unit: int) -> None:
    for e in elements:
        se = transform_to_schematic_element(e)
        se = apply_direction_and_length(se, e.get('direction', ''), e.get('length', 1), unit)
        se = apply_position(se, get_placed_element(schematic, e.get('place_after', None)))
        schematic += se

def fill_solution(schematic: elm.Schematic, light_lamps: bool, solution_definition: SolutionDefinition) -> None:
    if light_lamps:
        ll.light_lamps(schematic)

    try:
        solution = solution_definition.diagram_solution_creator(schematic)
    except ValueError as e:
        raise errors.IllegalElementValue(str(e)) from e
    for v in solution_definition.voltages:
        try:
            schematic += solution.draw_voltage(**v)
        except dp.UnknownElement as e:
            print(f'Cannot draw voltage of undefined element "{str(e)}".')
        except TypeError as e:
            unknown_argument = str(e).split()[-1].strip()
            raise errors.UnknownArgument(unknown_argument, 'voltages') from e
    for c in solution_definition.currents:
        try:
            schematic += solution.draw_current(**c)
        except dp.UnknownElement as e:
           print(f'Cannot draw current of undefined element "{str(e)}".')
        except TypeError as e:
            unknown_argument = str(e).split()[-1].strip()
            raise errors.UnknownArgument(unknown_argument, 'currents') from e
    for p in solution_definition.potentials:
        try:
            schematic += solution.draw_potential(**p)
        except dp.UnknownElement as e:
           print(f'Cannot draw potential of undefined node "{str(e)}".')
        except TypeError as e:
            unknown_argument = str(e).split()[-1].strip()
            raise errors.UnknownArgument(unknown_argument, 'potential') from e
    for p in solution_definition.powers:
        try:
            schematic += solution.draw_power(**p)
        except dp.UnknownElement as e:
           print(f'Cannot draw power of undefined element "{str(e)}".')
        except TypeError as e:
            unknown_argument = str(e).split()[-1].strip()
            raise errors.UnknownArgument(unknown_argument, 'powers') from e

def parse_circuit_data(data: dict) -> dict:
    circuit_definiton = data.get('circuit', {'unit': 7, 'elements': [], 'solution': {'type': None}})
    if len(circuit_definiton['elements']) == 0:
        raise errors.EmptyCircuit('No elements in circuit definition')
    return circuit_definiton

def create_schematic(circuit_data: dict) -> elm.Schematic:
    circuit_data = parse_circuit_data(circuit_data)
    unit = circuit_data.get('unit', 7)
    elements = circuit_data.get('elements', [])
    schematic = elm.Schematic(unit=unit)
    fill_schematic(schematic, elements, unit)
    return schematic

def draw_schematic(circuit_data: dict, circuit_ax: Optional[Axes] = None) -> elm.Schematic:
    circuit_data = parse_circuit_data(circuit_data)
    unit = circuit_data.get('unit', 7)
    elements = circuit_data.get('elements', [])
    light_lamps = circuit_data.get('light_lamps', False)
    solution_definition = SolutionDefinition(circuit_data.get('solution', {}))
    if circuit_ax is None:
        with elm.Schematic(unit=unit) as schematic:
            fill_schematic(schematic, elements, unit)
            fill_solution(schematic, light_lamps, solution_definition)
        return schematic
    schematic = elm.Schematic(unit=circuit_data['unit'], canvas=circuit_ax)
    fill_schematic(schematic, elements, unit)
    fill_solution(schematic, light_lamps, solution_definition)
    schematic.draw(show=False)
    return schematic