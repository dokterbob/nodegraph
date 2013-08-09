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


class PathTestMixin(EdgeTestMixin):
    """ Mixin for tests depending on a Path `self.p` to be available. """

    def setUp(self):
        super(PathTestMixin, self).setUp()

        self.p = Path(edges=[self.e])
