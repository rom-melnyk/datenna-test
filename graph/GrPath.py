from .Node import Node
from .Edge import Edge

class GrPath:
    def __init__(self, edge: Edge, from_node: Node = None):
        self.edges: dict[Edge] = [edge]
        self.from_node = from_node if from_node != None else edge.from_node
        self.to_node = edge.get_opposite_node(self.from_node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        self.to_node = edge.get_opposite_node(self.to_node)

    def clone(self) -> "GrPath":
        cloned = GrPath(self.edges[0], self.from_node)
        for e in self.edges[1:]:
            cloned.add_edge(e)
        return cloned
