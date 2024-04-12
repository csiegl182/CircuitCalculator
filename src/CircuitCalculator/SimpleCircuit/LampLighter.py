from .Elements import Schematic
from .DiagramTranslator import SchematicDiagramParser, circuit_translator
from ..Circuit.solution import ComplexSolution
import schemdraw
import matplotlib as mpl
from typing import Callable

def light_lamps(schematic: Schematic, on_threshold_percentage: float = 0.1, breakthrough_threshold_percentage: float = 1.2) -> None:
    def light_color(brightness: float) -> tuple[float, float, float]:
        colormap: Callable[[float], tuple[float, float, float]] = mpl.colormaps['YlOrRd']
        if brightness <= on_threshold_percentage:
            return (1, 1, 1)
        if brightness >= breakthrough_threshold_percentage:
            return (0.2, 0.2, 0.2)
        return colormap(1-brightness)
    diagram_parser = SchematicDiagramParser(schematic)
    solution = ComplexSolution(circuit=circuit_translator(schematic))
    lamps = [component for component in solution.circuit.components if component.type == 'lamp']
    brightness_percentages = [solution.get_power(lamp.id).real/float(lamp.value['P']) for lamp in lamps]
    for lamp, brght_pct in zip(lamps, brightness_percentages):
        schemdraw_lamp = diagram_parser.get_element(lamp.id)
        schemdraw_lamp.segments.append(schemdraw.SegmentCircle((0.5, 0), 0.5, color=light_color(brght_pct), fill=True, zorder=-100))