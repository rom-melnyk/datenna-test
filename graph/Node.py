from .utils.utils import autoinc

new_id = autoinc()

class Node:
    def __init__(self, id: str = None, props: dict = None):
        if id == None:
            id = next(new_id)
        if props == None:
            props = {}

        self.id = id
        self.props = props
