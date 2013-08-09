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

    def __init__(self, graph_name):
        # Graph TTL container
        self.graph_name = graph_name

        # Set initial ttl to 0
        self.graph_ttl = 0

        # Create empty set for storage of nodes
        self.nodes = set()

        # Create a dictionary (Node -> ttl) for storing node ttl's
        self.node_ttl = {}

        # Create emtpy set for storage of edges
        self.edges = set()

        # Create empty dictionery (Edge -> ttl_ for storing edge ttl's
        self.edge_ttl = {}

        # Create empty set for storage of paths
        self.paths = set()

        # Create a dictionary for storing edge -> score pairs
        self.scores = {}
