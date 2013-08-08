class GraphStore(object):
    """
    Store for Graph data; Edges (scores) and Nodes are stored here.

    The idea is to be able to have pluggable storage backends with the default
    (for now) being an in-memory store.

    store = GraphStore(graph=...)
    store.edges = ...
    store.nodes = ...
    store.scores[node] = ...
    """

    def __init__(self, graph):
        self.graph = graph

        # Create empty set for storage of nodes
        self.nodes = set()

        # Create emtpy set for storage of edges
        self.edges = set()

        # Create an ordered dictionary for storing edge -> score pairs
        self.scores = {}
