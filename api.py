import graph_db


def get_city_by_id(id: str):
    return graph_db.nodes[id]

def get_citis_by_criteria(name_pattern: str = None,
                          population_from: int = None,
                          population_to: int = None
):
    cities = [n for _, n in graph_db.nodes if n.props["name"]] # TODO

def add_city(name: str, population: int):
    city_node = Node(props={"name": name, "population": population})
    graph_db.add_node(city_node)

def add_route(from_id: str, to_id: str, distance: int):
    if not graph_db.nodes[from_id]:
        raise Error(f"Unknown city <{from_id}>; please add it first")
    if not graph_db.nodes[to_id]:
        raise Error(f"Unknown city <{to_id}>; please add it first")
    from_node = graph_db.nodes[from_id]
    to_node = graph_db.nodes[to_id]
    edge = Edge(from_node=from_node, to_node=to_node, props={"distance": distance})
    graph_db.add