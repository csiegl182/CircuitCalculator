import schemdraw
from .Display import red, blue, print_voltage, print_current

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
    def __init__(self, voltage_source: VoltageSource, resistor: Resistor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(voltage_source)
        self.add(resistor)
        self.anchors['start'] = voltage_source.start
        self.anchors['end'] = resistor.end
        self.drop(resistor.end)
        self._name = voltage_source.name
        self._V = voltage_source.V
        self._R = resistor.R

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