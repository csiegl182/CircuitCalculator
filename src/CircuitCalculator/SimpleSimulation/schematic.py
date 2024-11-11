from typing import Optional
import CircuitCalculator.SimpleCircuit.Elements as elm
from matplotlib.axes import Axes
from typing import Callable
import CircuitCalculator.SimpleCircuit.DiagramSolution as ds
from dataclasses import dataclass
from inspect import signature

solutions = {
    'dc': ds.real_solution,
    'real': ds.real_solution,
    'complex': ds.complex_solution,
    'single_frequency_time_domain': ds.single_frequency_complex_solution
}

@dataclass
class SolutionDefinition:
    data : dict

    @property
    def diagram_solution_creator(self) -> Callable[[elm.Schematic], ds.SchematicDiagramSolution]:
        solution_fcn = solutions.get(self.data['type'], ds.empty_solution)
        feasible_solution_params = signature(solution_fcn).parameters.keys()
        solution_parameters = {k: v for k, v in self.data.items() if k in feasible_solution_params}
        return lambda schematic: solution_fcn(schematic=schematic, **solution_parameters)

    @property
    def voltages(self) -> list[dict]:
        return self.data.get('voltages', [])

    @property
    def currents(self) -> list[dict]:
        return self.data.get('currents', [])

    @property
    def potentials(self) -> list[dict]:
        return self.data.get('potentials', [])

    @property
    def powers(self) -> list[dict]:
        return self.data.get('powers', [])

element_handlers = {
    'resistor': lambda kwargs: element_factory(elm.Resistor, **kwargs),
    'impedance': lambda kwargs: element_factory(elm.Impedance, **kwargs),
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

def fill(schematic: elm.Schematic, elements: list[elm.Element], unit: float, solution_definition: SolutionDefinition) -> None:
    for e in elements:
        se = transform_to_schematic_element(e)
        se = apply_direction_and_length(se, e.get('direction', ''), e.get('length', 1), unit)
        se = apply_position(se, get_placed_element(schematic, e.get('place_after', None)))
        schematic += se

    solution = solution_definition.diagram_solution_creator(schematic)
    for v in solution_definition.voltages:
        schematic += solution.draw_voltage(**v)
    for c in solution_definition.currents:
        schematic += solution.draw_current(**c)
    for p in solution_definition.potentials:
        schematic += solution.draw_potential(**p)
    for p in solution_definition.powers:
        schematic += solution.draw_power(**p)

def create_schematic(circuit_data: dict, circuit_ax: Optional[Axes] = None) -> elm.Schematic:
    unit = circuit_data.get('unit', 7)
    elements = circuit_data.get('elements', [])
    solution_definition = SolutionDefinition(circuit_data.get('solution', {}))
    if circuit_ax is None:
        with elm.Schematic(unit=unit) as schematic:
            fill(schematic, elements, unit, solution_definition)
        return schematic
    schematic = elm.Schematic(unit=circuit_data['unit'], canvas=circuit_ax)
    fill(schematic, elements, unit, solution_definition)
    schematic.draw(show=False)
    return schematic