import unittest

from ..lowlevel import Graph, Node, Edge


class GraphTestMixin(object):
    """ Mixin for tests depending on a Graph `self.g` to be available. """

    def setUp(self):
        super(GraphTestMixin, self).setUp()

        self.g = Graph(name='test_graph')


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


class TestGraph(GraphTestMixin, unittest.TestCase):
    """ Tests for Graph. """

    def test_init(self):
        """ Test created Graph. """
        # Assert no edges or nodes are present
        self.assertFalse(self.g.edges.all())
        self.assertFalse(self.g.nodes.all())

    def test_duplicate(self):
        """ Graphs with the same name should be identical and vice versa. """
        duplicate_graph = Graph(name=self.g.name)

        self.assertEquals(self.g, duplicate_graph)

        new_graph = Graph(name='new_graph')

        self.assertNotEquals(self.g, new_graph)


class TestNode(NodeTestMixin, unittest.TestCase):
    """ Tests for Node. """

    def test_init(self):
        """ Test created Node. """
        self.assertEquals(set([self.n]), self.g.nodes.all())
        self.assertEquals(set([]), self.g.edges.all())

    def test_get_total_score(self):
        """ Test getting the total score for single node. """

        # Initial total score for trivial graph (single Node) is 0
        self.assertEquals(self.n.get_total_score(), 0)

    def test_duplicate(self):
        """ Nodes with the same name should be identical and vice versa.. """
        duplicate_node = Node(graph=self.n.graph, name=self.n.name)

        # Assert equality
        self.assertEquals(self.n, duplicate_node)

        # Nothing should have changed in the graph from inital state
        self.test_init()

        new_node = Node(graph=self.n.graph, name='new_node')

        # Assert inequality
        self.assertNotEquals(self.n, new_node)

        # Should have been added to the Graph
        self.assertEquals(set([self.n, new_node]), self.g.nodes.all())

    def test_twographs(self):
        """ Test that two graphs do not interfere. """

        new_graph = Graph(name='new_graph')

        # Should be empty
        self.assertEquals(set(), new_graph.nodes.all())
        self.assertEquals(set(), new_graph.edges.all())

        # Old graph has not changed
        self.test_init()


class TestEdge(EdgeTestMixin, unittest.TestCase):
    """ Tests for Edge. """

    def test_init(self):
        """ Test created Edge. """
        self.assertEquals(set([self.n, self.n2]), self.g.nodes.all())
        self.assertEquals(set([self.e]), self.g.edges.all())

    def test_duplicate(self):
        """ Edges with same two nodes should be identical and vice versa. """
        duplicate_edge = Edge(from_node=self.n, to_node=self.n2)

        # Assert equality
        self.assertEquals(self.e, duplicate_edge)

        # Assert nothing has changed
        self.test_init()

    def test_twographs(self):
        """ Test that two graphs do not interfere. """

        new_graph = Graph(name='new_graph')

        # Should be empty
        self.assertEquals(set(), new_graph.nodes.all())
        self.assertEquals(set(), new_graph.edges.all())

        # Old graph has not changed
        self.test_init()

    def test_increase_score(self):
        """ Test increasing the score. """
        self.assertEquals(self.e.score, 0)

        # Increase by 100 (default)
        self.e.increase_score()

        self.assertEquals(self.e.score, 100)

        # Increase by another 10
        self.e.increase_score(10)

        self.assertEquals(self.e.score, 110)

    def test_decrease_score(self):
        # Increase score to 110 by repeating test above
        self.test_increase_score()

        # Decrease with 100 (default)
        self.e.decrease_score()
        self.assertEquals(self.e.score, 10)

        # Decrease by another 5
        self.e.decrease_score(5)
        self.assertEquals(self.e.score, 5)

        # Assert that decreasing it again with 100 does not go below 0
        self.e.decrease_score()
        self.assertEquals(self.e.score, 0)


if __name__ == '__main__':
    unittest.main()
