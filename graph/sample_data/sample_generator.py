import math
from random import randint, randrange
from ..Node import Node
from ..Edge import Edge
from ..Graph import Graph
from ..utils.utils import generate_city_name

"""Generate sample graph data.

1. Generate 10k nodes as 100x100 field.
2. Generate vertical and horizontal connections between neighbors.
3. Around 20% nodes get 10..20 extra edges to random other nodes
   within given radius (1/4 of the field size; 25 nodes).
"""

num_nodes = 10_000
array_dim = math.floor(math.sqrt(num_nodes))
distance_mult = 100
chance_extra_edges = 20 # %
min_extra_edges = 10
max_extra_edges = 20
extra_edge_radius = math.ceil(array_dim / 4)

def calc_distance(x1, y1, x2, y2) -> int:
    """Calculate the distance between two points."""
    return round(
        math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2),
        2
    ) * distance_mult

def generate_node_props():
    return {
        "population": randrange(1_000, 1_000_000, 1_000),
        "name": generate_city_name()
    }

def calc_num_extra_edges() -> int:
    """Calculate the number of extra edges to generate: 0 or `randint(10, 20)`."""
    if randint(1, 100) <= chance_extra_edges:
        return randint(min_extra_edges, max_extra_edges)
    else:
        return 0

def calc_extra_edges_coord_range(pos: int):
    """Calculate the coord range `pos-R <-> pos+R`.

    Respects the field size constraints `0 >= coord < 100`.
    The generated range is fed later into the `randint(*coord_range)`.
    """
    from_pos = pos - extra_edge_radius
    to_pos = pos + extra_edge_radius
    if from_pos < 0:
        return [0, extra_edge_radius]
    elif to_pos >= array_dim:
        return [array_dim - extra_edge_radius - 1, array_dim - 1]
    else:
        return [from_pos, to_pos]

def generate_sample_data():
    nodes = [
        [Node(props=generate_node_props()) for x in range(0, array_dim)]
        for y in range(0, array_dim)
    ]
    graph = Graph()

    for y in range(0, array_dim):
        for x in range(0, array_dim):
            """Add nodes and generate the v/h edges."""
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

    for y in range(0, array_dim):
        for x in range(0, array_dim):
            """Occasionaly generate extra edges."""
            num_extra_edges = calc_num_extra_edges()
            extra_edges_x_range = calc_extra_edges_coord_range(x)
            extra_edges_y_range = calc_extra_edges_coord_range(y)
            for _ in range(0, num_extra_edges):
                extra_x = randint(*extra_edges_x_range)
                extra_y = randint(*extra_edges_y_range)
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

if __name__ == "__main__":
    import os

    print(f"Generating a sample graph for {num_nodes} nodes...")
    g = generate_sample_data()

    filename = "sample_data.graph"
    print(f"Done. Writing to the {os.getcwd()}/{filename}...")
    with open(filename, "w", encoding="utf-8") as file:
        for line in g.serialize():
            file.writelines(line + "\n")

    print(f"The {filename} saved.")
