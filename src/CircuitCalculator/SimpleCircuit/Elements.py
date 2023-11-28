import schemdraw, schemdraw.elements, schemdraw.util
from . import schemdraw_element_extension as extension

from . import Display as dsp

import numpy as np

from typing import Any
from enum import Enum
from abc import ABC

def round_node(node: schemdraw.util.Point) -> schemdraw.util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return schemdraw.util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: schemdraw.elements.Element, n_labels: tuple[str, ...]=('start', 'end')) -> list[schemdraw.util.Point]:
    try:
        return [round_node(element.absanchors[n_label]) for n_label in n_labels]
    except KeyError:
        return []

def get_node_direction(node1: schemdraw.util.Point, node2: schemdraw.util.Point) -> tuple[int, int]:
    delta = node2 - node1
    delta_x = +1 if delta.x >= 0 else -1
    delta_y = +1 if delta.y >= 0 else -1
    return delta_x, delta_y

def is_reverse(element: schemdraw.elements.Element) -> bool:
    n1, n2 = get_nodes(element)
    dx, dy = get_node_direction(n1, n2)
    if dx < 0 or dy < 0:
        return True
    return False

def segments_of(element: schemdraw.elements.Element) -> list[schemdraw.segments.SegmentType]:
    return element.segments

class SwitchState(Enum):
    OPEN = False
    CLOSED = True

class Schematic(schemdraw.Drawing):
    def __init__(self, unit=7, **kwargs):
        super().__init__(unit=unit, **kwargs)

    def __getitem__(self, id: str) -> schemdraw.elements.Element:
        names = [e.name for e in self.elements if hasattr(e, 'name')]
        try:
            index = names.index(id)
        except ValueError:
            raise KeyError
        return self.elements[index]

    def clear_labels(self) -> None:
        self.elements = [e for e in self.elements if not isinstance(e, VoltageLabel) and not isinstance(e, CurrentLabel)]

    def draw(self, *args, **kwargs):
        if self.fig is not None:
            self.fig.clear()
        return super().draw(*args, **kwargs)

    def save_copy(self, fname: str, **kwargs) -> None:
        import copy
        cpy = copy.deepcopy(self)
        cpy.save(fname, **kwargs)

class SimpleAnalysisElement(ABC):
    def __init__(self, *, name: str, reverse: bool = False):
        self._name = name
        self._reverse = reverse

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_reverse(self) -> bool:
        return self._reverse

    def values(self) -> dict[str, complex]:
        ...

def simple_analysis_element(element):
    class decorated_element(element, SimpleAnalysisElement):
        def __init__(self, *args, **kwargs):
            element.__init__(self, *args, **kwargs)
            SimpleAnalysisElement.__init__(self, name=kwargs['name'], reverse=kwargs.get('reverse', False))
    return decorated_element

