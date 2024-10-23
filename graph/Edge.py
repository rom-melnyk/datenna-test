from .utils.utils import autoinc
from .Node import Node

new_id = autoinc()

class Edge:
    def __init__(
            self,
            from_node: Node,
            to_node: Node,
            id: int = None,
            props: dict = None):
        if from_node == to_node or from_node.id == to_node.id:
            raise Exception(f"The loop \"{from_node.id}-{to_node.id}\" is not permitted")

        if id == None:
            id = next(new_id)
        if props == None:
            props = {}

        self.id = id
        self.from_node = from_node
        self.to_node = to_node
        self.props = props

    def get_opposite_node(self, node: Node) -> Node:
        match node:
            case self.from_node:
                return self.to_node
            case self.to_node:
                return self.from_node
            case _:
                raise Exception(f"The node \"{node.id}\" does not belong to the edge \"{self.id}\"")
