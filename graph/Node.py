import json
from .utils.utils import Autoinc

auto_id = Autoinc()

class Node:
    def __init__(self, id: int = None, props: dict = None):
        if id == None:
            id = auto_id.next()
        else:
            auto_id.use(id)
        if props == None:
            props = {}

        self.id = id
        self.props = props

    def serialize(self) -> str:
        """Return a string representation of the node."""
        return json.dumps({
            "type": "Node",
            "id": self.id,
            "props": self.props,
        })
