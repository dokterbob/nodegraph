import unittest

from .mixins import (
    TrivialPathTestMixin, DualPathTestMixin, ComplexPathTestMixin
)


class TestTrivialPath(TrivialPathTestMixin, unittest.TestCase):
    """ Tests for a Path with single Edge. """

    def test_init(self):
        """
        Test initial conditions for created Path.
        """

        # The weight should be 0.0 for a Path containing Edges without scores
        self.assertEqual(self.p.get_weight(), 0.0)

    def test_weight_simple(self):
        """
        Increase the score for Edge and ascertain result in path weight.
        """
        self.e.increase_score()
        self.assertEquals(self.e.get_weight(), 1.0)

        self.assertEqual(self.p.get_weight(), 1.0)

    def test_weight_cache(self):
        """ Test caching for get_weight(). """

        # Set some cache value
        self.e.ttl = 5

        # Test ttl
        self.assertEquals(self.p.get_ttl(), 5)

        # Populate the cache
        self.assertAlmostEquals(self.p.get_weight(), 0.0)

        # Test cache
        self.assertEquals(self.g.store.cache.get((self.p, 'weight')), 0.0)
        self.assertTrue(self.g.store.cache.get_expires((self.p, 'weight')))

        # With score increased, weight should be 1.0 - but 0.0 still in cache
        self.e.increase_score()

        # Cache should not have changed
        self.assertEquals(self.g.store.cache.get((self.p, 'weight')), 0.0)
        self.assertTrue(self.g.store.cache.get_expires((self.p, 'weight')))

        self.assertAlmostEqual(self.p.get_weight(), 0.0)

        # Flush cache
        self.g.store.cache.flush()

        # New value propagated!
        self.assertAlmostEqual(self.p.get_weight(), 1.0)


class TestDualPath(DualPathTestMixin, unittest.TestCase):
    """ Tests for a Path with two Edges. """

    def test_weight_initial(self):
        """ Test initial weight. """

        # Initial weight should be 0.0
        self.assertEqual(self.p2.get_weight(), 0.0)

    def test_weight_one_score(self):
        """ Test weight when one Edge has a nonzero score. """

        # Score for e, should get e.get_weight() -> 1.0
        self.e.increase_score()

        # Path weight should still be 0.0
        self.assertEqual(self.p2.get_weight(), 0.0)

    def test_weight_two_score(self):
        """ Test weight when both Edges have maximal score. """

        self.e.increase_score()
        self.e2.increase_score()

        # Path weight should still be equal to 1.0*1.0*dampening
        self.assertEqual(self.p2.get_weight(), self.p2.dampening)


class TestComplexPath(ComplexPathTestMixin, unittest.TestCase):
    """ Test behaviour of complex paths (with more than two Edges). """

    def test_weight_initial(self):
        """ Test initial weight. """

        # Initial weight should be 0.0
        self.assertEqual(self.p3.get_weight(), 0.0)

    def test_weight_three_score(self):
        """ Test weight when both Edges have maximal score. """

        self.e.increase_score()
        self.e2.increase_score()
        self.e3.increase_score()

        # Path weight should still be equal to 1.0*1.0*1.0*dampening^2
        self.assertAlmostEqual(self.p3.get_weight(), self.p3.dampening**2)


if __name__ == '__main__':
    unittest.main()
