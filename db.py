"""Simple graph database.

For real app can be substituted with (Graph)DB connector.

See Also
--------
`graph.utils.sample_data` : generate and persist the sample graph
"""

from .graph.Graph import Graph
from .graph.utils import sample_data as sd

graph: Graph = None

def init():
    global graph
    graph = sd.read_from_file()
    if graph == None:
        graph = sd.generate_sample_data()
        sd.write_to_file(graph)

def db() -> Graph:
    return graph
