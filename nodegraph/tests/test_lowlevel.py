import unittest

from ..lowlevel import Graph


class TestGraph(unittest.TestCase):
    def test_init(self):
        """ Test creating a graph. """
        g = Graph(name='test_graph')
        self.assertTrue(hasattr(g, 'edges'))
        self.assertTrue(hasattr(g, 'nodes'))


if __name__ == '__main__':
    unittest.main()
