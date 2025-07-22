import schemdraw, schemdraw.elements
from . import Display as dsp
from typing import Type, Optional

def resistor(element: Type[schemdraw.elements.Element2Term]) -> Type[schemdraw.elements.Element2Term]:
    class extended_resistor(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, 0.3)
            self.anchors['v_label'] = (0.5, -1.1)
            self.anchors['s_label'] = (0.5, 0.9)

        def down(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, -0.6)
            self.anchors['v_label'] = (0.5, 0.3)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().down(length=length)

        def up(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, 0.4)
            self.anchors['v_label'] = (0.5, -1.1)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().up(length=length)

        def left(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, -0.9)
            self.anchors['v_label'] = (0.5, 0.3)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().left(length=length)

        def _place_label(self, label: schemdraw.elements.elements.Label, theta: float = 0):
            delta = self.end-self.start
            if abs(delta[1]) > abs(delta[0]): # portrait placing
                if delta[1] < 0:
                    theta = 90
            super()._place_label(label=label, theta=theta)
    
    return extended_resistor

def source(element: Type[schemdraw.elements.Element2Term]) -> Type[schemdraw.elements.Element2Term]:
    class extended_source(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, 1.1)
            self.anchors['v_label'] = (0.5, -1.1)
            self.anchors['i_label'] = (1.2, 0.3)
            self.anchors['s_label'] = (0.5, 1.5)

        def down(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['s_label'] = (0.5, -0.7)
            return super().down(length=length)
    return extended_source

def capacitor(element: Type[schemdraw.elements.Element2Term]) -> Type[schemdraw.elements.Element2Term]:
    class extended_capacitor(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.0, 0.3)
            self.anchors['v_label'] = (0.0, -1.0)
            self.anchors['s_label'] = (0.0, 0.9)

        def down(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.0, -0.6)
            self.anchors['s_label'] = (0.0, -1.1)
            self.anchors['v_label'] = (0.0, 0.3)
            return super().down(length=length)

        def left(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.0, -0.6)
            self.anchors['s_label'] = (0.0, -1.1)
            self.anchors['v_label'] = (0.0, 0.3)
            return super().left(length=length)

        def _place_label(self, label: schemdraw.elements.elements.Label, theta: float = 0):
            delta = self.end-self.start
            if abs(delta[1]) > abs(delta[0]): # portrait placing
                if delta[1] < 0:
                    theta = 90
            super()._place_label(label, theta)
    return extended_capacitor

def inductor(element: Type[schemdraw.elements.Element2Term]) -> Type[schemdraw.elements.Element2Term]:
    class extended_inductor(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, 0.3)
            self.anchors['v_label'] = (0.5, -0.8)
            self.anchors['s_label'] = (0.5, 0.9)

        def down(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, -0.6)
            self.anchors['v_label'] = (0.5, 0.3)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().down(length=length)

        def left(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, -0.6)
            self.anchors['v_label'] = (0.5, 0.2)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().left(length=length)

        def _place_label(self, label: schemdraw.elements.elements.Label, theta: float = 0):
            delta = self.end-self.start
            if abs(delta[1]) > abs(delta[0]): # portrait placing
                if delta[1] < 0:
                    theta = 90
            super()._place_label(label, theta)
    return extended_inductor

def linear_current_source(element: Type[schemdraw.elements.Element2Term]) -> Type[schemdraw.elements.Element2Term]:
    class extended_linear_source(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, -1.2)
            self.anchors['start'] = (0, 0)
            self.anchors['center'] = (0, 1.5)
            self.anchors['end'] = (3, 0)

        def up(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, -0.6)
            self.anchors['v_label'] = (1.5, -2.5)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().up()

    return extended_linear_source

def linear_voltage_source(element: Type[schemdraw.elements.Element2Term]) -> Type[schemdraw.elements.Element2Term]:
    class extended_linear_source(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['v_label'] = (2, -1.5)
            self.anchors['start'] = (-5, 0)
            self.anchors['center'] = (0, 1.5)
            self.anchors['end'] = (0, 0)

        def up(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['v_label'] = (-1.5, -2.5)
            return super().up()

    return extended_linear_source

def lamp(element: Type[schemdraw.elements.Element2Term]) -> Type[schemdraw.elements.Element2Term]:
    class extended_lamp(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, 0.8)
            self.anchors['v_label'] = (0.5, -1.1)
            self.anchors['i_label'] = (1.2, 0.3)
            self.anchors['s_label'] = (0.5, 1.5)

        def down(self, length: Optional[float] = None) -> schemdraw.elements.Element:
            self.anchors['s_label'] = (0.5, -0.7)
            return super().down(length=length)

    return extended_lamp

def voltage_arrow(start: tuple[float, float] = (1.5, 0.7), end: tuple[float, float] = (-0.5, 0.7), arrowwidth: float = 0.3, arrowlength: float = 0.4, color=dsp.blue) -> schemdraw.Segment:
    return schemdraw.Segment((start, end), arrow='->', arrowwidth=arrowwidth, arrowlength=arrowlength, color=color)

def current_arrow(start: tuple[float, float] = (1.2, 0.3), end: tuple[float, float] = (1.8, 0.3), arrowwidth: float = 0.3, arrowlength: float = 0.4, color=dsp.red) -> schemdraw.Segment:
    return schemdraw.Segment((start, end), arrow='->', arrowwidth=arrowwidth, arrowlength=arrowlength, color=color)
