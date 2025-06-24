from . import elements as elm
from dataclasses import dataclass

class FloatingGroundNode(Exception): pass

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
    node_zero_label: str = '0'

    def __post_init__(self):
        if self.node_zero_label not in self.node_labels and self.number_of_nodes != 0:
            raise FloatingGroundNode
        if len(set(self.branch_ids)) != len(self.branches):
            raise AmbiguousBranchIDs
        
    @property
    def branch_ids(self) -> list[str]:
        return [b.id for b in self.branches]

    @property
    def node_labels(self) -> list[str]:
        if len(self.branches) == 0:
            return [self.node_zero_label]
        node1_set = {branch.node1 for branch in self.branches}
        node2_set = {branch.node2 for branch in self.branches}
        return sorted(list(node1_set.union(node2_set)))

    @property
    def number_of_nodes(self) -> int:
        return len(self.node_labels)

    def is_zero_node(self, node: str) -> bool:
        return node == self.node_zero_label

    def branches_connected_to(self, node: str) -> list[Branch]:
        connected_branches = [branch for branch in self.branches if branch.node1 == node or branch.node2 == node]
        connected_branches.sort(key=lambda x: x.node1 if x.node1!=node else x.node2)
        return connected_branches

    def nodes_connected_to(self, node: str) -> set[str]:
        return {b.node1 if b.node1 != node else b.node2 for b in self.branches_connected_to(node=node)}

    def branches_between(self, node1: str, node2: str) -> list[Branch]:
        return [branch for branch in self.branches if set((branch.node1, branch.node2)) == set((node1, node2))]

    def __getitem__(self, id: str) -> Branch:
        return {b.id: b for b in self.branches}[id]