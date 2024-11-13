from .Elements import Schematic
from ..Circuit.dump_load import dictify_circuit
from .DiagramTranslator import circuit_translator
from . import Elements as simple_circuit_elements
import schemdraw.elements
import schemdraw.util
import schemdraw.transform
from typing import Any, TypedDict, Callable, TypeVar
from collections import ChainMap
from .. import dump_load
import functools

class SchemdrawObjectProperties(TypedDict):
    type: str
    values: dict[str, Any] | list

class SimpleCircuitObjectProperties(SchemdrawObjectProperties):
    name: str
    reverse: bool

T = TypeVar('T')

def schemdraw_object_properties(object: T, value_fcn: Callable[[T], dict[str, Any] | list]) -> SchemdrawObjectProperties:
    return SchemdrawObjectProperties(type=str(type(object).__name__), values=value_fcn(object))

def listify_point(p: schemdraw.util.Point) -> list[float]:
    return [serialize_schemdraw_element(p.x), serialize_schemdraw_element(p.y)]

def dictify_segment(s: schemdraw.segments.Segment) -> dict[str, Any]:
    return {
        'path' : serialize_schemdraw_element(s.path),
        'zorder' : serialize_schemdraw_element(s.zorder),
        'color' : serialize_schemdraw_element(s.color),
        'fill' : serialize_schemdraw_element(s.fill),
        'lw' : serialize_schemdraw_element(s.lw),
        'ls' : serialize_schemdraw_element(s.ls),
        'arrow' : serialize_schemdraw_element(s.arrow),
        'arrowwidth' : serialize_schemdraw_element(s.arrowwidth),
        'arrowlength' : serialize_schemdraw_element(s.arrowlength),
        'clip' : serialize_schemdraw_element(s.clip),
        'capstyle' : serialize_schemdraw_element(s.capstyle),
        'joinstyle' : serialize_schemdraw_element(s.joinstyle),
        'visible' : serialize_schemdraw_element(s.visible)
    }

def dictify_segment_text(s: schemdraw.segments.SegmentText) -> dict[str, Any]:
    return {
        'pos' : serialize_schemdraw_element(s.xy),
        'label' : serialize_schemdraw_element(s.text),
        'align' : serialize_schemdraw_element(s.align),
        'font' : serialize_schemdraw_element(s.font),
        'mathfont' : serialize_schemdraw_element(s.mathfont),
        'fontsize' : serialize_schemdraw_element(s.fontsize),
        'color' : serialize_schemdraw_element(s.color),
        'rotation' : serialize_schemdraw_element(s.rotation),
        'rotation_mode' : serialize_schemdraw_element(s.rotation_mode),
        'rotation_global' : serialize_schemdraw_element(s.rotation_global),
        'clip' : serialize_schemdraw_element(s.clip),
        'zorder' : serialize_schemdraw_element(s.zorder),
        'visible' : serialize_schemdraw_element(s.visible)
        }

def dictify_segment_circle(s: schemdraw.segments.SegmentCircle) -> dict[str, Any]:
    return {
        'center' : serialize_schemdraw_element(s.center),
        'radius' : serialize_schemdraw_element(s.radius),
        'color' : serialize_schemdraw_element(s.color),
        'lw' : serialize_schemdraw_element(s.lw),
        'ls' : serialize_schemdraw_element(s.ls),
        'fill' : serialize_schemdraw_element(s.fill),
        'clip' : serialize_schemdraw_element(s.clip),
        'zorder' : serialize_schemdraw_element(s.zorder),
        'ref' : serialize_schemdraw_element(s.endref),
        'visible' : serialize_schemdraw_element(s.visible)
        }

def dictify_transform(t: schemdraw.transform.Transform) -> dict[str, Any]:
    return {
        'theta' : serialize_schemdraw_element(t.theta),
        'globalshift' : serialize_schemdraw_element(t.shift),
        'localshift' : serialize_schemdraw_element(t.localshift),
        'zoom' : serialize_schemdraw_element(t.zoom)
    }

schemdraw_serializers = {
    str: lambda x: x,
    int: lambda x: x,
    float: lambda x: x,
    bool: lambda x: x,
    dict: lambda x: {k: serialize_schemdraw_element(v) for k, v in x.items()},
    list: lambda x: [serialize_schemdraw_element(e) for e in x],
    tuple: lambda x: [serialize_schemdraw_element(e) for e in x],
    ChainMap: lambda x: {k: serialize_schemdraw_element(v) for k, v in x.items()},
    schemdraw.util.Point: lambda x: schemdraw_object_properties(x, listify_point),
    schemdraw.segments.Segment: lambda x: schemdraw_object_properties(x, dictify_segment),
    schemdraw.segments.SegmentText: lambda x: schemdraw_object_properties(x, dictify_segment_text),
    schemdraw.segments.SegmentCircle: lambda x: schemdraw_object_properties(x, dictify_segment_circle),
    schemdraw.transform.Transform: lambda x: schemdraw_object_properties(x, dictify_transform)
}

def serialize_schemdraw_element(e):
    serialize = schemdraw_serializers.get(type(e), lambda _: None)
    return serialize(e)

def dictify_element(e: schemdraw.elements.Element) -> SimpleCircuitObjectProperties:
    return SimpleCircuitObjectProperties(
        type=e.type,
        name=e.name,
        reverse=e.is_reverse,
        values={
            '_userparams' : serialize_schemdraw_element(e._userparams),
            'segments' : serialize_schemdraw_element(e.segments),
            'params' : serialize_schemdraw_element(e.params),
            'anchors' : serialize_schemdraw_element(e.anchors),
            'absanchors' : serialize_schemdraw_element(e.absanchors),
            'transform' : serialize_schemdraw_element(e.transform),
            'absdrop' : serialize_schemdraw_element(e.absdrop)
        }
    )

