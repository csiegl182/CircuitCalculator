from NodalAnalysis import *
from typing import Set, List, Tuple
import json
import schemdraw
import schemdraw.elements as elm

def round_node(node: schemdraw.util.Point) -> schemdraw.util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return schemdraw.util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: schemdraw.elements.Element2Term) -> Tuple[schemdraw.util.Point, schemdraw.util.Point]:
    return round_node(element.absanchors['start']), round_node(element.absanchors['end'])

def get_all_nodes(elements: List[schemdraw.elements.Element2Term]) -> Set[schemdraw.util.Point]:
    nodes = {round_node(e.absanchors['start']) for e in elements}
    nodes = nodes.union({round_node(e.absanchors['end']) for e in elements})
    return nodes

element_type = {
    schemdraw.elements.sources.SourceI : "real_current_source",
    schemdraw.elements.twoterm.ResistorIEEE : "resistor",
    schemdraw.elements.lines.Line: "line"
}

def get_identical_nodes(node: schemdraw.util.Point, elements: List[schemdraw.elements.Element2Term]) -> Set[schemdraw.util.Point]:
    lines = [element for element in elements if element_type[type(element)] == "line"]
    identical_nodes = set()
    for line in lines:
        n1, n2 = get_nodes(line)
        if node == n1:
            identical_nodes.add(n2)
        elif node == n2:
            identical_nodes.add(n1)
    return identical_nodes

def get_unique_nodes(elements: List[schemdraw.elements.Element2Term]) -> Set[schemdraw.util.Point]:
    unique_nodes = get_all_nodes(elements)
    for node in get_all_nodes(elements):
        if node in unique_nodes:
            for n in get_identical_nodes(node, elements):
                unique_nodes.remove(n)
    return unique_nodes

def get_unique_node_mapping(elements: List[schemdraw.elements.Element2Term]) -> Dict[schemdraw.util.Point, schemdraw.util.Point]:
    unique_nodes = get_unique_nodes(elements)
    node_mapping = {}
    for n in get_all_nodes(elements):
        identical_nodes = get_identical_nodes(n, elements)
        current_unique_node = unique_nodes.intersection(identical_nodes)
        if len(current_unique_node) > 0:
            node_mapping.update({n: current_unique_node.pop()})
        else:
            node_mapping.update({n: n})
    return node_mapping

def get_two_term_elements(drawing: schemdraw.Drawing) -> List[schemdraw.elements.Element2Term]:
    return [e for e in drawing.elements if isinstance(e, schemdraw.elements.Element2Term)]

def parse_drawing(drawing: schemdraw.Drawing):
    el = []
    unique_node_mapping = get_unique_node_mapping(get_two_term_elements(drawing))
    unique_nodes = list(get_unique_nodes(get_two_term_elements(drawing)))
    print(unique_node_mapping)
    elements = [e for e in get_two_term_elements(drawing) if element_type[type(e)] != "line"]
    for e in elements:
        n1, n2 = get_nodes(e)
        d = {
            "types": element_type[type(e)],
            "id" : "",
            "N1" : unique_nodes.index(unique_node_mapping[n1]),
            "N2" : unique_nodes.index(unique_node_mapping[n2])
        }
        el.append(d)
    print(json.dumps(el, indent=2))


if __name__ == '__main__':

    network = load_network_from_json('./example_network_1.json')
    Y = create_node_admittance_matrix_from_network(network)
    I = create_current_vector_from_network(network)
    U = calculate_node_voltages(Y, I)

    n1, n2 = 1, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2):.2f}')
    n1, n2 = 1, 2
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2):.2f}')
    n1, n2 = 2, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2):.2f}')

    with open('./example_network_1.json', 'r') as json_file:
        network_definition = json.load(json_file)

    print(json.dumps(network_definition, indent=2))
    for branch in network_definition:
        branch['U'] = calculate_branch_voltage(U, branch['N1'], branch['N2'])
        if branch['type'] == "resistor":
            branch['I'] = branch['U']/branch['R']
        elif branch['type'] == "real_current_source":
            branch['Ui'] = branch['I'] * branch['R']
            branch['Us'] = branch['Ui'] + branch['U']
    print(json.dumps(network_definition, indent=2))
    
    with schemdraw.Drawing() as d:
        d += elm.SourceI().up().label('1A/100Ohm')
        d += elm.Resistor().right().label('10Ohm')
        d += elm.Resistor().down().label('20Ohm')
        d += elm.Line().left()
        d += elm.Ground()
    parse_drawing(d)
    #d.draw()

    