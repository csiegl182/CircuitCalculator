import schemdraw, schemdraw.elements, schemdraw.util

from .SchemdrawDIN import elements as din_elements
from . import Display as dsp

from typing import Any
from enum import Enum

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

class VoltageSource(din_elements.SourceUDIN):
    def __init__(self, V: complex, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._V = V
        if reverse:
            self._V *= -1
        self._name = name
        self.anchors['value_label'] = (0.5, 1.1)
        self.anchors['s_label'] = (0.5, 1.5)
        label = dsp.print_complex(V, unit='V', precision=precision)
        self.label(f'{self._name}={label}', rotate=True, color=dsp.blue, loc='value_label', halign='center', valign='center')

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=dsp.blue))

    def down(self) -> schemdraw.elements.Element:
        self.anchors['s_label'] = (0.5, -0.7)
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def V(self) -> complex:
        return self._V

    def values(self) -> dict[str, complex]:
        return {'U' : self.V}

class Impedance(schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, Z: complex, name: str, *args, show_name: bool = True, show_value: bool = True, precision: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self._Z = Z
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_impedance(self.Z, precision=precision) if show_value else ''
        self.anchors['value_label'] = (0.5, 0.3)
        self.anchors['v_label'] = (0.5, -1.1)
        self.anchors['s_label'] = (0.5, 0.9)
        self.label(label, rotate=True, loc='value_label', halign='center')

    def down(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -0.6)
        self.anchors['v_label'] = (0.5, 0.3)
        self.anchors['s_label'] = (0.5, -1.2)
        return super().down()

    def left(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -0.6)
        self.anchors['v_label'] = (0.5, 0.3)
        self.anchors['s_label'] = (0.5, -1.2)
        return super().left()

    @property
    def name(self) -> str:
        return self._name

    @property
    def Z(self) -> complex:
        return self._Z

    @property
    def Y(self) -> complex:
        return 1/self._Z

    def values(self) -> dict[str, complex]:
        return {'Z' : self._Z}

    def _place_label(self, *args, **kwargs):
        delta = self.end-self.start
        if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
            if delta[1] < 0:
                kwargs.update({'rotation': 90})

        super()._place_label(*args, **kwargs)

class CurrentSource(din_elements.SourceIDIN):
    def __init__(self, I: complex, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I
        if reverse:
            self._I *= -1
        self._name = name
        a, b = (1.2, 0.3), (1.8, 0.3)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=dsp.red))
        self.anchors['I_label'] = a
        label = dsp.print_complex(self._I, unit='A', precision=precision)
        self.label(f'{self._name}={label}', loc='I_label', ofst=(0, 0.4), rotate=True, color=dsp.red)

    @property
    def name(self) -> str:
        return self._name

    @property
    def I(self) -> complex:
        return self._I

    def values(self) -> dict[str, complex]:
        return {'I' : self.I}

class Resistor(schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, R: float, name: str, *args, show_name: bool = True, show_value: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self._R = R
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_resistance(self.R) if show_value else ''
        self.anchors['value_label'] = (0.5, 0.3)
        self.anchors['v_label'] = (0.5, -1.1)
        self.anchors['s_label'] = (0.5, 0.9)
        self.label(label, rotate=True, loc='value_label', halign='center')

    def down(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -0.6)
        self.anchors['v_label'] = (0.5, 0.3)
        self.anchors['s_label'] = (0.5, -1.2)
        return super().down()

    def left(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -0.6)
        self.anchors['v_label'] = (0.5, 0.3)
        self.anchors['s_label'] = (0.5, -1.2)
        return super().left()

    @property
    def name(self) -> str:
        return self._name

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> dict[str, float]:
        return {'R' : self._R}

    def _place_label(self, *args, **kwargs):
        delta = self.end-self.start
        if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
            if delta[1] < 0:
                kwargs.update({'rotation': 90})
        super()._place_label(*args, **kwargs)

class Conductance(schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, G: float, name: str, *args, show_name: bool = True, show_value: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self._G = G
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_conductance(self.G) if show_value else ''
        self.anchors['value_label'] = (0.5, 0.3)
        self.anchors['s_label'] = (1.8, 1.1)
        self.label(label, rotate=True, loc='value_label', halign='center')

    def down(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -0.9)
        return super().down()

    def left(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -1)
        return super().left()

    @property
    def name(self) -> str:
        return self._name

    @property
    def R(self) -> float:
        return 1/self._G

    @property
    def G(self) -> float:
        return self._G

    def values(self) -> dict[str, float]:
        return {'G' : self._R}

    def _place_label(self, *args, **kwargs):
        delta = self.end-self.start
        if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
            if delta[1] < 0:
                kwargs.update({'rotation': 90})

        super()._place_label(*args, **kwargs)

class ACVoltageSource(din_elements.SourceUDIN):
    def __init__(self, V: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, precision=3, label_offset: float = 0.2, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._V = V
        if reverse:
            self._V *= -1
        self._name = name
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        label = dsp.print_sinosoidal(self._V, unit='V', precision=precision, w=w, deg=deg)
        self.anchors['value_label'] = (0.5, 1.1)
        self.anchors['s_label'] = (0.5, 0.9)
        self.label(f'{self._name}={label}', rotate=True, color=dsp.blue, loc='value_label', halign='center', valign='center')

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=dsp.blue))

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

    @property
    def name(self) -> str:
        return self._name

    def values(self) -> dict[str, complex]:
        return {'U' : self.V}

class ACCurrentSource(din_elements.SourceIDIN):
    def __init__(self, I: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I
        if reverse:
            self._I *= -1
        self._name = name
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        label = dsp.print_sinosoidal(self._I, unit='A', precision=precision, w=w, deg=deg)
        self.anchors['I_label'] = (0.5, 1.1)
        self.label(f'{self._name}={label}', rotate=True, color=dsp.blue, loc='I_label', halign='center', valign='center')

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=dsp.blue))

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

    @property
    def name(self) -> str:
        return self._name

    def values(self) -> dict[str, complex]:
        return {'I' : self.I}

