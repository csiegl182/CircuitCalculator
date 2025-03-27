import schemdraw, schemdraw.elements, schemdraw.util
from . import schemdraw_element_extension as extension

from . import Display as dsp

import numpy as np

from typing import Any
from collections import ChainMap
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
        self.elements = [e for e in self.elements if not isinstance(e, VoltageLabel) and not isinstance(e, CurrentLabel) and not isinstance(e, PowerLabel)]

    def draw(self, *args, **kwargs):
        if self.fig is not None:
            self.fig.clear()
        return super().draw(*args, **kwargs)

    def save_copy(self, fname: str, **kwargs) -> None:
        import copy
        cpy = copy.deepcopy(self)
        cpy.save(fname, **kwargs)

class SimpleCircuitElement(ABC):
    def __init__(self, *, name: str, reverse: bool = False):
        self._name = name
        self._reverse = reverse

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_reverse(self) -> bool:
        return self._reverse

    @property
    def type(self) -> str:
        ...

def simple_circuit_element(element):
    class decorated_element(element, SimpleCircuitElement):
        def __init__(self, *args, **kwargs):
            element.__init__(self, *args, **kwargs)
            SimpleCircuitElement.__init__(self, name=kwargs.get('name', ''), reverse=kwargs.get('reverse', False))
    return decorated_element

