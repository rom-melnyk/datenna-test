import json
from .Node import Node
from .Edge import Edge
from .GrPath import GrPath

class Graph:
    """Simple graph data engine."""
    def __init__(self):
        self.nodes: dict[int, Node] = {}
        self.edges: dict[int, Edge] = {}
        self.node_edges: dict[int, list[Edge]] = {}

    def add_node(self, node: Node):
        """Add a node to the graph."""
        if node.id in self.nodes:
            raise Exception(f"The node {node.id} already exists")
        self.nodes[node.id] = node
        self.node_edges[node.id] = []

    def add_edge(self, edge: Edge):
        """Add an edge to the graph and establish all necessary connections."""
        if edge.id in self.edges:
            raise Exception(f"The edge {edge.id} already exists")

        if edge.from_node.id not in self.nodes:
            self.add_node(edge.from_node)
        if edge.to_node.id not in self.nodes:
            self.add_node(edge.to_node)

        self.edges[edge.id] = edge

        self.node_edges[edge.from_node.id].append(edge)
        self.node_edges[edge.to_node.id].append(edge)

    def get_node_edges(self, node: Node) -> list[Edge]:
        """Return the list of edges hitting given node."""
        return self.node_edges[node.id]

    def has_edge_between(self, n1: Node, n2: Node) -> bool:
        for e in self.node_edges[n1.id]:
            if e.get_opposite_node(n1) == n2:
                return True
        return False

    def get_paths_from_node(
        self,
        node: Node,
        max_hops,
        _current_path: GrPath = None,
        _visited_nodes: set[Node] = None,
    ) -> list[GrPath]:
        """Find all possible paths from given node within `max_hops`.

        The method is recursive and uses BFS graph traversing.
        **Known flaws:** if there is >1 paths between A and B,
        the method returns the 1st shortest path; all the other paths are ignored:
            ```
            A -- B
            |    |
            C -- D
            get_paths_from_node(A, max_hops=2) -> [{A-B}, {A-C}, {A-B-D}]
                                                  but not {A-B-D-C}
                                                  neither {A-C-D-B}
            ```
        """
        if _current_path != None and len(_current_path.edges) >= max_hops:
            return []
        if _visited_nodes == None:
            _visited_nodes: set[Node] = set()

        paths: list[GrPath] = []
        for e in self.get_node_edges(node):
            """Add 1st degree paths (from given node)."""
            if e.get_opposite_node(node) in _visited_nodes:
                continue
            if _current_path == None:
                path = GrPath(e, node)
            else:
                path = _current_path.clone()
                path.add_edge(e)
            _visited_nodes.add(path.to_node)
            paths.append(path)

        all_paths = paths[:]
        for p in paths:
            """Add 2nd degree paths (from each destination nodes of 1st deg. paths)"""
            all_paths += self.get_paths_from_node(
                p.to_node,
                max_hops,
                _current_path=p,
                _visited_nodes=_visited_nodes)

        return all_paths

    def serialize(self) -> list[str]:
        """Serialize the graph into list of JSONs.

        ⚠️ Mind that the result is the list of JSON strings but not a JSON itself ⚠️
        This is done for the sake of performance: parsing a 10Mb JSON is heavy,
        but parsing 100k short strings is ok.
        """
        serialized = []
        for n in self.nodes.values():
            serialized.append(n.serialize())
        for e in self.edges.values():
            serialized.append(e.serialize())
        return serialized

    def from_serialized(serialized: list[str]) -> "Graph":
        """Restore the graph from serialized representation.

        See Also
        --------
        `serialize()`
        """
        objects = [json.loads(s) for s in serialized]
        nodes = [Node(id=n["id"], props=n["props"]) for n in objects if n["type"] == "Node"]
        nodes_dict = {}
        for n in nodes:
            nodes_dict[n.id] = n
        edges = [
            Edge(
                id=e["id"],
                from_node=nodes_dict[e["from_node_id"]],
                to_node=nodes_dict[e["to_node_id"]],
                props=e["props"]
            ) for e in objects if e["type"] == "Edge"]
        graph = Graph()
        for n in nodes:
            graph.add_node(n)
        for e in edges:
            graph.add_edge(e)
        return graph
