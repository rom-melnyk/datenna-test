from .Node import Node
from .Edge import Edge

class GrPath:
    """Simple representation of the path between two nodes in the graph.

    The `from_node` and `to_node` must be explicitly defined
    because the path might contain one edge.
    E.g.,
        ```
        nodes: [A, B, C, D]
        edges: [B-A, B-C, D-C] # Some edges are flipped
        path: {"from_node": A, "to_node": D, edges: [B-A, B-C, D-C]}
        ```
    """
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

    def get_ordered_nodes(self) -> list[Node]:
        """Return the "normalized" list of path nodes.

        E.g.,
            ```
            nodes: [A, B, C, D]
            edges: [B-A, B-C, D-C] # Some edges are flipped
            path: {"from_node": A, "to_node": D, edges: [B-A, B-C, D-C]}
            path.get_ordered_nodes() -> [A, B, C, D]
            ```
        """
        ordered = [self.from_node]
        for e in self.edges:
            last_node = ordered[len(ordered) - 1]
            ordered.append(e.get_opposite_node(last_node))
        return ordered

    def to_api_repr(self) -> dict:
        """Bring the path to the API-friendly representation."""
        nodes = [{"id": n.id, "name": n.props["name"]} for n in self.get_ordered_nodes()]
        distance = sum([e.props["distance"] for e in self.edges])
        return {
            "from_id": self.from_node.id,
            "from_name": self.from_node.props["name"],
            "to_id": self.to_node.id,
            "to_name": self.to_node.props["name"],
            "nodes": nodes,
            "distance": round(distance, 2)
        }