@simple_circuit_element
class Element(schemdraw.elements.Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@simple_circuit_element
@extension.source
class VoltageSource(schemdraw.elements.SourceV):
    def __init__(self, *args, name: str, V: float = float('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        try:
            V = float(V)
        except ValueError:
            V = float('nan')
        if np.isnan(V):
            show_value = False
        self._V = V if not reverse else -V
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_real(V, unit='V', precision=precision) if show_value else ''
        self.label(f'{label}', rotate=True, color=dsp.blue, loc='value_label', halign='center', valign='center')
        self.segments.append(extension.voltage_arrow())

    @property
    def V(self) -> float:
        return self._V

    @property
    def type(self) -> str:
        return 'voltage_source'

@simple_circuit_element
@extension.source
class ComplexVoltageSource(schemdraw.elements.SourceV):
    def __init__(self, *args, name: str, V: complex = complex('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        try:
            V = complex(V)
        except ValueError:
            V = complex('nan')
        if np.isnan(V):
            show_value = False
        self._V = V if not reverse else -V
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_complex(V, unit='V', precision=precision) if show_value else ''
        self.label(f'{label}', rotate=True, color=dsp.blue, loc='value_label', halign='center', valign='center')
        self.segments.append(extension.voltage_arrow())

    @property
    def V(self) -> complex:
        return self._V

    @property
    def type(self) -> str:
        return 'complex_voltage_source'

@simple_circuit_element
@extension.source
class CurrentSource(schemdraw.elements.SourceI):
    def __init__(self, *args, name: str, I: float = float('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            I = float(I)
        except ValueError:
            I = float('nan')
        if np.isnan(I):
            show_value = False
        self._I = I if not reverse else -I
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_real(I, unit='A', precision=precision) if show_value else ''
        self.label(f'{label}', loc='i_label', ofst=(0, 0.4), rotate=True, color=dsp.red)
        self.segments.append(extension.current_arrow())

    @property
    def I(self) -> float:
        return self._I

    @property
    def type(self) -> str:
        return 'current_source'

@simple_circuit_element
@extension.source
class ComplexCurrentSource(schemdraw.elements.SourceI):
    def __init__(self, *args, name: str, I: complex = complex('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            I = complex(I)
        except ValueError:
            I = complex('nan')
        if np.isnan(I):
            show_value = False
        self._I = I if not reverse else -I
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_complex(I, unit='A', precision=precision) if show_value else ''
        self.label(f'{label}', loc='i_label', ofst=(0, 0.4), rotate=True, color=dsp.red)
        self.segments.append(extension.current_arrow())

    @property
    def I(self) -> complex:
        return self._I

    @property
    def type(self) -> str:
        return 'complex_current_source'

@simple_circuit_element
@extension.resistor
class Resistor(schemdraw.elements.Resistor):
    def __init__(self, *args, name: str, R: float = float('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            R = float(R)
        except ValueError:
            R = float('nan')
        if np.isnan(R):
            show_value = False
        self._R = R
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_resistance(self.R, precision=precision) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'resistor'

@simple_circuit_element
@extension.resistor
class Conductance(schemdraw.elements.Resistor):
    def __init__(self, *args, name: str, G: float = float('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            G = float(G)
        except ValueError:
            G = float('nan')
        if np.isnan(G):
            show_value = False
        self._G = G
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_conductance(self.G, precision=precision) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def R(self) -> float:
        return 1/self._G

    @property
    def G(self) -> float:
        return self._G

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'conductance'

@simple_circuit_element
@extension.resistor
class Impedance(schemdraw.elements.Resistor):
    def __init__(self, *args, name: str, Z: complex = complex('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            Z = complex(Z)
        except ValueError:
            Z = complex('nan')
        if np.isnan(Z):
            show_value = False
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

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'impedance'

@simple_circuit_element
@extension.resistor
class Admittance(schemdraw.elements.Resistor):
    def __init__(self, *args, name: str, Y: complex = complex('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            Y = complex(Y)
        except ValueError:
            Y = complex('nan')
        if np.isnan(Y):
            show_value = False
        self._Y = Y
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_impedance(self.Z, precision=precision) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def Z(self) -> complex:
        return 1/self._Y

    @property
    def Y(self) -> complex:
        return 1/self._Y

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'admittance'

@simple_circuit_element
@extension.source
class ACVoltageSource(schemdraw.elements.SourceSin):
    def __init__(self, V: float, w: float, phi: float, name: str, *args, show_name: bool = True, show_value: bool = True, sin=False, deg=False, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        self._V = V if not reverse else -V
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        if self._sin:
            self._phi -= np.pi/2
        self.segments.append(extension.voltage_arrow())
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_sinosoidal(V*np.exp(1j*self._phi), unit='V', precision=precision, w=w, deg=deg) if show_value else ''
        self.label(label, rotate=True, color=dsp.blue, loc='value_label', halign='center')

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
    def type(self) -> str:
        return 'ac_voltage_source'

@simple_circuit_element
@extension.source
class ACCurrentSource(schemdraw.elements.SourceSin):
    def __init__(self, *args, I: float, w: float, phi: float, name: str, show_name: bool = True, show_value: bool = True, sin=False, deg=False, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I if not reverse else -I
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        if self._sin:
            self._phi -= np.pi/2
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_sinosoidal(I*np.exp((1j*self._phi)), unit='A', precision=precision, w=w, deg=deg) if show_value else ''
        self.label(label, loc='i_label', ofst=(0, 0.4), rotate=True, color=dsp.red)
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

    @property
    def type(self) -> str:
        return 'ac_current_source'

@extension.source
@simple_circuit_element
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

    @property
    def type(self) -> str:
        return 'rect_voltage_source'

@simple_circuit_element
@extension.source
class TriangleVoltageSource(schemdraw.elements.SourceTriangle):
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

    @property
    def type(self) -> str:
        return 'tri_voltage_source'

@simple_circuit_element
@extension.source
class SawtoothVoltageSource(schemdraw.elements.Source):
    def __init__(self, V: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, **kwargs):
        super().__init__(*args, reverse=not reverse, **kwargs)
        self._V = V if not reverse else -V
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        self.segments.append(schemdraw.segments.Segment([(0.3, 0.2), (0.7, 0), (0.3, 0), (0.7, -0.2), (0.3, -0.2)]))
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

    @property
    def type(self) -> str:
        return 'saw_voltage_source'

@simple_circuit_element
@extension.source
class RectCurrentSource(schemdraw.elements.SourceSquare):
    def __init__(self, I: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
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

    @property
    def type(self) -> str:
        return 'rect_current_source'

@simple_circuit_element
@extension.source
class TriangleCurrentSource(schemdraw.elements.SourceTriangle):
    def __init__(self, I: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
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

    @property
    def type(self) -> str:
        return 'tri_current_source'

@simple_circuit_element
@extension.source
class SawtoothCurrentSource(schemdraw.elements.Source):
    def __init__(self, I: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._I = I if not reverse else -I
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        self.segments.append(schemdraw.segments.Segment([(0.3, 0.2), (0.7, 0), (0.3, 0), (0.7, -0.2), (0.3, -0.2)]))
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

    @property
    def type(self) -> str:
        return 'saw_current_source'

@simple_circuit_element
@extension.capacitor
class Capacitor(schemdraw.elements.Capacitor):
    def __init__(self, *args, name: str, C: float = float('nan'), show_name: bool = True, show_value: bool = True, reverse: bool = False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            C = float(C)
        except ValueError:
            C = float('nan')
        if np.isnan(C):
            show_value = False
        self._C = C
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_capacitance(C) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def C(self) -> float:
        return self._C

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'capacitor'

@simple_circuit_element
@extension.inductor
class Inductance(schemdraw.elements.Inductor):
    def __init__(self, *args, name: str, L: float = float('nan'), show_name: bool = True, show_value: bool = True, label_offset: float = 0.2, reverse: bool = False, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        try:
            L = float(L)
        except ValueError:
            L = float('nan')
        if np.isnan(L):
            show_value = False
        self._L = L
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_inductance(L) if show_value else ''
        self.label(label, rotate=True, loc='value_label', halign='center')

    @property
    def L(self) -> float:
        return self._L

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'inductance'

@extension.linear_current_source
@simple_circuit_element
class RealCurrentSource(schemdraw.elements.compound.ElementCompound):
    def __init__(self, name: str, I: float, R: float, *args, **kwargs):
        self._I = I
        self._R = R
        self._name = name
        super().__init__(*args, **kwargs)

    def setup(self):
        zoom_resistor = 0.7
        cs = CurrentSource(I=self._I, name=self._name, d='r')
        res = Resistor(R=self._R, name='R', l=zoom_resistor, d='r')
        transform = schemdraw.transform.Transform(theta = 0, globalshift=(((-3-zoom_resistor)/2,-1.5)), localshift=(0, 0), zoom=zoom_resistor)
        res.segments = [s.xform(transform) for s in res.segments]
        res.anchors['value_label'] = (-1.5, -2.5)
        self.add(cs)
        self.add(res)
        self.add(l_up:=schemdraw.elements.Line(d='r', l=1).at(res.end))
        self.add(l_down:=schemdraw.elements.Line(d='l', l=1).at(res.start))
        self.add(schemdraw.elements.Line(d='u', l=1.5).at(l_up.end))
        self.add(schemdraw.elements.Line(d='u', l=1.5).at(l_down.end))

    @property
    def I(self) -> complex:
        return self._I

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    @property
    def type(self) -> str:
        return 'real_current_source'

@extension.linear_voltage_source
@simple_circuit_element
class RealVoltageSource(schemdraw.elements.compound.ElementCompound):
    def __init__(self, name: str, V: float, R: float, *args, **kwargs):
        self._V = V
        self._R = R
        self._name = name
        super().__init__(*args, **kwargs)

    def setup(self):
        zoom_resistor = 1 
        vs = VoltageSource(V=self._V, name=self._name, d='l')
        res = Resistor(R=self._R, name='R', l=zoom_resistor, d='l')
        transform_resistor = schemdraw.transform.Transform(theta = 0, globalshift=(0, 0), zoom=zoom_resistor)
        res.segments = [s.xform(transform_resistor) for s in res.segments]
        res.anchors['value_label'] = (0.5, -0.8)
        self.add(L:=schemdraw.elements.Line(d='l', l=1))
        self.add(res.at(L.end))
        self.add(vs)

    @property
    def V(self) -> complex:
        return self._V

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    @property
    def type(self) -> str:
        return 'real_voltage_source'

@simple_circuit_element
class Line(schemdraw.elements.lines.Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return ''

    @property
    def type(self) -> str:
        return 'line'

@simple_circuit_element
@extension.lamp
class Lamp(schemdraw.elements.Lamp2):
    def __init__(self, V_ref: float, P_ref: float, name: str, *args, show_name: bool = True, show_value: bool = True, reverse: bool = False, precision: int = 3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        self._V_ref = V_ref
        self._P_ref = P_ref
        label = ''
        label += f'{name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += dsp.print_real(P_ref, unit='W', precision=precision) if show_value else ''
        self.label(label, rotate=show_value, loc='value_label', halign='center', valign='center')

    @property
    def V_ref(self) -> float:
        return self._V_ref

    @property
    def P_ref(self) -> float:
        return self._P_ref

    @property
    def R(self) -> float:
        return self._V_ref**2/self._P_ref

    @property
    def is_reverse(self) -> bool:
        return False

class LabeledLine(Line):
    def __init__(self, *args, name: str, **kwargs):
        super().__init__(*args, name=name, **kwargs)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return 'labeled_line'

    @property
    def is_reverse(self) -> bool:
        return False

@simple_circuit_element
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

    @property
    def type(self) -> str:
        return 'node'

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

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'label_node'

@simple_circuit_element
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

    @property
    def is_reverse(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return 'switch'

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
    def __init__(self, *args, name: str = '0', **kwargs):
        super().__init__(*args, name=name, **kwargs)
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
    def type(self) -> str:
        return 'ground'

    def up(self, _: float) -> schemdraw.elements.Element:
        return super().left()

    def down(self, _: float) -> schemdraw.elements.Element:
        return super().right()

    def left(self, _: float) -> schemdraw.elements.Element:
        return super().down()

    def right(self, _: float) -> schemdraw.elements.Element:
        return super().up()

class VoltageLabel(schemdraw.elements.CurrentLabel):
    def __init__(self, at: schemdraw.elements.Element, vlabel: str = '', label_loc: str = 'bottom', reverse: bool = False, color: str | tuple[float, float, float] = dsp.blue, **kwargs):
        self.params = ChainMap({'headwidth': 0.3, 'headlength': 0.4, 'color': color}, self.params)
        if isinstance(at, RealVoltageSource):
            kwargs.update({'length': kwargs.get('length', 4)})
        super().__init__(reverse=reverse, **kwargs)
        try:
            self.at(at.v_label)
            self.theta(at.transform.theta)
        except AttributeError:
            self.at(at.center)
        rotate = kwargs.get('rotate', True)
        if rotate == True and at.transform.theta == 270:
            rotate = 90
        self.label(vlabel, rotate=rotate, loc=label_loc, ofst=(0, -0.1))

class CurrentLabel(schemdraw.elements.CurrentLabelInline):
    def __init__(self, at: schemdraw.elements.Element, ilabel: str = '', **kwargs):
        kwargs.update(i_label_args.get(type(at), {}))
        kwargs.update({'color': kwargs.get('color', dsp.red)})
        kwargs.update({'headlength': kwargs.get('headlength', 0.4)})
        kwargs.update({'headwidth': kwargs.get('headwidth', 0.3)})
        totlen = at.params.get('l', at.params.get('unit', 7))
        kwargs.update({'ofst': totlen/4-kwargs['headlength']/2})
        start = kwargs.get('start', True)
        reverse = kwargs.get('reverse', False)
        if isinstance(at, RealVoltageSource) or isinstance(at, RealCurrentSource): # when replacing CurrentLabelInline this dependency may be removed
            reverse = not reverse
        kwargs.update({'start' : start, 'reverse' : reverse})
        super().__init__(**kwargs)
        self.at(at)
        self.label(ilabel)

class PowerLabel(schemdraw.elements.Label):
    def __init__(self, at: schemdraw.elements.Element, plabel: str = '', offset: float = 0, **kwargs):
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
        self.label(plabel, rotate=rotate, halign='center', ofst=(0, offset))

i_label_args : dict[Any, dict[str, float]] = {
    Resistor : {'ofst' : 0},
    Conductance : {'ofst' : 1.4},
    Impedance : {'ofst' : 1.4},
    Admittance : {'ofst' : 1.4},
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