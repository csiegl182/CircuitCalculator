from schemdraw.elements import STYLE_IEC
from schemdraw.elements import STYLE_IEEE
from .DIN.style import STYLE_DIN
from schemdraw.elements import style as schemdraw_style

circuit_styles = {
    'IEC' : STYLE_IEC,
    'IEEE' : STYLE_IEEE,
    'DIN' : STYLE_DIN
}

def select(style: str = '') -> None:
    schemdraw_style(style=circuit_styles.get(style, STYLE_IEEE))
