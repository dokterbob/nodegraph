from .cache import GraphCache


class GraphStore(object):
    """
    Store for Graph data; Edges (scores) and Nodes are stored here.

    The idea is to be able to have pluggable storage backends with the default
    (for now) being an in-memory store.

    store = GraphStore(name=...)
    store.edges = ...
    store.nodes = ...
    store.scores[node] = ...
    """

    def __init__(self, name):
        # Graph TTL container
        self.name = name

        # Set initial ttl to 0
        self.graph_ttl = 0

        # Set initial graph dampening to 0
        self.path_dampening = 0.90

        # Set initial recursion weight cutoff for ensembles
        self.ensemble_weight_cutoff = 0.10

        # Create empty set for storage of nodes
        self.nodes = set()

        # Create a dictionary (Node -> ttl) for storing node ttl's
        self.node_ttl = {}

        # Create emtpy set for storage of edges
        self.edges = set()

        # Create empty dictionery (Edge -> ttl_ for storing edge ttl's
        self.edge_ttl = {}

        # Create a dictionary for storing Edge -> score pairs
        self.edge_score = {}

        # Key-value cache
        self.cache = GraphCache()

    def key(self):
        """ Key used for hashing and comparisons. """
        return self.name

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())