def schematic_to_dict(d: schemdraw.Drawing) -> list[SimpleCircuitObjectProperties]:
    return [dictify_element(e) for e in d.elements]

schemdraw_deserializers = {
    str(schemdraw.segments.Segment.__name__) : lambda x: schemdraw.segments.Segment(**deserialize_schemdraw_elements(x)), # type: ignore
    str(schemdraw.segments.SegmentText.__name__) : lambda x: schemdraw.segments.SegmentText(**deserialize_schemdraw_elements(x)),
    str(schemdraw.segments.SegmentCircle.__name__) : lambda x: schemdraw.segments.SegmentCircle(**deserialize_schemdraw_elements(x)),
    str(schemdraw.util.Point.__name__) : lambda *x: schemdraw.util.Point(*x),
    str(schemdraw.transform.Transform.__name__) : lambda x: schemdraw.transform.Transform(**deserialize_schemdraw_elements(x)),
}

def deserialize_schemdraw_elements(element: dict[str, Any] | list) -> Any:
    if type(element) == list:
        return [deserialize_schemdraw_elements(e) for e in element]
    if type(element) == dict:
        try:
            return schemdraw_deserializers[element['type']](element['values'])
        except KeyError:
            return {k: deserialize_schemdraw_elements(v) for k, v in element.items()}
    return element

def combine_to_complex(real_imag: tuple[str, str], z: str, kv: dict[str, Any]) -> dict[str, Any]:
    kv.update({z: complex(kv.pop(real_imag[0], 0), kv.pop(real_imag[1], 0))})
    return kv

simple_circuit_element_types = {
    'voltage_source' : lambda **kwargs: simple_circuit_elements.VoltageSource(**kwargs),
    'current_source' : lambda **kwargs: simple_circuit_elements.CurrentSource(**kwargs),
    'ac_voltage_source' : lambda **kwargs: simple_circuit_elements.ACVoltageSource(**kwargs),
    'ac_current_source' : lambda **kwargs: simple_circuit_elements.ACCurrentSource(**kwargs),
    'rect_voltage_source' : lambda **kwargs: simple_circuit_elements.RectVoltageSource(**kwargs),
    'rect_current_source' : lambda **kwargs: simple_circuit_elements.RectCurrentSource(**kwargs),
    'complex_voltage_source' : lambda **kwargs: simple_circuit_elements.ComplexVoltageSource(**combine_to_complex(('V_real', 'V_imag'), 'V', kwargs)),
    'complex_current_source' : lambda **kwargs: simple_circuit_elements.ComplexCurrentSource(**combine_to_complex(('I_real', 'I_imag'), 'I', kwargs)), 
    'resistor' : lambda **kwargs: simple_circuit_elements.Resistor(**kwargs),
    'conductance' : lambda **kwargs: simple_circuit_elements.Conductance(**kwargs),
    'impedance' : lambda **kwargs: simple_circuit_elements.Impedance(**combine_to_complex(('R', 'X'), 'Z', kwargs)),
    'admittance' : lambda **kwargs: simple_circuit_elements.Admittance(**combine_to_complex(('G', 'B'), 'Y', kwargs)),
    'capacitor' : lambda **kwargs: simple_circuit_elements.Capacitor(**kwargs),
    'inductance' : lambda **kwargs: simple_circuit_elements.Inductance(**kwargs),
    'ground' : lambda **kwargs: simple_circuit_elements.Ground(**kwargs),
    'line' : lambda **kwargs: simple_circuit_elements.Line(**kwargs)
}

def undictify_element(element_dict: dict[str, Any], circuit_dict: dict[str, Any]) -> schemdraw.elements.Element:
    kwargs = deserialize_schemdraw_elements(element_dict['values']['_userparams'])
    kwargs.update({'name': element_dict.get('name', '')})
    kwargs.update({'reverse': element_dict.get('reverse', False)})
    if element_dict['name'] in circuit_dict.keys():
        kwargs.update(circuit_dict[element_dict['name']])
    try:
        element = simple_circuit_element_types[element_dict['type']](**kwargs)
    except KeyError:
        element = simple_circuit_elements.Element(**kwargs)
    element.segments=deserialize_schemdraw_elements(element_dict['values']['segments'])
    element.params=deserialize_schemdraw_elements(element_dict['values']['params'])
    element.anchors=deserialize_schemdraw_elements(element_dict['values']['anchors'])
    element.absanchors=deserialize_schemdraw_elements(element_dict['values']['absanchors'])
    element.transform=deserialize_schemdraw_elements(element_dict['values']['transform'])
    element.absdrop=deserialize_schemdraw_elements(element_dict['values']['absdrop'])
    return element

def undictify_schematic(schematic_dict: dict) -> Schematic:
    schematic = Schematic()
    circuit_dict = {c['id']: c['value'] for c in schematic_dict['circuit']['components']}
    schematic.elements.extend([undictify_element(e, circuit_dict) for e in schematic_dict['simple_circuit']])
    return schematic

def dictify_all(schematic: Schematic) -> dict:
    return {
        'circuit': dictify_circuit(circuit_translator(schematic)),
        'simple_circuit': schematic_to_dict(schematic)
    }

serialize = functools.partial(dump_load.serialize, dict_processor=dictify_all)
dump = functools.partial(dump_load.dump, dump_fcn=serialize)

deserialize = functools.partial(dump_load.deserialize, dict_preprocessor=undictify_schematic)
load = functools.partial(dump_load.load, deserialize_fcn=deserialize)