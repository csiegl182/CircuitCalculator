import schemdraw.elements, schemdraw.util
from dataclasses import dataclass
from . import Elements as elm

class UnknownElement(Exception): ...
class MultipleGroundNodes(Exception): ...

@dataclass(frozen=True)
class SchematicDiagramParser:
    drawing: elm.Schematic

    @property
    def all_elements(self) -> list[schemdraw.elements.Element]:
        return self.drawing.elements

    @property
    def circuit_elements(self) -> list[schemdraw.elements.Element]:
        def has_name_property(e: schemdraw.elements.Element):
            try:
                _ = e.name
            except AttributeError:
                return False
            return True
        return [e for e in self.all_elements if has_name_property(e)]

    @property
    def line_elements(self) -> list[elm.Line]:
        return [e for e in self.all_elements if type(e) is elm.Line]
    
    @property
    def node_elements(self) -> list[elm.Node]:
        return [e for e in self.all_elements if isinstance(e, elm.Node)]

    @property
    def all_nodes(self) -> set[schemdraw.util.Point]:
        nodes = {elm.round_node(e.absanchors['start']) for e in self.circuit_elements}
        nodes = nodes.union({elm.round_node(e.absanchors['end']) for e in self.circuit_elements})
        nodes = nodes.union({elm.round_node(e.absanchors['start']) for e in self.line_elements})
        nodes = nodes.union({elm.round_node(e.absanchors['end']) for e in self.line_elements})
        return nodes

    @property
    def unique_nodes(self) -> set[schemdraw.util.Point]:
        nodes = self.all_nodes
        for node in self.all_nodes:
            if node in nodes:
                for n in self._get_equal_electrical_potential_nodes(node).intersection(nodes):
                    nodes.remove(n)
                nodes.add(node)
        return nodes

    @property
    def node_label_mapping(self) -> dict[schemdraw.util.Point, str]:
        node_labels = {self.unique_node_mapping[elm.get_nodes(e)[0]] : e.node_id for e in self.node_elements}
        node_index = len(node_labels)+1
        unlabeled_nodes = [p for p in self.unique_nodes if p not in node_labels.keys()]
        for p in unlabeled_nodes:
            while str(node_index) in node_labels.values():
                node_index += 1
            node_labels.update({p : str(node_index)})
        return node_labels

    @property
    def unique_node_mapping(self) -> dict[schemdraw.util.Point, schemdraw.util.Point]:
        node_mapping = {}
        for n in self.all_nodes:
            identical_nodes = self._get_equal_electrical_potential_nodes(n)
            identical_nodes.remove(n)
            current_unique_node = self.unique_nodes.intersection(identical_nodes)
            if len(current_unique_node) > 0:
                node_mapping.update({n: current_unique_node.pop()})
            else:
                node_mapping.update({n: n})
        return node_mapping

    @property
    def ground(self) -> schemdraw.util.Point:
        ground_nodes = [n for n in self.node_elements if isinstance(n, elm.Ground)]
        if len(ground_nodes) > 1:
            raise MultipleGroundNodes
        if len(ground_nodes) == 0:
            return list(self.unique_nodes)[0]
        else:
            return elm.get_nodes(ground_nodes[0])[0]

    @property
    def ground_label(self) -> str:
        return self._get_node_index(self.ground)

    def _get_equal_electrical_potential_nodes(self, node: schemdraw.util.Point) -> set[schemdraw.util.Point]:
        equal_electrical_potential_nodes = set([node])
        old_length = 0
        while len(equal_electrical_potential_nodes) > old_length:
            old_length = len(equal_electrical_potential_nodes)
            for line in self.line_elements:
                n1, n2 = elm.get_nodes(line)
                if n1 in equal_electrical_potential_nodes:
                    equal_electrical_potential_nodes.add(n2)
                elif n2 in equal_electrical_potential_nodes:
                    equal_electrical_potential_nodes.add(n1)
        return equal_electrical_potential_nodes

    def _get_node_index(self, node: schemdraw.util.Point) -> str:
        return self.node_label_mapping[self.unique_node_mapping[node]]

    def get_element(self, name: str) -> schemdraw.elements.Element:
        elements = [e for e in self.circuit_elements if e.name == name]
        if len(elements) == 0:
            raise UnknownElement(name)
        else:
            return elements[0]