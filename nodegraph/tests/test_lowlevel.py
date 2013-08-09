import unittest

from ..lowlevel import Graph, Node, Edge

from .mixins import GraphTestMixin, NodeTestMixin, EdgeTestMixin


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

    def test_hash(self):
        """ Test hashing for Node / equivalence of duplicates. """
        same_node = Node(graph=self.g, name=self.n.name)
        other_node = Node(graph=self.g, name='other_node')

        # Node objects equality
        self.assertEquals(same_node, self.n)
        self.assertNotEquals(other_node.key(), self.n.key())

        # Key equality
        self.assertEquals(same_node.key(), self.n.key())
        self.assertNotEquals(other_node.key(), self.n.key())

        # Hash equality
        self.assertEquals(hash(same_node), hash(self.n))
        self.assertNotEquals(hash(other_node), hash(self.n))

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

        # Increase score to make life more interesting
        self.e.increase_score()

        duplicate_edge = Edge(from_node=self.n, to_node=self.n2)

        # Assert equality
        self.assertEquals(self.e, duplicate_edge)

        # Assert the scores remain up to date
        self.assertEquals(duplicate_edge.score, 100)

        duplicate_edge.increase_score()
        self.assertEquals(self.e.score, 200)

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

    def test_weight(self):
        """ Test weight for Graph with single Edge. """

        # Initially, no score has been assigned - hence no weight.
        self.assertAlmostEqual(self.e.weight, 0.0)

        # With score increased, weight should be 1.0
        self.e.increase_score()
        self.assertAlmostEqual(self.e.weight, 1.0)

    def test_multiweight(self):
        """ Test weight distribution for multiple Edges from `self.n`. """

        self.e.increase_score()
        self.assertEqual(self.e.score, 100)

        n3 = Node(graph=self.g, name='node_3')
        e2 = Edge(self.n, n3)
        e2.increase_score()
        self.assertEqual(e2.score, 100)

        # Total score
        self.assertEquals(self.n.get_total_score(), 200)

        # Equal weight distribution
        self.assertAlmostEqual(self.e.weight, 0.5)
        self.assertAlmostEqual(e2.weight, 0.5)

    def test_multiweight_unequal(self):
        """
        Test unequal weight distribution for multiple Edges from `self.n`.
        """
        # Start from situation above
        n3 = Node(graph=self.g, name='node_3')
        e2 = Edge(self.n, n3)
        e2.increase_score()
        self.assertEqual(e2.score, 100)

        # Unequal weight distribution
        self.e.increase_score(200)
        self.assertEqual(self.e.score, 200)

        # Total score
        self.assertEquals(self.n.get_total_score(), 300)

        # 2/3 for self.e - 1/3 for e2
        self.assertAlmostEqual(self.e.weight, 0.66666666)
        self.assertAlmostEqual(e2.weight, 0.33333333)


if __name__ == '__main__':
    unittest.main()
