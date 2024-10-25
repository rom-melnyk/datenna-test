import re
from .db import db

# def get_city_by_id(id: str):
#     return graph_db.nodes[id]

# def add_city(name: str, population: int):
#     city_node = Node(props={"name": name, "population": population})
#     graph_db.add_node(city_node)

# def add_route(from_id: str, to_id: str, distance: int):
#     if not graph_db.nodes[from_id]:
#         raise Error(f"Unknown city <{from_id}>; please add it first")
#     if not graph_db.nodes[to_id]:
#         raise Error(f"Unknown city <{to_id}>; please add it first")
#     from_node = graph_db.nodes[from_id]
#     to_node = graph_db.nodes[to_id]
#     edge = Edge(from_node=from_node, to_node=to_node, props={"distance": distance})
#     graph_db.add

async def get_city(city_id: int):
    """Return the city (node) info."""
    if city_id in db().nodes:
        return db().nodes[city_id]
    else:
        return {"error": True, "description": f"City {city_id} not found"}

async def get_cities(
        mask: str,
        population_from: int = None,
        population_to: int = None
    ) -> list:
    """Return the list of the cities matching given criteria.
    
    The `mask` is case-sensitive and can contain "*":
        - mask="ast" -> ✅ "last", "Astra". ❌ "La-St".
        - mask="a*t" -> ✅ "last", "Assertion". ❌ "Assembly".

    The `population_from`/`_to` are optional.
    """
    # Human-friendly syntax -> RegExp
    mask_re = re.compile(mask.replace("*", ".*"), re.IGNORECASE)
    return [
        c for c in db().nodes.values()
        if mask_re.search(c.props["name"])
        and (population_from == None or c.props["population"] >= population_from)
        and (population_to == None or c.props["population"] <= population_to)
    ]

async def get_routes_from_city(city_id: int, max_hops: int = None):
    if city_id not in db().nodes:
        return {"error": True, "description": f"City {city_id} not found"}
    if max_hops == None:
        max_hops = 2
    if max_hops > 3 or max_hops < 1:
        return {"error": True, "description": f"The `max_hops` must be between 1 and 3"}

    city = db().nodes[city_id]
    routes = db().get_paths_from_node(city, 2)
    return routes
