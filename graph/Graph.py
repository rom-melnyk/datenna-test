import json
from .Node import Node
from .Edge import Edge

class Graph:
    def __init__(self):
        self.nodes = {} # dict[int, Node]
        self.edges = {} # dict[int, Edge]
        self.node_edges = {} # dict[int, list[Edge]]
    
    def add_node(self, node: Node):
        """Add a node to the graph."""
        if node.id in self.nodes:
            raise Exception(f"The node \"{node.id}\" already exists")
        self.nodes[node.id] = node
        self.node_edges[node.id] = []

    def add_edge(self, edge: Edge):
        """Add an edge to the graph and establish all necessary connections."""
        if edge.id in self.edges:
            raise Exception(f"The node \"{edge.id}\" already exists")

        if edge.from_node.id not in self.nodes:
            self.add_node(edge.from_node)
        if edge.to_node.id not in self.nodes:
            self.add_node(edge.to_node)

        self.edges[edge.id] = edge
        
        self.node_edges[edge.from_node.id].append(edge)
        self.node_edges[edge.to_node.id].append(edge)

    def get_node_edges(self, node: Node) -> list[Edge]:
        return self.node_edges[node.id]

    def has_edge_between(self, n1: Node, n2: Node) -> bool:
        for e in self.node_edges[n1.id]:
            if e.get_opposite_node(n1) == n2:
                return True
        return False

    def get_paths_from_node(self):
        pass
    
    def serialize(self) -> list[str]:
        """Serialize the graph into list of JSONs.
        ⚠️ Mind that the result is the list of JSON strings but not a JSON itself ⚠️
        This is done for the sake of performance: parsing a 10Mb JSON is heavy,
        but parsing 100k short strings is ok.
        """
        serialized = []
        for n in self.nodes.values():
            serialized.append(json.dumps({
                "type": "Node",
                "id": n.id,
                "props": n.props,
            }))
        for e in self.edges.values():
            serialized.append(json.dumps({
                "type": "Edge",
                "id": e.id,
                "from_node_id": e.from_node.id,
                "to_node_id": e.to_node.id,
                "props": e.props,
            }))
        return serialized
    
    def from_serialized(serialized: list[str]) -> "Graph":
        objects = [json.parse(s) for s in serialized]
        nodes = [Node(id=n.id, props=n.props) for n in objects if objects["type"] == "Node"]
        nodes_dict = {}
        for n in nodes:
            nodes_dict[n.id] = n
        edges = [
            Edge(
                id=e.id,
                from_node=nodes_dict[e.from_node_id],
                to_node=nodes_dict[e.to_node_id],
                props=e.props
            ) for e in objects if objects["type"] == "Edge"]
        graph = Graph()
        for n in nodes:
            graph.add_node(n)
        for e in edges:
            graph.add_edge(e)
        return graph