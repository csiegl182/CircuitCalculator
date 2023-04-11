import schemdraw.elements
from .elements import InductorDIN, SourceIDIN2
from .elements import SourceUDIN
from .elements import SourceIDIN

STYLE_DIN = schemdraw.elements.STYLE_IEC.copy()
STYLE_DIN.update({
    'Inductor': InductorDIN,
    'SourceV': SourceUDIN,
    'SourceI': SourceIDIN,
    'SourceIArrow': SourceIDIN2,
    })
