import schemdraw
import schemdraw.elements
from .Display import red, blue, print_voltage, print_current
from typing import Any
from ..Utils import ScientificFloat, ScientificComplex

def segments_of(element: schemdraw.elements.Element) -> list[schemdraw.segments.SegmentType]:
    return element.segments

class Schematic(schemdraw.Drawing):
    def __init__(self, unit=7, **kwargs):
        super().__init__(unit=unit, **kwargs)

    def save_copy(self, fname: str, **kwargs) -> None:
        import copy
        cpy = copy.deepcopy(self)
        cpy.save(fname, **kwargs)

class VoltageSource(schemdraw.elements.sources.Source):
    def __init__(self, V: complex, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._V = -V
        else:
            self._V = V
        self._name = name
        self.anchors['V_label'] = (0.5, 1.1)
        self.label(f'{self._name}={print_voltage(V, precision=precision)}', rotate=True, color=blue, loc='V_label', halign='center', valign='center')
        self.segments.append(schemdraw.segments.Segment([(0, 0), (1, 0)]))

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=blue))

    @property
    def name(self) -> str:
        return self._name

    @property
    def V(self) -> complex:
        return self._V

    def values(self) -> dict[str, complex]:
        return {'U' : self.V}

class ACVoltageSource(VoltageSource):
    def __init__(self, V: float, w: float, phi: float, name: str, *args, sin=False, deg=False, reverse=False, precision=3, label_offset: float = 0.2, **kwargs):
        super().__init__(V, name, *args, reverse=reverse, precision=precision, **kwargs)
        self._w = w
        self._phi = phi
        self._deg = deg
        self._sin = sin
        label = '$' + f'{self._V:4.2f}' + '\\mathrm{V}\\cdot\\cos(' + f'{self._w:4.2g}' + '\\cdot t + ' + f'{self._phi:4.2f}' + ')$'
        self.label(label, rotate=True, ofst=label_offset)

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

class CurrentSource(schemdraw.elements.sources.SourceI):
    def __init__(self, I: complex, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._I = -I
        else:
            self._I = I
        self._name = name
        self.segments = DrawCurrentSource()
        a, b = (1.2, 0.3), (1.8, 0.3)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=red))
        self.anchors['I_label'] = a
        self.label(f'{self._name}={print_current(self._I)}', loc='I_label', ofst=(0, 0.4), rotate=True, color=red)

    @property
    def name(self) -> str:
        return self._name

    @property
    def I(self) -> complex:
        return self._I

    def values(self) -> dict[str, complex]:
        return {'I' : self.I}

def DrawSource() -> list[schemdraw.segments.SegmentType]:
    return [
        schemdraw.segments.Segment([(0, 0), (0, 0), schemdraw.elements.elements.gap, (1, 0), (1, 0)]),
        schemdraw.segments.SegmentCircle((0.5, 0), 0.5,)
    ]

def DrawCurrentSource() -> list[schemdraw.segments.SegmentType]:
    return DrawSource() + [
        schemdraw.segments.Segment([(0.5, -0.5), (0.5, 0.5)])
    ]

def DrawRealCurrentSource() -> list[schemdraw.segments.SegmentType]:
    return DrawCurrentSource() + [
        schemdraw.segments.SegmentCircle((-0.5, 0), 0.07, fill='black'),
        schemdraw.segments.SegmentCircle((1.5, 0), 0.07, fill='black'),
        schemdraw.segments.Segment([(-0.5, 0), (-0.5, 1)]),
        schemdraw.segments.Segment([(1.5, 0), (1.5, 1)]),
        schemdraw.segments.Segment([(-0.5, 1), (0, 1)]),
        schemdraw.segments.Segment([(1, 1), (1.5, 1)]),
        schemdraw.segments.Segment([(0, 0.8), (1, 0.8), (1, 1.2), (0, 1.2), (0, 0.8)])
    ]

def DrawVoltageSource() -> list[schemdraw.segments.SegmentType]:
    return DrawSource() + [
        schemdraw.segments.Segment([(0, 0), (1, 0)])
    ]