class RectVoltageSource(schemdraw.elements.Source):
    def __init__(self, V: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, precision=3, label_offset: float = 0.2, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._V = V
        if reverse:
            self._V *= -1
        self._name = name
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        self.anchors['value_label'] = (0.5, 1.1)
        self.anchors['s_label'] = (0.5, 0.9)

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment([(0.3, 0.25), (0.3, 0.1), (0.7, 0.1), (0.7, -0.05), (0.3, -0.05), (0.3, -0.2), (0.7, -0.2)]))
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=dsp.blue))

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

    @property
    def name(self) -> str:
        return self._name

    def values(self) -> dict[str, complex]:
        return {'U' : self.V}

class RectCurrentSource(schemdraw.elements.Source):
    def __init__(self, I: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, precision=3, label_offset: float = 0.2, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I
        if reverse:
            self._I *= -1
        self._name = name
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        self.anchors['I_label'] = (0.5, 1.1)

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment([(0.3, 0.25), (0.3, 0.1), (0.7, 0.1), (0.7, -0.05), (0.3, -0.05), (0.3, -0.2), (0.7, -0.2)]))
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=dsp.blue))

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

    @property
    def name(self) -> str:
        return self._name

    def values(self) -> dict[str, complex]:
        return {'I' : self.I}

