from schemdraw.elements.twoterm import ResistorIEC
from schemdraw.elements.sources import Source
from schemdraw.transform import Transform
from schemdraw.segments import Segment

class InductorDIN(ResistorIEC):
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments = [self.segments[0].xform(Transform(theta=0, globalshift=(0,0)), fill='black')]

class SourceUDIN(Source):
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (1, 0)]))

class SourceIDIN(Source):
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0.5, -0.5), (0.5, 0.5)]))

class SourceIDIN2(SourceIDIN):
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment((1.2, 0.2), (1.7, 0.2), arrow='>'))
