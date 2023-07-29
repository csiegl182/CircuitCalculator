import schemdraw, schemdraw.elements
from . import Display as dsp
from typing import Type

def resistor(element: Type[schemdraw.elements.Element]) -> Type[schemdraw.elements.Element]:
    class extended_resistor(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, 0.3)
            self.anchors['v_label'] = (0.5, -1.1)
            self.anchors['s_label'] = (0.5, 0.9)

        def down(self) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, -0.6)
            self.anchors['v_label'] = (0.5, 0.3)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().down()

        def up(self) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, 0.4)
            self.anchors['v_label'] = (0.5, -1.1)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().up()

        def left(self) -> schemdraw.elements.Element:
            self.anchors['value_label'] = (0.5, -0.9)
            self.anchors['v_label'] = (0.5, 0.3)
            self.anchors['s_label'] = (0.5, -1.2)
            return super().left()

        def _place_label(self, *args, **kwargs):
            delta = self.end-self.start
            if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
                if delta[1] < 0:
                    kwargs.update({'rotation': 90})
            super()._place_label(*args, **kwargs)
    
    return extended_resistor

def source(element: Type[schemdraw.elements.Element]) -> Type[schemdraw.elements.Element]:
    class extended_source(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, 1.1)
            self.anchors['v_label'] = (0.5, -1.1)
            self.anchors['i_label'] = (1.2, 0.3)
            self.anchors['s_label'] = (0.5, 1.5)

        def down(self) -> schemdraw.elements.Element:
            self.anchors['s_label'] = (0.5, -0.7)
            return super().down()
    return extended_source

def capacitor(element: Type[schemdraw.elements.Element]) -> Type[schemdraw.elements.Element]:
    class extended_inductor(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.0, 0.3)
            self.anchors['v_label'] = (0.0, -1.0)
            self.anchors['s_label'] = (0.0, 0.9)

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

        def _place_label(self, *args, **kwargs):
            delta = self.end-self.start
            if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
                if delta[1] < 0:
                    kwargs.update({'rotation': 90})
            super()._place_label(*args, **kwargs)

    return extended_inductor

def inductor(element: Type[schemdraw.elements.Element]) -> Type[schemdraw.elements.Element]:
    class extended_inductor(element):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.anchors['value_label'] = (0.5, 0.3)
            self.anchors['v_label'] = (0.5, -0.8)
            self.anchors['s_label'] = (0.5, 0.9)

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

        def _place_label(self, *args, **kwargs):
            delta = self.end-self.start
            if abs(delta[1]) > abs(delta[0]): # portrait placing of resistor
                if delta[1] < 0:
                    kwargs.update({'rotation': 90})
            super()._place_label(*args, **kwargs)

    return extended_inductor

def voltage_arrow(start: tuple[float, float] = (1.5, 0.7), end: tuple[float, float] = (-0.5, 0.7), arrowwidth: float = 0.3, arrowlength: float = 0.4, color=dsp.blue) -> schemdraw.Segment:
    return schemdraw.Segment((start, end), arrow='->', arrowwidth=arrowwidth, arrowlength=arrowlength, color=color)

def current_arrow(start: tuple[float, float] = (1.2, 0.3), end: tuple[float, float] = (1.8, 0.3), arrowwidth: float = 0.3, arrowlength: float = 0.4, color=dsp.red) -> schemdraw.Segment:
    return schemdraw.Segment((start, end), arrow='->', arrowwidth=arrowwidth, arrowlength=arrowlength, color=color)
