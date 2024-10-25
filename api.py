import re
from fastapi import Response
from pydantic import BaseModel
from .db import db
from .graph.Node import Node
from .graph.Edge import Edge

async def get_city(city_id: int, response: Response):
    """Return the city (node) info."""
    if city_id in db().nodes:
        return db().nodes[city_id]
    else:
        response.status_code = 404
        return {"error": True, "description": f"City {city_id} not found"}

async def get_cities(
        name: str | None,
        population_over: int | None,
        population_under: int | None,
        response: Response
    ) -> list:
    """Return the list of the cities matching given (optional) criteria.

    The `name` is case-sensitive mask and can contain "*":
        - name="ast" -> ✅ "last", "Astra". ❌ "La-St".
        - name="a*t" -> ✅ "last", "Assertion". ❌ "Assembly".
    """
    # Human-friendly syntax -> RegExp
    name_re = re.compile(
        ".*" if not name else name.replace("*", ".*"),
        re.IGNORECASE
    )
    cities = [
        city for city in db().nodes.values()
        if name_re.search(city.props["name"])
        and (population_over == None or city.props["population"] >= population_over)
        and (population_under == None or city.props["population"] <= population_under)
    ]

    return {"cities": cities}

async def get_routes_from_city(city_id: int, max_hops: int | None, response: Response):
    """Return the list of possible routes from given city.

    Maximum number of hops must be within [1..3];
    it makes little sense to travel with >2 stopovers."""
    if city_id not in db().nodes:
        response.status_code = 400
        return {"error": True, "description": f"City {city_id} not found"}
    if max_hops == None:
        max_hops = 2
    if max_hops > 3 or max_hops < 1:
        response.status_code = 400
        return {"error": True, "description": f"The `max_hops` must be between 1 and 3"}

    city = db().nodes[city_id]
    routes = db().get_paths_from_node(city, max_hops)
    routes_repr = [r.to_api_repr() for r in routes]

    """Imitate the `ORDER BY hops ASC, distance ASC`.
    Think "closest-to-travel cities first".
    """
    routes_repr.sort(key=lambda r: (len(r["nodes"]), r["distance"]))
    return {"routes": routes_repr}

class City(BaseModel):
    name: str
    population: int

async def add_city(city: City, response: Response) -> Node:
    has_city_with_name = [cty for cty in db().nodes.values() if cty.props["name"] == city.name]
    if has_city_with_name:
        response.status_code = 400
        return {"error": True, "description": f"City \"{city.name}\" already exists"}

    node = Node(props={"name": city.name, "population": city.population})
    db().add_node(node)
    return node

class Route(BaseModel):
    from_id: int
    to_id: int
    distance: int | float

async def add_route(route: Route, response: Response) -> Edge:
    if not route.from_id in db().nodes:
        response.status_code = 400
        return {
            "error": True,
            "description": f"Unknown city <{route.from_id}>; please add it first"
        }
    if not route.to_id in db().nodes:
        response.status_code = 400
        return {
            "error": True,
            "description": f"Unknown city <{route.to_id}>; please add it first"
        }

    from_node = db().nodes[route.from_id]
    to_node = db().nodes[route.to_id]
    edge = Edge(
        from_node=from_node,
        to_node=to_node,
        props={"distance": route.distance}
    )
    db().add_edge(edge)
    return edge
