from .Elements import Schematic, SimpleAnalysisElement
import schemdraw.elements
import schemdraw.util
import schemdraw.transform
import json
from typing import Any, TypedDict, Callable, TypeVar

class ObjectProperties(TypedDict):
    type: str
    values: dict[str, Any] | list

T = TypeVar('T')

def object_properies(object: T, value_fcn: Callable[[T], dict[str, Any] | list]) -> ObjectProperties:
    return ObjectProperties(type=str(type(object).__name__), values=value_fcn(object))


def listify_point(p: schemdraw.util.Point) -> list[float]:
    return [serialize(p.x), serialize(p.y)]

def dictify_segment(s: schemdraw.segments.Segment) -> dict[str, Any]:
    return {
        'path' : serialize(s.path),
        'zorder' : serialize(s.zorder),
        'color' : serialize(s.color),
        'fill' : serialize(s.fill),
        'lw' : serialize(s.lw),
        'ls' : serialize(s.ls),
        'arrow' : serialize(s.arrow),
        'arrowwidth' : serialize(s.arrowwidth),
        'arrowlength' : serialize(s.arrowlength),
        'clip' : serialize(s.clip),
        'capstyle' : serialize(s.capstyle),
        'joinstyle' : serialize(s.joinstyle),
        'visible' : serialize(s.visible)
    }

def dictify_segment_text(s: schemdraw.segments.SegmentText) -> dict[str, Any]:
    return {
        'pos' : serialize(s.xy),
        'label' : serialize(s.text),
        'align' : serialize(s.align),
        'font' : serialize(s.font),
        'mathfont' : serialize(s.mathfont),
        'fontsize' : serialize(s.fontsize),
        'color' : serialize(s.color),
        'rotation' : serialize(s.rotation),
        'rotation_mode' : serialize(s.rotation_mode),
        'rotation_global' : serialize(s.rotation_global),
        'clip' : serialize(s.clip),
        'zorder' : serialize(s.zorder),
        'visible' : serialize(s.visible)
        }

def dictify_segment_circle(s: schemdraw.segments.SegmentCircle) -> dict[str, Any]:
    return {
        'center' : serialize(s.center),
        'radius' : serialize(s.radius),
        'color' : serialize(s.color),
        'lw' : serialize(s.lw),
        'ls' : serialize(s.ls),
        'fill' : serialize(s.fill),
        'clip' : serialize(s.clip),
        'zorder' : serialize(s.zorder),
        'ref' : serialize(s.endref),
        'visible' : serialize(s.visible)
        }

def dictify_transform(t: schemdraw.transform.Transform) -> dict[str, Any]:
    return {
        'theta' : serialize(t.theta),
        'globalshift' : serialize(t.shift),
        'localshift' : serialize(t.localshift),
        'zoom' : serialize(t.zoom)
    }

serializers = {
    str: lambda x: x,
    int: lambda x: x,
    float: lambda x: x,
    bool: lambda x: x,
    dict: lambda x: {k: serialize(v) for k, v in x.items()},
    list: lambda x: [serialize(e) for e in x],
    tuple: lambda x: [serialize(e) for e in x],
    schemdraw.util.Point: lambda x: object_properies(x, listify_point),
    schemdraw.segments.Segment: lambda x: object_properies(x, dictify_segment),
    schemdraw.segments.SegmentText: lambda x: object_properies(x, dictify_segment_text),
    schemdraw.segments.SegmentCircle: lambda x: object_properies(x, dictify_segment_circle),
    schemdraw.transform.Transform: lambda x: object_properies(x, dictify_transform)
}

def serialize(e):
    serialize = serializers.get(type(e), lambda _: None)
    return serialize(e)

def dictify_element(e: schemdraw.elements.Element) -> dict[str, Any]:
    return {
        '_userparams' : serialize(e._userparams),
        'segments' : serialize(e.segments),
        'params' : serialize(e.params),
        'anchors' : serialize(e.anchors),
        'absanchors' : serialize(e.absanchors),
        'transform' : serialize(e.transform),
        'absdrop' : serialize(e.absdrop)
    }

def drawing_to_dict(d: schemdraw.Drawing) -> list[dict[str, Any]]:
    return [dictify_element(e) for e in d.elements]

deserializers = {
    str(schemdraw.segments.Segment.__name__) : lambda x: schemdraw.segments.Segment(**deserialize(x)), # type: ignore
    str(schemdraw.segments.SegmentText.__name__) : lambda x: schemdraw.segments.SegmentText(**deserialize(x)),
    str(schemdraw.segments.SegmentCircle.__name__) : lambda x: schemdraw.segments.SegmentCircle(**deserialize(x)),
    str(schemdraw.util.Point.__name__) : lambda *x: schemdraw.util.Point(*x),
    str(schemdraw.transform.Transform.__name__) : lambda x: schemdraw.transform.Transform(**deserialize(x))
}

def deserialize(element: dict[str, Any] | list) -> Any:
    if type(element) == list:
        return [deserialize(e) for e in element]
    if type(element) == dict:
        try:
            return deserializers[element['type']](element['values'])
        except KeyError:
            return {k: deserialize(v) for k, v in element.items()}
    return element

def undictify_element(element_dict: dict[str, Any]) -> schemdraw.elements.Element:
    element = schemdraw.elements.Element(**deserialize(element_dict['_userparams']))
    element.segments=deserialize(element_dict['segments'])
    element.params=deserialize(element_dict['params'])
    element.anchors=deserialize(element_dict['anchors'])
    element.absanchors=deserialize(element_dict['absanchors'])
    element.transform=deserialize(element_dict['transform'])
    element.absdrop=deserialize(element_dict['absdrop'])
    return element

def schematic(d: list[dict[str, Any]]) -> Schematic:
    schematic = Schematic()
    schematic.elements.extend([undictify_element(e) for e in d])
    return schematic

def dump_json(json_file: str, schematic: Schematic) -> None:
    with open(json_file, 'w') as file:
        json.dump(drawing_to_dict(schematic), file)

def load_json(json_file: str) -> Schematic:
    with open(json_file, 'r') as file:
        return schematic(json.load(file))