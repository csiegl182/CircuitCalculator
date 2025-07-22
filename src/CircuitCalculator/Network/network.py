from . import elements as elm
from dataclasses import dataclass

class AmbiguousBranchIDs(Exception): pass

@dataclass(frozen=True)
class Branch:
    node1 : str
    node2 : str
    element : elm.NortenTheveninElement

    @property
    def id(self) -> str:
        return self.element.name

@dataclass(frozen=True)
class Network:
    branches: list[Branch]
    reference_node_label: str = '0'

    def __post_init__(self):
        branch_ids = [b.id for b in self.branches]
        if len(set(branch_ids)) != len(branch_ids):
            raise AmbiguousBranchIDs
        
    @property
    def branch_ids(self) -> list[str]:
        return [b.id for b in self.branches if b.node1 in self.node_labels or b.node2 in self.node_labels]

    @property
    def node_labels(self) -> set[str]:
        connected_nodes = set([self.reference_node_label])
        nodes_to_assess = set([self.reference_node_label])
        nodes_already_assessed = set()
        while nodes_to_assess:
            new_nodes_to_assess = set()
            for node in nodes_to_assess:
                new_nodes_to_assess.update(self.nodes_connected_to(node))
            nodes_already_assessed.update(nodes_to_assess)
            nodes_to_assess = new_nodes_to_assess - nodes_already_assessed
            connected_nodes.update(new_nodes_to_assess)
        return connected_nodes

    @property
    def number_of_nodes(self) -> int:
        return len(self.node_labels)

    def is_zero_node(self, node: str) -> bool:
        return node == self.reference_node_label

    def branches_connected_to(self, node: str) -> list[Branch]:
        connected_branches = [branch for branch in self.branches if branch.node1 == node or branch.node2 == node]
        connected_branches.sort(key=lambda x: x.node1 if x.node1!=node else x.node2)
        return connected_branches

    def nodes_connected_to(self, node: str) -> set[str]:
        return {b.node1 if b.node1 != node else b.node2 for b in self.branches_connected_to(node=node)}

    def branches_between(self, node1: str, node2: str) -> list[Branch]:
        return [branch for branch in self.branches if set((branch.node1, branch.node2)) == set((node1, node2))]

    def __getitem__(self, id: str) -> Branch:
        if id not in [b.id for b in self.branches]:
            raise KeyError(f"Branch with id '{id}' not found in the network.")
        if id not in self.branch_ids:
            raise KeyError(f"Branch with id '{id}' is floating.")
        return {b.id: b for b in self.branches if b.id in self.branch_ids}[id]