class Impedance(schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, Z: complex, name: str, *args, show_name: bool = True, show_value: bool = True, precision: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self._Z = Z
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += str(ScientificComplex(value=self.Z, unit='$\\Omega$', use_exp_prefix=True, precision=precision)) if show_value else ''
        self.anchors['Z_label'] = (0.5, 0.3)
        self.label(label, rotate=True, loc='Z_label', halign='center')

    def down(self) -> schemdraw.elements.Element:
        self.anchors['Z_label'] = (0.5, -0.9)
        return super().down()

    def left(self) -> schemdraw.elements.Element:
        self.anchors['Z_label'] = (0.5, -1)
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

class Resistor(schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, R: float, name: str, *args, show_name: bool = True, show_value: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self._R = R
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += str(ScientificFloat(value=self.R, unit='$\\Omega$', use_exp_prefix=True)) if show_value else ''
        self.anchors['R_label'] = (0.5, 0.3)
        self.label(label, rotate=True, loc='R_label', halign='center')

    def down(self) -> schemdraw.elements.Element:
        self.anchors['R_label'] = (0.5, -0.9)
        return super().down()

    def left(self) -> schemdraw.elements.Element:
        self.anchors['R_label'] = (0.5, -1)
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

class Capacitor(schemdraw.elements.twoterm.Capacitor):
    def __init__(self, C: float, name: str, *args, show_name: bool = True, show_value: bool = True, label_offset: float = 0.2, **kwargs):
        super().__init__(*args, **kwargs)
        self._C = C
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += str(ScientificFloat(value=self.C, unit='$\\mathrm{F}$', use_exp_prefix=True)) if show_value else ''
        self.label(label, rotate=True, ofst=label_offset)

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
        label += str(ScientificFloat(value=self.L, unit='$\\mathrm{H}$', use_exp_prefix=True)) if show_value else ''
        self.label(label, rotate=True, ofst=label_offset)

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

class LabelNode(Node):
    def __init__(self, id : str = '', id_loc : str | dict[str, Any] = '', *args, show=True, **kwargs):
        super().__init__(id, *args, **kwargs)
        locations = {
            'W': {'loc': 'left', 'align': ['right', 'center']},
            'N': {'loc': 'top', 'align': ['center', 'bottom']},
            'NE': {'loc': 'NE', 'align': ['left', 'bottom']},
            'NW': {'loc': 'NW', 'align': ['right', 'bottom']},
            'E': {'loc': 'right', 'align': ['left', 'center']},
            'S': {'loc': 'bottom', 'align': ['center', 'top']},
            'SW': {'loc': 'SW', 'align': ['left', 'top']},
            'SE': {'loc': 'SE', 'align': ['right', 'top']}
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
        self.add_label(f'{self.node_id}', **self.id_loc)

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

class VoltageLabel(schemdraw.elements.CurrentLabel):
    def __init__(self, at: schemdraw.elements.Element, label: str = '', label_loc: str = 'bottom', **kwargs):
        kwargs['color'] = kwargs.get('color', blue)
        super().__init__(**kwargs)
        if isinstance(at, RealVoltageSource):
            self.at(at.center)
        else:
            try:
                self.at(at.v_label)
                self.theta(at.transform.theta)
            except AttributeError:
                self.at(at)
        self.label(label, rotate=kwargs.get('rotate', True), loc=label_loc, ofst=(0, -0.1))

class CurrentLabel(schemdraw.elements.CurrentLabelInline):
    def __init__(self, at: schemdraw.elements.Element, label: str = '', **kwargs):
        kwargs['color'] = kwargs.get('color', red)
        totlen = at._userparams.get('l', at._userparams.get('unit', 3))
        kwargs['ofst'] = totlen/4-0.15+kwargs.get('ofst', 0)
        start = kwargs.get('start', True)
        reverse = kwargs.get('reverse', False)
        kwargs.update({'start' : start, 'reverse' : reverse})
        super().__init__(**kwargs)
        self.at(at)
        self.label(label)

    @property
    def name(self) -> str:
        return ''

v_label_args : dict[Any, dict[str, Any]]= {
    Resistor : {'ofst' : -0.6},
    Impedance : {'ofst' : -0.6},
    CurrentSource : {'ofst' : 1.5, 'label_loc': 'top'},
    RealCurrentSource : {'ofst' : 1.5, 'label_loc': 'top'}
}

i_label_args : dict[Any, dict[str, Any]]= {
    Resistor : {'ofst' : 1.4},
    Impedance : {'ofst' : 1.4},
    VoltageSource : {'ofst' : -2.8},
    RealVoltageSource: {'ofst' : -0.8}
}