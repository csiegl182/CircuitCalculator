import schemdraw
from .Display import red, blue, print_voltage, print_current
from abc import ABC

class CircuitElement(ABC):
    pass

class VoltageSource(CircuitElement, schemdraw.elements.sources.SourceV):
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

class RealVoltageSource(CircuitElement, schemdraw.elements.sources.SourceV):
    def __init__(self, V: float, R: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._V = -V
        else:
            self._V = V
        self._R = R
        self._name = name
        self.label(f'{self._name} {print_voltage(V, precision=precision)}V / {R}$\\Omega$')

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
        return {'U' : self.V, 'R' : self.R}

class CurrentSource(CircuitElement, schemdraw.elements.sources.SourceI):
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
        schemdraw.segments.Segment([(0.5, -0.5), (0.5, 0.5)])
    ]

class RealCurrentSource(CircuitElement, schemdraw.elements.sources.SourceI):
    def __init__(self, I: float, R: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._I = -I
        else:
            self._I = I
        self._R = R
        self._name = name
        self.segments = DrawRealCurrentSource()

        a, b = (1, -0.3), (1.5, -0.3)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.2, arrowlength=.3, color=red))
        self.label(f'{self._name}={print_current(I, precision=precision)}A', rotate=True, ofst=(0, -2.1))
        self.label(f'{print_current(R, precision=precision)}$\\Omega$', rotate=True, ofst=(0, .2))

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

class Resistor(CircuitElement, schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._R = R
        self._name = name
        self.label(f'{self._name}={self._R}$\\Omega$', rotate=True)

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

class Line(CircuitElement, schemdraw.elements.lines.Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return ''

class Node(CircuitElement, schemdraw.elements.Element):
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
    def __init__(self, id : str = '', id_loc : str = '', *args, **kwargs):
        super().__init__(id, *args, **kwargs)
        self.segments.append(schemdraw.SegmentCircle([0, 0], 0.12, fill='black'))
        if id_loc != '':
            if id_loc == 'W':
                label_param = {'loc': 'left', 'align': ['right', 'center']}
            elif id_loc == 'N':
                label_param = {'loc': 'top', 'align': ['center', 'bottom']}
            elif id_loc == 'E':
                label_param = {'loc': 'right', 'align': ['left', 'center']}
            else: # id_loc == 'S'
                label_param = {'loc': 'bottom', 'align': ['center', 'top']}
            self.bbox = self.get_bbox(includetext=False)
            self.add_label(f'{self.node_id}', **label_param)

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
        

class CircuitLabel(ABC):
    ...

class CurrentLabel(CircuitLabel, schemdraw.elements.CurrentLabelInline):
    pass

class VoltageLabel(CircuitLabel, schemdraw.elements.CurrentLabel):
    pass