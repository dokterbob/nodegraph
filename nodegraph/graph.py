from .managers import EdgeManager, NodeManager, PathManager, EnsembleManager

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
        self.ensembles = EnsembleManager(graph=self)

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
    def path_dampening(self):
        """
        Path dampening storage wrapper.
        """
        return self.store.path_dampening

    @path_dampening.setter
    def path_dampening(self, value):
        assert isinstance(value, int)

        self.store.path_dampening = value

    @property
    def ensemble_weight_cutoff(self):
        """
        Recursion weight cutoff for ensembles.
        """
        return self.store.ensemble_weight_cutoff

    @ensemble_weight_cutoff.setter
    def ensemble_weight_cutoff(self, value):
        assert isinstance(value, float)

        self.store.ensemble_weight_cutoff = value

    @property
    def ensemble_max_recursion(self):
        """
        Maximum iteration depth for ensemble recursion.
        """
        return self.store.ensemble_max_recursion

    @ensemble_max_recursion.setter
    def ensemble_max_recursion(self, value):
        assert isinstance(value, int)

        self.store.ensemble_max_recursion = value

    @property
    def name(self):
        """
        Graph name storage wrapper
        """
        return self._name
