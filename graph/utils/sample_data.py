"""Generate sample graph data.

1. Generate 10k cities (nodes) as 100x100 field.
2. Generate routes between the cities:
    - All cities get vertical and horizontal connections with the neighbors.
    - Around 20% cities get up to 20 extra routes to other random cities.
3. The loops (X-X) re not permitted on the Graph level.
   Duplicate routes are generally permitted but not generated here.
"""

import math
import os
from random import randrange
from ..Node import Node
from ..Edge import Edge
from ..Graph import Graph
from ..utils.utils import generate_city_name

num_cities = 10_000
"""Try to map the `num_cities` into (more or less) square field."""
field_size_x = math.floor(math.sqrt(num_cities))
field_size_y = math.ceil(num_cities / field_size_x)
distance_mult = 100 # The distance between neighbors.
chance_extra_routes = 20 # % of cities getting extra routes.
num_extra_routes = 5

def calc_distance(x1, y1, x2, y2) -> int:
    """Calculate the distance between two points."""
    return round(
        math.sqrt((x1 - x2)**2 + (y1 - y2)**2) * distance_mult,
        2
    )

def generate_city_props():
    return {
        "population": randrange(1_000, 1_000_000, 1_000),
        "name": generate_city_name()
    }

def generate_sample_data() -> Graph:
    print(f"ℹ️ Generating a sample graph for {num_cities} cities...")
    nodes = [
        [Node(props=generate_city_props()) for x in range(field_size_x)]
        for y in range(field_size_y)
    ]
    graph = Graph()

    for y in range(field_size_y):
        for x in range(field_size_x):
            """Add cities (nodes) and generate the v/h routes (edges)."""
            graph.add_node(nodes[y][x])
            if y > 0:
                graph.add_edge(Edge(
                    nodes[y][x],
                    nodes[y-1][x],
                    props={"distance": calc_distance(x, y, x, y-1)}
                ))
            if x > 0:
                graph.add_edge(Edge(
                    nodes[y][x],
                    nodes[y][x-1],
                    props={"distance": calc_distance(x, y, x-1, y)}
                ))

    for y in range(field_size_x):
        for x in range(field_size_y):
            """Occasionaly generate extra edges."""
            if not randrange(100) < chance_extra_routes:
                continue

            for _ in range(num_extra_routes):
                extra_x = randrange(field_size_x)
                extra_y = randrange(field_size_y)
                if (not graph.has_edge_between(nodes[y][x], nodes[extra_y][extra_x])
                        and x != extra_x
                        and y != extra_y):
                    edge = Edge(
                        nodes[x][y],
                        nodes[extra_x][extra_y],
                        props={"distance": calc_distance(x, y, extra_x, extra_y)}
                    )
                    graph.add_edge(edge)

    return graph

def get_sample_data_filepath():
    return os.path.join(os.getcwd(), ".sample_data.graph")

def write_to_file(graph: Graph):
    filepath = get_sample_data_filepath()
    print(f"ℹ️ Writing to the {filepath}...")
    with open(filepath, "w", encoding="utf-8") as file:
        for line in graph.serialize():
            file.writelines(line + os.linesep)

    print(f"ℹ️ The {filepath} saved successfully.")

def read_from_file() -> Graph | None:
    filepath = get_sample_data_filepath()
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            serialized = file.readlines()
            graph = Graph.from_serialized(serialized)
            print(f"ℹ️ The graph of {len(graph.nodes)} nodes successfully initialized from the {filepath}")
            return graph
    except FileNotFoundError:
        print(f"⚠️ The {filepath} not found")
    except Exception as e:
        (f"❌ Failed reading from the {filepath}", e)