@extension.source
@simple_analysis_element
class VoltageSource(schemdraw.elements.SourceV):
    def __init__(self, *args, name: str, V: float, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        self._V = V if not reverse else -V
        label = dsp.print_real(V, unit='V', precision=precision)
        self.label(f'{name}={label}', rotate=True, color=dsp.blue, loc='value_label', halign='center', valign='center')
        self.segments.append(extension.voltage_arrow())

    @property
    def V(self) -> float:
        return self._V

    def values(self) -> dict[str, float]:
        return {'V' : self.V}

@extension.source
@simple_analysis_element
class ComplexVoltageSource(schemdraw.elements.SourceV):
    def __init__(self, *args, name: str, V: complex, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        self._V = V if not reverse else -V
        label = dsp.print_complex(V, unit='V', precision=precision)
        self.label(f'{name}={label}', rotate=True, color=dsp.blue, loc='value_label', halign='center', valign='center')
        self.segments.append(extension.voltage_arrow())

    @property
    def V(self) -> complex:
        return self._V

    def values(self) -> dict[str, complex]:
        return {'V' : self.V}

@extension.source
@simple_analysis_element
class CurrentSource(schemdraw.elements.SourceI):
    def __init__(self, *args, I: float, name: str, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I if not reverse else -I
        label = dsp.print_complex(I, unit='A', precision=precision)
        self.label(f'{name}={label}', loc='i_label', ofst=(0, 0.4), rotate=True, color=dsp.red)
        self.segments.append(extension.current_arrow())

    @property
    def I(self) -> float:
        return self._I

    def values(self) -> dict[str, float]:
        return {'I' : self.I}

@extension.source
@simple_analysis_element
class ComplexCurrentSource(schemdraw.elements.SourceI):
    def __init__(self, *args, I: complex, name: str, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I if not reverse else -I
        label = dsp.print_complex(I, unit='A', precision=precision)
        self.label(f'{name}={label}', loc='i_label', ofst=(0, 0.4), rotate=True, color=dsp.red)
        self.segments.append(extension.current_arrow())

    @property
    def I(self) -> complex:
        return self._I

    def values(self) -> dict[str, complex]:
        return {'I' : self.I}

@extension.resistor
@simple_analysis_element
class Resistor(schemdraw.elements.Resistor):
    def __init__(self, *args, R: float, name: str, show_name: bool = True, show_value: bool = True, reverse: bool = False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._R = R
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_resistance(self.R) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> dict[str, float]:
        return {'R' : self._R}

@extension.resistor
@simple_analysis_element
class Conductance(schemdraw.elements.Resistor):
    def __init__(self, *args, G: float, name: str, show_name: bool = True, show_value: bool = True, reverse: bool = False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._G = G
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_conductance(self.G) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def R(self) -> float:
        return 1/self._G

    @property
    def G(self) -> float:
        return self._G

    def values(self) -> dict[str, float]:
        return {'G' : self._R}

@extension.resistor
@simple_analysis_element
class Impedance(schemdraw.elements.Resistor):
    def __init__(self, *args, Z: complex, name: str, show_name: bool = True, show_value: bool = True, precision: int = 3, reverse: bool = False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._Z = Z
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_impedance(self.Z, precision=precision) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def Z(self) -> complex:
        return self._Z

    @property
    def Y(self) -> complex:
        return 1/self._Z

    def values(self) -> dict[str, complex]:
        return {'Z' : self._Z}

@extension.source
@simple_analysis_element
class ACVoltageSource(schemdraw.elements.SourceSin):
    def __init__(self, V: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, precision=3, label_offset: float = 0.2, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        self._V = V if not reverse else -V
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        label = dsp.print_sinosoidal(V*np.exp(1j*phi), unit='V', precision=precision, w=w, deg=deg)
        self.label(f'{name}={label}', rotate=True, color=dsp.blue, loc='value_label', halign='center', valign='center')

    @property
    def w(self) -> float:
        return self._w

    @property
    def phi(self) -> float:
        return self._phi

    @property
    def sin(self) -> bool:
        return self._sin

    @property
    def deg(self) -> bool:
        return self._deg

    @property
    def V(self) -> float:
        return self._V

    def values(self) -> dict[str, complex]:
        return {'U' : self.V}

@extension.source
@simple_analysis_element
class ACCurrentSource(schemdraw.elements.SourceSin):
    def __init__(self, *args, I: float, w: float, phi: float, name: str, sin=False, deg=False, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I if not reverse else -I
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        label = dsp.print_sinosoidal(I*np.exp((1j*phi)), unit='A', precision=precision, w=w, deg=deg)
        self.label(f'{name}={label}', loc='i_label', ofst=(0, 0.4), rotate=True, color=dsp.red)
        self.segments.append(extension.current_arrow())

    @property
    def w(self) -> float:
        return self._w

    @property
    def phi(self) -> float:
        return self._phi

    @property
    def sin(self) -> bool:
        return self._sin

    @property
    def deg(self) -> bool:
        return self._deg

    @property
    def I(self) -> float:
        return self._I

    def values(self) -> dict[str, complex]:
        return {'I' : self.I}

@extension.source
@simple_analysis_element
class RectVoltageSource(schemdraw.elements.SourceSquare):
    def __init__(self, V: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        self._V = V if not reverse else -V
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        self.segments.append(extension.voltage_arrow())
        self.label(f'{name}', loc='value_label', halign='center', rotate=True, color=dsp.blue)

    @property
    def w(self) -> float:
        return self._w

    @property
    def phi(self) -> float:
        return self._phi

    @property
    def sin(self) -> bool:
        return self._sin

    @property
    def deg(self) -> bool:
        return self._deg

    @property
    def V(self) -> float:
        return self._V

    def values(self) -> dict[str, complex]:
        return {'U' : self.V}

@simple_analysis_element
class RectCurrentSource(schemdraw.elements.SourceSquare):
    def __init__(self, I: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, **kwargs):
        super().__init__(self, *args, reverse=reverse, **kwargs)
        self._I = I if not reverse else -I
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        self.segments.append(extension.current_arrow())
        self.label(f'{name}', loc='i_label', halign='center', rotate=True, color=dsp.red)

    @property
    def w(self) -> float:
        return self._w

    @property
    def phi(self) -> float:
        return self._phi

    @property
    def sin(self) -> bool:
        return self._sin

    @property
    def deg(self) -> bool:
        return self._deg

    @property
    def I(self) -> float:
        return self._I

    def values(self) -> dict[str, complex]:
        return {'I' : self.I}

@extension.capacitor
@simple_analysis_element
class Capacitor(schemdraw.elements.Capacitor):
    def __init__(self, C: float, name: str, *args, show_name: bool = True, show_value: bool = True, reverse: bool = False, **kwargs):
        self._C = C
        super().__init__(*args, reverse=reverse, **kwargs)
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_capacitance(C) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def C(self) -> float:
        return self._C

    def values(self) -> dict[str, float]:
        return {'C' : self._C}

@extension.inductor
@simple_analysis_element
class Inductance(schemdraw.elements.Inductor):
    def __init__(self, L: float, name: str, *args, show_name: bool = True, show_value: bool = True, label_offset: float = 0.2, reverse: bool = False, **kwargs):
        self._L = L
        super().__init__(*args, reverse=reverse, **kwargs)
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_inductance(L) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def L(self) -> float:
        return self._L

    def values(self) -> dict[str, float]:
        return {'L$' : self._L}

class RealCurrentSource(schemdraw.elements.Element2Term, SimpleAnalysisElement):
    def __init__(self, current_source: CurrentSource, resistor: Resistor, *args, zoom_resistor: float = 0.7, name: str = '', reverse: bool = False, **kwargs):
        if current_source.is_reverse:
            reverse = not reverse
        super().__init__(*args, reverse=reverse, **kwargs)
        SimpleAnalysisElement.__init__(self, name=current_source.name, reverse=reverse)
        self.segments += segments_of(current_source)
        transform = schemdraw.transform.Transform(theta = 0, globalshift=((1-zoom_resistor)/2,-1.5), localshift=(0, 0), zoom=zoom_resistor)
        self.segments += [s.xform(transform) for s in segments_of(resistor)]
        left_line = schemdraw.Segment([(-1, 0), (-1, -1.5), ((1-zoom_resistor)/2, -1.5)])
        right_line = schemdraw.Segment([(2, 0), (2, -1.5), ((1+zoom_resistor)/2, -1.5)])
        self.segments += [left_line, right_line]
        self.anchors['value_label'] = (0.5, -1.2)
        self.anchors['i_label'] = current_source.anchors['i_label']
        self.anchors['v_label'] = (0.5, -2.4)
        self._userlabels += current_source._userlabels
        self._userlabels += resistor._userlabels
        self._I = current_source.I
        self._R = resistor.R

    @property
    def I(self) -> complex:
        return self._I

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> dict[str, complex]:
        return {'I' : self.I, 'R' : self.R}

class RealVoltageSource(schemdraw.elements.Element2Term, SimpleAnalysisElement):
    def __init__(self, voltage_source: VoltageSource, resistor: Resistor, *args, reverse: bool = False, **kwargs):
        reverse_voltage_source = not voltage_source.is_reverse
        if reverse_voltage_source:
            reverse = not reverse
        schemdraw.elements.Element2Term.__init__(self, *args, reverse=reverse_voltage_source, **kwargs)
        SimpleAnalysisElement.__init__(self, name=voltage_source.name, reverse=reverse_voltage_source)
        transform_resistor = schemdraw.transform.Transform(theta = 0, globalshift=(0, 0))
        transform_voltage_source = schemdraw.transform.Transform(theta = 0, globalshift=(3, 0))
        if reverse:
            transform_resistor, transform_voltage_source = transform_voltage_source, transform_resistor
        self.segments.append(schemdraw.segments.Segment([(0, 0), (0, 0), schemdraw.elements.elements.gap, (1, 0), (3, 0), schemdraw.elements.elements.gap, (4, 0), (4, 0)]))
        self.segments.extend([s.xform(transform_resistor) for s in segments_of(resistor)])
        self.segments.extend([s.xform(transform_voltage_source) for s in segments_of(voltage_source)])
        for a, p in voltage_source.anchors.items():
            self.anchors[a+'_vs'] = transform_voltage_source.transform(p)
        for a, p in resistor.anchors.items():
            self.anchors[a+'_res'] = transform_resistor.transform(p)
        voltage_source_labels = [l for l in voltage_source._userlabels]
        resistor_labels = [l for l in resistor._userlabels]
        for l in voltage_source_labels:
            if type(l.loc) == str:
                l.loc += '_vs'
        for l in resistor_labels:
            if type(l.loc) == str:
                l.loc += '_res'
        self._userlabels += voltage_source._userlabels
        self._userlabels += resistor._userlabels
        self._V = -voltage_source.V
        self._R = resistor.R
        self.anchors['v_label'] = (2, -1.5)

    @property
    def V(self) -> complex:
        return self._V

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> dict[str, float]:
        return {'I' : self.I, 'R' : self.R}

class Line(schemdraw.elements.lines.Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return ''

@simple_analysis_element
class Node(schemdraw.elements.Element):
    def __init__(self, *args, name: str = '', **kwargs):
        super().__init__(*args, name=name, **kwargs)
        self.node_id = name
        self.params['theta'] = 0
        self.params['drop'] = (0, 0)
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)
        self.anchors['NE'] = (0.5, 0.1)
        self.anchors['NW'] = (-0.5, 0.1)
        self.anchors['SE'] = (0.5, -0.3)
        self.anchors['SW'] = (-0.5, -0.3)

class LabelNode(Node):
    def __init__(self, id_loc : str | dict[str, str] = '', *args, name: str = '', show=True, **kwargs):
        super().__init__(*args, name=name, **kwargs)
        locations = {
            'W': {'loc': 'left', 'halign': 'right', 'valign': 'center'},
            'N': {'loc': 'top', 'halign': 'center', 'valign': 'bottom'},
            'NE': {'loc': 'NE', 'halign': 'left', 'valign': 'bottom'},
            'NW': {'loc': 'NW', 'halign': 'right', 'valign': 'bottom'},
            'E': {'loc': 'right', 'halign': 'left', 'valign': 'center'},
            'S': {'loc': 'bottom', 'halign': 'center', 'valign': 'top'},
            'SW': {'loc': 'SW', 'halign': 'right', 'valign': 'top'},
            'SE': {'loc': 'SE', 'halign': 'left', 'valign': 'top'}
        }
        self.segments.append(schemdraw.SegmentCircle((0, 0), 0.12, fill='black'))
        self.id_loc = {}
        if isinstance(id_loc, str):
            self.id_loc.update(locations.get(id_loc, {}))
        else:
            self.id_loc.update(id_loc)
        if show:
            self.show()

    def show(self):
        self.segments.append(schemdraw.SegmentCircle((0, 0), 0.12, fill='black'))
        self.bbox = self.get_bbox(includetext=False)
        self.label(f'{self.name}', **self.id_loc)

class Switch(schemdraw.elements.elements.Element2Term):
    def __init__(self, name: str, *args, state: SwitchState = SwitchState.OPEN, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state
        self._name = name
        self.segments.append(schemdraw.Segment([(0, 0), schemdraw.elements.elements.gap, (1, 0)]))
        self.segments.append(schemdraw.SegmentCircle((schemdraw.elements.switches.sw_dot_r, 0), schemdraw.elements.switches.sw_dot_r, fill='bg', zorder=3))
        self.segments.append(schemdraw.SegmentCircle((1-schemdraw.elements.switches.sw_dot_r, 0), schemdraw.elements.switches.sw_dot_r, fill='bg', zorder=3))
        self.segments.append(schemdraw.Segment([(0,0)]))
        if self.state == SwitchState.OPEN:
            self.open()
        if self.state == SwitchState.CLOSED:
            self.close()

    @property
    def name(self) -> str:
        return self._name

    def open(self) -> None:
        self.state = SwitchState.OPEN
        self.segments.pop()
        self.segments.append(schemdraw.Segment([(schemdraw.elements.switches.sw_dot_r, 0), (1, 0.6)]))

    def close(self) -> None:
        self.state = SwitchState.CLOSED
        self.segments.pop()
        self.segments.append(schemdraw.Segment([(schemdraw.elements.switches.sw_dot_r, 0), (1, schemdraw.elements.switches.sw_dot_r*1.2)]))

    def toggle(self) -> None:
        if self.state == self.state.OPEN:
            self.close()
        if self.state == self.state.CLOSED:
            self.open()

class Ground(Node):
    def __init__(self, id: str = '0', *args, **kwargs):
        super().__init__(id, *args, name=id, **kwargs)
        gndgap = 0.12
        gnd_lead = 0.4
        resheight = schemdraw.elements.twoterm.resheight
        gap = schemdraw.elements.elements.gap
        self.segments.append(schemdraw.Segment(
            [(0, 0), (0, -gnd_lead), (-resheight, -gnd_lead),
             (resheight, -gnd_lead), gap, (-resheight*.7, -gndgap-gnd_lead),
             (resheight*.7, -gndgap-gnd_lead), gap,
             (-resheight*.2, -gndgap*2-gnd_lead),
             (resheight*.2, -gndgap*2-gnd_lead)]))

    @property
    def name(self) -> str:
        return 'Ground'

    def up(self) -> schemdraw.elements.Element:
        return super().left()

    def down(self) -> schemdraw.elements.Element:
        return super().right()

    def left(self) -> schemdraw.elements.Element:
        return super().down()

    def right(self) -> schemdraw.elements.Element:
        return super().up()

class VoltageLabel(schemdraw.elements.CurrentLabel):
    def __init__(self, at: schemdraw.elements.Element, label: str = '', label_loc: str = 'bottom', reverse: bool = False, **kwargs):
        kwargs.update({'color': kwargs.get('color', dsp.blue)})
        kwargs.update({'headlength': kwargs.get('headlength', 0.4)})
        kwargs.update({'headwidth': kwargs.get('headwidth', 0.3)})
        if isinstance(at, RealVoltageSource):
            kwargs.update({'length': kwargs.get('length', 4)})
        super().__init__(reverse=reverse, **kwargs)
        try:
            self.at(at.v_label)
            self.theta(at.transform.theta)
        except AttributeError:
            self.at(at)
        rotate = kwargs.get('rotate', True)
        if rotate == True and at.transform.theta == 270:
            rotate = 90
        self.label(label, rotate=rotate, loc=label_loc, ofst=(0, -0.1))

class CurrentLabel(schemdraw.elements.CurrentLabelInline):
    def __init__(self, at: schemdraw.elements.Element, label: str = '', **kwargs):
        kwargs.update(i_label_args.get(type(at), {}))
        kwargs.update({'color': kwargs.get('color', dsp.red)})
        kwargs.update({'headlength': kwargs.get('headlength', 0.4)})
        kwargs.update({'headwidth': kwargs.get('headwidth', 0.3)})
        totlen = at._userparams.get('l', at._userparams.get('unit', 3))
        kwargs.update({'ofst': totlen/4-0.15+kwargs.get('ofst', 0)})
        start = kwargs.get('start', True)
        reverse = kwargs.get('reverse', False)
        if isinstance(at, RealVoltageSource) or isinstance(at, RealCurrentSource): # when replacing CurrentLabelInline this dependency may be removed
            reverse = not reverse
        kwargs.update({'start' : start, 'reverse' : reverse})
        super().__init__(**kwargs)
        self.at(at)
        self.label(label)

class PowerLabel(schemdraw.elements.Label):
    def __init__(self, at: schemdraw.elements.Element, label: str = '', **kwargs):
        kwargs.update({'color': kwargs.get('color', dsp.green)})
        super().__init__(**kwargs)
        try:
            self.at(at.s_label)
            self.theta(at.transform.theta)
        except AttributeError:
            self.at(at.center)
        rotate = kwargs.get('rotate', True)
        if rotate == True and at.transform.theta == 270:
            rotate = 90
        self.label(label, rotate=rotate, halign='center')

i_label_args : dict[Any, dict[str, float]] = {
    Resistor : {'ofst' : 1.4},
    Impedance : {'ofst' : 1.4},
    Capacitor : {'ofst' : 1.4},
    Inductance : {'ofst' : 1.4},
    VoltageSource : {'ofst' : -2.8},
    ComplexVoltageSource : {'ofst' : -2.8},
    CurrentSource : {'ofst' : -2.8},
    ComplexCurrentSource : {'ofst' : -2.8},
    ACVoltageSource : {'ofst' : -3.8},
    RealVoltageSource: {'ofst' : -0.8},
    RealCurrentSource: {'ofst' : 1.4}
}