import schemdraw
from .Display import red, blue, print_voltage, print_current
from typing import Any

class Schematic(schemdraw.Drawing):
    pass

class VoltageSource(schemdraw.elements.sources.SourceV):
    def __init__(self, V: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._V = -V
        else:
            self._V = V
        self._name = name
        self.label(f'{self._name}={print_voltage(V, precision=precision)}V', rotate=True)
        self.segments = DrawVoltageSource()

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=blue))

    @property
    def name(self) -> str:
        return self._name

    @property
    def V(self) -> float:
        return self._V

    def values(self) -> dict[str, float]:
        return {'U' : self.V}

class CurrentSource(schemdraw.elements.sources.SourceI):
    def __init__(self, I: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._I = -I
        else:
            self._I = I
        self._name = name
        self.label(f'{self._name}={print_current(I, precision=precision)}A', rotate=True)
        self.segments = DrawCurrentSource()

        a, b = (1.2, -0.3), (1.8, -0.3)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=red))

    @property
    def name(self) -> str:
        return self._name

    @property
    def I(self) -> float:
        return self._I

    def values(self) -> dict[str, float]:
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

class Resistor(schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, R: float, name: str, *args, show_name: bool = True, show_value: bool = True, label_offset: float = 0.2, **kwargs):
        super().__init__(*args, **kwargs)
        self._R = R
        self._name = name
        label = ''
        label += f'{self._name}' if show_name else ''
        label += '=' if  show_name and show_value else ''
        label += f'{self.R}$\\Omega$' if show_value else ''
        self.label(label, rotate=True, ofst=label_offset)

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

class RealCurrentSource(schemdraw.elements.compound.ElementCompound):
    def __init__(self, current_source: CurrentSource, resistor: Resistor, *args, d:str = 'up', **kwargs):
        super().__init__(*args, **kwargs)
        if d == 'left':
            self.add(current_source.left())
            self.add(Line('up'))
            self.add(resistor.right())
            self.add(Line('down'))
        elif d == 'down':
            self.add(current_source.down())
            self.add(Line('right'))
            self.add(resistor.up())
            self.add(Line('left'))
        elif d == 'right':
            self.add(current_source.right())
            self.add(Line('up'))
            self.add(resistor.left())
            self.add(Line('down'))
        else:
            self.add(current_source)
            self.add(Line('right'))
            self.add(resistor.down())
            self.add(Line('left'))
        self.anchors['start'] = current_source.start
        self.anchors['end'] = current_source.end
        self.drop(current_source.end)
        self._name = current_source.name
        self._I = current_source.I
        self._R = resistor.R

    @property
    def name(self) -> str:
        return self._name

    @property
    def I(self) -> float:
        return self._I

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> dict[str, float]:
        return {'I' : self.I, 'R' : self.R}

class RealVoltageSource(schemdraw.elements.compound.ElementCompound):
    def __init__(self, voltage_source: VoltageSource, resistor: Resistor, *args, reverse=False, **kwargs):
        super().__init__(*args, d='right', **kwargs)
        if reverse:
            self.add(resistor)
            self.add(voltage_source)
            start = resistor.start
            end = voltage_source.end
        else:
            self.add(voltage_source)
            self.add(resistor)
            start = voltage_source.start
            end = resistor.end
        self.anchors['start'] = start
        self.anchors['end'] = end
        self.anchors['center'] = (resistor.end-resistor.start)/2 + resistor.start
        self.drop(end)
        self._name = voltage_source.name
        self._V = voltage_source.V
        self._R = resistor.R
        self.resistor_length = resistor._userparams.get('l', resistor._userparams.get('unit', 3))
        self.resistor_d = resistor._userparams.get('d', 'right')

    @property
    def name(self) -> str:
        return self._name

    @property
    def V(self) -> float:
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

    @property
    def name(self) -> str:
        return f'Node {self.node_id}'

class LabelNode(Node):
    def __init__(self, id : str = '', id_loc : str | dict[str, Any] = '', *args, show=True, **kwargs):
        super().__init__(id, *args, **kwargs)
        if show:
            self.segments.append(schemdraw.SegmentCircle([0, 0], 0.12, fill='black'))
            if isinstance(id_loc, str):
                if id_loc == 'W':
                    loc = {'loc': 'left', 'align': ['right', 'center']}
                elif id_loc == 'N':
                    loc = {'loc': 'top', 'align': ['center', 'bottom']}
                elif id_loc == 'E':
                    loc = {'loc': 'right', 'align': ['left', 'center']}
                elif id_loc == 'S':
                    loc = {'loc': 'bottom', 'align': ['center', 'top']}
                else:
                    loc = {}
            else:
                loc = id_loc
            self.bbox = self.get_bbox(includetext=False)
            self.add_label(f'{self.node_id}', **loc)

    @property
    def name(self) -> str:
        return f'Node {self.node_id}'

class Ground(Node):
    def __init__(self, id: str = '0', *args, **kwargs):
        super().__init__(id, *args, **kwargs)
        gndgap = 0.12
        gnd_lead = 0.4
        resheight = schemdraw.elements.twoterm.resheight
        gap = schemdraw.elements.twoterm.gap
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
    def __init__(self, at: schemdraw.elements.Element, label: str = '', **kwargs):
        kwargs['top'] = kwargs.get('top', False)
        kwargs['ofst'] = kwargs.get('ofst', 0.6)
        kwargs['color'] = kwargs.get('color', blue)
        if isinstance(at, RealVoltageSource):
            kwargs['d'] = at.resistor_d
            kwargs['reverse'] = not kwargs.get('reverse', False)
        super().__init__(**kwargs)
        self.params['lblofst'] = 0.1
        if isinstance(at, RealVoltageSource):
            self.at(at.center)
        else:
            self.at(at)
        self.label(label, rotate=kwargs.get('rotate', False))

class CurrentLabel(schemdraw.elements.CurrentLabelInline):
    def __init__(self, at: schemdraw.elements.Element, label: str = '', **kwargs):
        kwargs['color'] = kwargs.get('color', red)
        totlen = at._userparams.get('l', at._userparams.get('unit', 3))
        if isinstance(at, RealVoltageSource):
            kwargs['d'] = at.resistor_d
            totlen = at.resistor_length
        kwargs['ofst'] = totlen/4-0.15+kwargs.get('ofst', 0)
        start = kwargs.get('start', True)
        reverse = kwargs.get('reverse', False)
        if not start and reverse:
            reverse = not reverse
        kwargs.update({'start' : start, 'reverse' : reverse})
        super().__init__(**kwargs)
        if isinstance(at, RealVoltageSource):
            self.at(at.center)
        else:
            self.at(at)
        self.label(label)

    @property
    def name(self) -> str:
        return ''