class Capacitor(schemdraw.elements.twoterm.Capacitor):
    def __init__(self, C: float, name: str, *args, show_name: bool = True, show_value: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self._C = C
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_capacitance(C) if show_value else ''
        self.anchors['value_label'] = (0.0, 0.3)
        self.anchors['v_label'] = (0.0, -1.0)
        self.anchors['s_label'] = (0.0, 0.9)
        self.label(label, rotate=True, loc='value_label', halign='center')

    def down(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.0, -0.6)
        self.anchors['s_label'] = (0.0, -1.1)
        self.anchors['v_label'] = (0.0, 0.3)
        return super().down()

    def left(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.0, -0.6)
        self.anchors['s_label'] = (0.0, -1.1)
        self.anchors['v_label'] = (0.0, 0.3)
        return super().left()

    @property
    def name(self) -> str:
        return self._name

    @property
    def C(self) -> float:
        return self._C

    def values(self) -> dict[str, float]:
        return {'C' : self._C}

    def _place_label(self, *args, **kwargs):
        delta = self.end-self.start
        if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
            if delta[1] < 0:
                kwargs.update({'rotation': 90})
        super()._place_label(*args, **kwargs)

class Inductance(schemdraw.elements.twoterm.Inductor):
    def __init__(self, L: float, name: str, *args, show_name: bool = True, show_value: bool = True, label_offset: float = 0.2, **kwargs):
        super().__init__(*args, **kwargs)
        self._L = L
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_inductance(L) if show_value else ''
        self.anchors['value_label'] = (0.5, 0.3)
        self.anchors['v_label'] = (0.5, -0.8)
        self.anchors['s_label'] = (0.5, 0.9)
        self.label(label, rotate=True, loc='value_label', halign='center')

    def down(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -0.6)
        self.anchors['v_label'] = (0.5, 0.3)
        self.anchors['s_label'] = (0.5, -1.2)
        return super().down()

    def left(self) -> schemdraw.elements.Element:
        self.anchors['value_label'] = (0.5, -0.6)
        self.anchors['v_label'] = (0.5, 0.2)
        self.anchors['s_label'] = (0.5, -1.2)
        return super().left()

    @property
    def name(self) -> str:
        return self._name

    @property
    def L(self) -> float:
        return self._L

    def values(self) -> dict[str, float]:
        return {'L$' : self._L}

    def _place_label(self, *args, **kwargs):
        delta = self.end-self.start
        if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
            if delta[1] < 0:
                kwargs.update({'rotation': 90})
        super()._place_label(*args, **kwargs)

class RealCurrentSource(schemdraw.elements.Element2Term):
    def __init__(self, current_source: CurrentSource, resistor: Resistor, *args, zoom_resistor=0.7, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments += segments_of(current_source)
        transform = schemdraw.transform.Transform(theta = 0, globalshift=((1-zoom_resistor)/2,-1), localshift=(0, 0), zoom=zoom_resistor)
        self.segments += [s.xform(transform) for s in segments_of(resistor)]
        left_line = schemdraw.Segment([(-1, 0), (-1, -1), ((1-zoom_resistor)/2, -1)])
        right_line = schemdraw.Segment([(2, 0), (2, -1), ((1+zoom_resistor)/2, -1)])
        self.segments += [left_line, right_line]
        self.anchors.update(current_source.anchors)
        self.anchors.update({k:(v[0]+0, v[1]-2.2) for k, v in resistor.anchors.items()})
        self._userlabels += current_source._userlabels
        self._userlabels += resistor._userlabels
        self._name = current_source.name
        self._I = current_source.I
        self._R = resistor.R

    @property
    def name(self) -> str:
        return self._name

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

class RealVoltageSource(schemdraw.elements.Element2Term):
    def __init__(self, voltage_source: VoltageSource, resistor: Resistor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(schemdraw.segments.Segment([(0, 0), (0, 0), schemdraw.elements.elements.gap, (4, 0), (4, 0)]))
        self.segments.extend(segments_of(voltage_source))
        self.segments.append(schemdraw.segments.Segment([(1, 0), (3, 0)]))
        transform = schemdraw.transform.Transform(theta = 0, globalshift=(3, 0))
        self.segments.extend([s.xform(transform) for s in segments_of(resistor)])
        self.anchors.update(voltage_source.anchors)
        self.anchors.update({k:(v[0]+3, v[1]) for k, v in resistor.anchors.items()})
        self._userlabels += voltage_source._userlabels
        self._userlabels += resistor._userlabels
        self._name = voltage_source.name
        self._V = voltage_source.V
        self._R = resistor.R

    @property
    def name(self) -> str:
        return self._name

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

class Node(schemdraw.elements.Element):
    def __init__(self, id: str = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_id = id
        self.params['theta'] = 0
        self.params['drop'] = (0, 0)
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)
        self.anchors['NE'] = (0.5, 0.1)
        self.anchors['NW'] = (-0.5, 0.1)
        self.anchors['SE'] = (0.5, -0.3)
        self.anchors['SW'] = (-0.5, -0.3)

    @property
    def name(self) -> str:
        return f'Node {self.node_id}'

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

class LabelNode(Node):
    def __init__(self, id : str = '', id_loc : str | dict[str, str] = '', *args, show=True, **kwargs):
        super().__init__(id, *args, **kwargs)
        locations = {
            'W': {'loc': 'left', 'halign': 'right', 'valign': 'center'},
            'N': {'loc': 'top', 'halign': 'center', 'valign': 'bottom'},
            'NE': {'loc': 'NE', 'halign': 'left', 'valign': 'bottom'},
            'NW': {'loc': 'NW', 'halign': 'right', 'valign': 'bottom'},
            'E': {'loc': 'right', 'halign': 'left', 'valign': 'center'},
            'S': {'loc': 'bottom', 'halign': 'center', 'valign': 'top'},
            'SW': {'loc': 'SW', 'halign': 'left', 'valign': 'top'},
            'SE': {'loc': 'SE', 'halign': 'right', 'valign': 'top'}
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
        self.label(f'{self.node_id}', **self.id_loc)

    @property
    def name(self) -> str:
        return f'Node {self.node_id}'

class Ground(Node):
    def __init__(self, id: str = '0', *args, **kwargs):
        super().__init__(id, *args, **kwargs)
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
        kwargs.update(v_label_args.get(type(at), {}))
        kwargs.update({'color': kwargs.get('color', dsp.blue)})
        kwargs.update({'headlength': kwargs.get('headlength', 0.4)})
        kwargs.update({'headwidth': kwargs.get('headwidth', 0.3)})
        # adjust counting arrow system of voltage sources for display
        if type(at) in source_elements:
            reverse = not reverse
        super().__init__(reverse=reverse, **kwargs)
        if isinstance(at, RealVoltageSource):
            self.at(at.center)
        else:
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

source_elements : list[Any] = [
        VoltageSource,
        RealVoltageSource,
        ACVoltageSource,
        CurrentSource
]

v_label_args : dict[Any, dict[str, float | str ]] = {
    VoltageSource : {'ofst' : -0.7},
    ACVoltageSource : {'ofst' : -0.7},
    CurrentSource : {'ofst' : -0.8, 'label_loc': 'top'},
    RealCurrentSource : {'ofst' : -2.1, 'label_loc': 'top'}
}

i_label_args : dict[Any, dict[str, float]] = {
    Resistor : {'ofst' : 1.4},
    Impedance : {'ofst' : 1.4},
    Capacitor : {'ofst' : 1.4},
    Inductance : {'ofst' : 1.4},
    VoltageSource : {'ofst' : -2.8},
    ACVoltageSource : {'ofst' : -3.8},
    RealVoltageSource: {'ofst' : -0.8}
}