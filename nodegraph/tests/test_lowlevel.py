import unittest

from ..lowlevel import Graph, Node, Edge


class TestGraph(unittest.TestCase):
    """ Tests for Graph. """

    def test_init(self):
        """ Test creating a Graph. """
        g = Graph(name='test_graph')
        self.assertTrue(hasattr(g, 'edges'))
        self.assertTrue(hasattr(g, 'nodes'))


class GraphTestMixin(object):
    """ Mixin for tests depending on a Graph `self.g` to be available. """

    def setUp(self):
        self.g = Graph(name='test_graph')

        super(GraphTestMixin, self).setUp()


class TestNode(GraphTestMixin, unittest.TestCase):
    """ Tests for Node. """

    def test_init(self):
        """ Test creating a Node. """

        n = Node(graph=self.g, name='test_node')

        self.assertIn(n, self.g.nodes.all())

    def test_get_total_score(self):
        """ Test getting the total score for single node. """

        n = Node(graph=self.g, name='test_node')
        self.assertEquals(n.get_total_score(), 0)


# class TestEdge(GraphTestMixin, unittest.TestCase):
#     def test_init(self):
#         """ Test creating an Edge. """

#         e = Edge(graph=self.g)

if __name__ == '__main__':
    unittest.main()
