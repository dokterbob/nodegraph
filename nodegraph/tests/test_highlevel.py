import unittest

from .mixins import (
    TrivialPathTestMixin, DualPathTestMixin, ComplexPathTestMixin,
    EnsembleTestMixin
)

from ..highlevel import Path


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
        self.assertEqual(self.p2.get_weight(), self.g.path_dampening)


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
        self.assertAlmostEqual(self.p3.get_weight(), self.g.path_dampening**2)

    def test_weight_unequal_score(self):
        """
        Test weight with one Edge 'forking' the Path.

        self.p3:      [ <self.n> -> <self.n2> -> <self.n3> ]
        forking_path: [ <self.n> -> <forking_node> ]
        """
        forking_node = self.g.nodes.create(name='forking_node')
        forking_edge = self.g.edges.create(
            from_node=self.n, to_node=forking_node
        )
        forking_path = Path([forking_edge])

        # In the fork, have 1/3 of the weight go to the forking edge
        forking_edge.increase_score()

        self.e.increase_score()
        self.e.increase_score()

        self.e2.increase_score()
        self.e3.increase_score()

        # Assert Edge weights
        self.assertAlmostEqual(
            self.e.get_weight(), 2.0/3
        )
        self.assertAlmostEqual(
            forking_edge.get_weight(), 1.0/3
        )
        self.assertAlmostEqual(
            self.e2.get_weight(), 1.0
        )
        self.assertAlmostEqual(
            self.e3.get_weight(), 1.0
        )

        # Assert Path weights
        self.assertAlmostEqual(
            self.p3.get_weight(), self.g.path_dampening**2 * 2.0/3
        )

        self.assertAlmostEqual(
            forking_path.get_weight(), 1.0/3
        )


class TestEnsemble(EnsembleTestMixin, unittest.TestCase):
    """ Test Ensemble weight. """

    def test_weight_initial(self):
        """ Test initial weight. """

        # Initial weight should be 0.0
        self.assertEqual(self.es.get_weight(), 0.0)

    def test_weight_simple(self):
        """
        Increase the score for Edge and ascertain result in path weight.
        """
        self.e.increase_score()

        self.assertEquals(self.es.get_weight(), 1.0)
        self.assertEquals(self.es.get_weight(), self.p.get_weight())

    def test_weight_sum(self):
        """
        Test a composite weight of a collection of paths.
        """
        self.e.increase_score(10)
        self.e2.increase_score(5)
        self.e3.increase_score(15)

        self.assertEquals(self.es.get_weight(), self.p.get_weight())

        self.assertEquals(self.es2.get_weight(),
            self.p2.get_weight() + self.p3.get_weight()
        )

    def test_weight_cache(self):
        """ Test caching for get_weight(). """

        # Set some cache value
        self.e.ttl = 5
        self.e2.ttl = 5

        # Test ttl
        self.assertEquals(self.es.get_ttl(), 5)

        # Populate the cache
        self.assertAlmostEquals(self.es.get_weight(), 0.0)

        # Test cache
        self.assertEquals(self.g.store.cache.get((self.es, 'weight')), 0.0)
        self.assertTrue(self.g.store.cache.get_expires((self.es, 'weight')))

        # With score increased, weight should be 1.0 - but 0.0 still in cache
        self.e.increase_score()

        # Cache should not have changed
        self.assertEquals(self.g.store.cache.get((self.es, 'weight')), 0.0)
        self.assertTrue(self.g.store.cache.get_expires((self.es, 'weight')))

        self.assertAlmostEqual(self.es.get_weight(), 0.0)

        # Flush cache
        self.g.store.cache.flush()

        # New value propagated!
        self.assertAlmostEqual(self.es.get_weight(), 1.0)


class TestEnsembleManager(EnsembleTestMixin, unittest.TestCase):
    """ Test Ensemble Manager methods. """

    def test_get_none(self):
        """ Without score, no paths should be returned. """

        ensemble = self.g.ensembles.get(self.n, self.n2)

        self.assertEquals(ensemble.paths, set())

    def test_get_single(self):
        """ Test get() for trivial Path. """

        self.e.increase_score()

        ensemble = self.g.ensembles.get(self.n, self.n2)

        self.assertEquals(
            ensemble.paths, set([self.p])
        )
        self.assertEquals(ensemble, self.es)

    def test_get_two(self):
        """ Test get() for degenerate Path (multiple routes). """

        self.e.increase_score()
        self.e2.increase_score()
        self.e3.increase_score()

        ensemble = self.g.ensembles.get(self.n, self.n3)

        self.assertEquals(
            ensemble.paths, set([self.p2, self.p3])
        )
        self.assertEquals(ensemble, self.es2)

    def test_recursion_cutoff(self):
        """ Test whether recursion is appropriately prevented. """

        self.e4 = self.g.edges.create(self.n2, self.n)

        self.e.increase_score()
        self.e4.increase_score()

        ensemble = self.g.ensembles.get(self.n, self.n2)

        # Note: there is an asymptote here around 5.2631578947324655
        self.assertAlmostEqual(ensemble.get_weight(), 5.3, places=1)

    def test_max_recursion(self):
        """ Test maximum recursion cutoff. """

        self.e4 = self.g.edges.create(self.n2, self.n)

        self.e.increase_score()
        self.e4.increase_score()

        # Test results at maximum depth
        self.g.ensemble_max_recursion = 40

        ensemble = self.g.ensembles.get(self.n, self.n2)

        self.assertAlmostEqual(ensemble.get_weight(), 5.2, places=1)


if __name__ == '__main__':
    unittest.main()
