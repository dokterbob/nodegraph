from ..cache import GraphCache
from ..lowlevel import Graph, Node, Edge
from ..highlevel import Path, Ensemble


class GraphTestMixin(object):
    """ Mixin for tests depending on a Graph `self.g` to be available. """

    def setUp(self):
        super(GraphTestMixin, self).setUp()

        self.g = Graph(name='test_graph')


class CacheTestMixin(GraphTestMixin):
    """ Mixin using a mock time `self.time` for testing the cache. """
    def setUp(self):
        super(CacheTestMixin, self).setUp()

        # Initialize mock time
        self.time = 0

        def mock_timer():
            """ Mock timer, simply returns static value `self.time`. """

            return self.time

        self.c = GraphCache(timer=mock_timer)
        self.g.store.cache = self.c


class NodeTestMixin(GraphTestMixin):
    """ Mixin for tests depending on a Node `self.n` to be available. """

    def setUp(self):
        super(NodeTestMixin, self).setUp()

        self.n = Node(graph=self.g, name='test_node')


class EdgeTestMixin(NodeTestMixin):
    """ Mixin for tests depending on an Edge `self.e` to be available. """

    def setUp(self):
        super(EdgeTestMixin, self).setUp()

        self.n2 = Node(graph=self.g, name='test_node_2')
        self.e = Edge(from_node=self.n, to_node=self.n2)


class TrivialPathTestMixin(EdgeTestMixin):
    """ Mixin for tests depending on a Path `self.p` to be available. """

    def setUp(self):
        super(TrivialPathTestMixin, self).setUp()

        self.p = Path(edges=[self.e])


class DualPathTestMixin(TrivialPathTestMixin):
    """
    Mixin for tests depending on a Path `self.p2` with a second Edge `self.e2`.
    """

    def setUp(self):
        super(DualPathTestMixin, self).setUp()

        self.n3 = Node(graph=self.g, name='test_node_3')
        self.e2 = Edge(from_node=self.n2, to_node=self.n3)

        self.p2 = Path(edges=[self.e, self.e2])


class ComplexPathTestMixin(DualPathTestMixin):
    """
    Mixin for tests depending on (at least) a Path `self.p3` with a third Edge
    `self.e3`.
    """

    def setUp(self):
        super(ComplexPathTestMixin, self).setUp()

        self.n4 = Node(graph=self.g, name='test_node_4')
        self.e3 = Edge(from_node=self.n3, to_node=self.n4)

        self.p3 = Path(edges=[self.e, self.e2, self.e3])


class EnsembleTestMixin(ComplexPathTestMixin):
    """
    Mixin for tests expecting:

        * self.p -> [self.e]
        * self.p2 -> [self.e, self.e2]
        * self.p3 -> [self.e, self.e2, self.e3]
        * self.e -> [self.n, self.n2]
        * self.e2 -> [self.n2, self.n3]
        * self.e3 -> [self.n3, self.n4]

        * self.es -> [self.p]
        * self.es2 -> [self.p, self.p2]
        * self.es3 -> [self.p, self.p2, self.p3]
    """
    def setUp(self):
        super(EnsembleTestMixin, self).setUp()

        self.es = Ensemble([self.p])
        self.es2 = Ensemble([self.p, self.p2])
        self.es3 = Ensemble([self.p, self.p2, self.p3])

