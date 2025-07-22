from .Elements import Schematic
from .DiagramTranslator import SchematicDiagramParser, circuit_translator
from ..Circuit.solution import complex_solution
import schemdraw
import matplotlib as mpl
from typing import Callable

def linear_colormap(start_color: tuple[float, float, float], end_color: tuple[float, float, float], num_samples: int) -> Callable[[float], tuple[float, float, float]]:
    return mpl.colors.LinearSegmentedColormap.from_list('light_bulb', [start_color, end_color], num_samples)

def light_lamps(schematic: Schematic, on_threshold_percentage: float = 0.05, breakthrough_threshold_percentage: float = 1.2) -> None:
    def light_color(brightness: float) -> tuple[float, float, float]:
        colormap: Callable[[float], tuple[float, float, float]] = linear_colormap((1.0, 0.62, 0.24), (0.97, 1.0, 0.52), 256)
        if brightness <= on_threshold_percentage:
            return (1, 1, 1)
        if brightness >= breakthrough_threshold_percentage:
            return (0.2, 0.2, 0.2)
        return colormap(brightness)
    diagram_parser = SchematicDiagramParser(schematic)
    circuit = circuit_translator(schematic)
    solution = complex_solution(circuit)
    lamps = [component for component in circuit.components if component.type == 'lamp']
    brightness_percentages = [solution.get_power(lamp.id).real/float(lamp.value['P']) for lamp in lamps]
    for lamp, brght_pct in zip(lamps, brightness_percentages):
        schemdraw_lamp = diagram_parser.get_element(lamp.id)
        schemdraw_lamp.segments.append(schemdraw.SegmentCircle((0.5, 0), 0.5, color=light_color(brght_pct), fill=True, zorder=-100))