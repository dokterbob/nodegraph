from .managers import EdgeManager, NodeManager, PathManager

from .store import GraphStore


class Graph(object):
    """
    Named container for graph objects.

    The information in this backend is lost as soon as the process dies.
    """

    def __init__(self, name, store=None):
        # Set (read-only) Graph name
        assert isinstance(name, basestring)
        self._name = name

        # Initialize the store, passing the (immutable) graph name
        if not store:
            self.store = GraphStore(name=self.name)

        assert isinstance(self.store, GraphStore)

        # Initialize managers
        self.edges = EdgeManager(graph=self)
        self.nodes = NodeManager(graph=self)
        self.paths = PathManager(graph=self)

    def key(self):
        """ Key used for hashing and comparisons. """
        return self.name

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())

    @property
    def ttl(self):
        """
        Graph ttl storage wrapper.
        """
        return self.store.graph_ttl

    @ttl.setter
    def ttl(self, value):
        assert isinstance(value, int)

        self.store.graph_ttl = value

    @property
    def name(self):
        """
        Graph name storage wrapper
        """
        return self._name


class Node(object):
    """
    Named node in a graph.
    """

    def __init__(self, graph, name):
        # Set name
        assert isinstance(name, basestring)
        self.name = name

        # Associate with graph
        assert isinstance(graph, Graph)
        self.graph = graph

        # Add oneself to graph
        self.graph.nodes.add(self)

    def key(self):
        """ Key used for hashing and comparisons. """
        return (self.graph.key(), self.name)

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())

    @property
    def ttl(self):
        """
        Node ttl storage wrapper, returns explicitly set ttl or graph default.
        """
        return self.graph.store.node_ttl.get(self, self.graph.ttl)

    @ttl.setter
    def ttl(self, value):
        assert isinstance(value, int)

        self.graph.store.node_ttl[self] = value

    @ttl.deleter
    def ttl(self):
        del self.graph.store.node_ttl[self]

    def get_total_score(self):
        """ Total score of all edges starting at this node. """

        edges = self.graph.edges.from_node(self)

        total_score = 0
        for edge in edges:
            total_score += edge.score

        return total_score


class Edge(object):
    """
    Weighed connection between two Nodes with implicit weight derived from
    score which can only be increased or decreased.
    """

    def __init__(self, from_node, to_node):
        # Initialize properties
        assert isinstance(from_node, Node)
        assert isinstance(to_node, Node)
        self.from_node = from_node
        self.to_node = to_node

        # Set graph
        assert self.from_node.graph == self.to_node.graph
        self.graph = self.from_node.graph

        # Add oneself to graph
        self.graph.edges.add(self)

    def increase_score(self, amount=100):
        """ Increase the score with the given amount. """
        self.score += amount

    def decrease_score(self, amount=100):
        """ Decrease the score with the given amount - but never less than 0. """

        if amount > self.score:
            self.score = 0
        else:
            self.score -= amount

    def key(self):
        """ Key used for hashing and comparisons. """
        return (self.from_node.key(), self.to_node.key())

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())

    @property
    def ttl(self):
        """
        Edge ttl property wrapper. Returns minimum ttl of nodes as default.
        """
        return self.graph.store.edge_ttl.get(self,
            min(self.from_node.ttl, self.to_node.ttl)
        )

    @ttl.setter
    def ttl(self, value):
        assert isinstance(value, int)

        self.graph.store.edge_ttl[self] = value

    @property
    def score(self):
        """ Score storage wrapper. """
        return self.graph.store.scores.get(self, 0)

    @score.setter
    def score(self, value):
        assert isinstance(value, int)

        self.graph.store.scores[self] = value

    @score.deleter
    def score(self):
        del self.graph.store.scores[self]

    @property
    def weight(self):
        """ Return the current weight. """

        # No score, no weight: simple optimizations, prevents division by zero
        if not self.score:
            return 0.0

        total_score = self.from_node.get_total_score()
        assert total_score

        weight = self.score / float(total_score)

        return weight
