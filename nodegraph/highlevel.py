import sys
from .lowlevel import Edge


class Path(object):
    """
    Ordered collection of Edges with compound weight as product of Edge weight.
    """

    def __init__(self, edges=[]):
        assert len(edges) >= 1, 'Paths should contain at least two Edges.'

        # This is equivalent to the assert statement, see:
        # http://docs.python.org/2/reference/simple_stmts.html#the-assert-statement
        if __debug__:
            for edge in edges:
                # They should all be edges
                if not isinstance(edge, Edge):
                    raise AssertionError('%s is not an Edge' % edge)

                # All should have same graph
                if not edge.graph == edges[0].graph:
                    raise AssertionError('Edges on different graphs.')

        # From node and to node
        self.from_node = edges[0].from_node
        self.to_node = edges[-1].to_node

        # Store Edges on object
        self.edges = edges

        # Set graph
        self.graph = edges[0].graph

        # Set path dampening from graph
        self.dampening = self.graph.path_dampening

    def key(self):
        """ Key used for hashing and comparisons. """
        keys = [edge.key() for edge in self.edges]

        return tuple(keys)

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        return '<Path {0}>'.format(self.edges)

    def get_ttl(self):
        """
        Returns the path ttl, which is the minimum of all the path's
        Edge ttls.
        """

        min_ttl = sys.maxint

        for edge in self.edges:
            if edge.ttl < min_ttl:
                min_ttl = edge.ttl

        assert min_ttl != sys.maxint

        return min_ttl

    def get_weight(self):
        """
        Returns the weight for this path.

        This is a compound property based on the product of the weight of
        all the Path's Edges multiplied with the Graph's `path_dampening`
        factor for each Edge.
        """

        # Nice hashable tuple of self and identifier
        cache_key = (self, 'weight')

        # Hit cache
        cached = self.graph.store.cache.get(cache_key)
        if cached is not None:
            return cached

        weight = 1.0
        for edge in self.edges:
            weight *= edge.get_weight()

        # Assert a sensible value
        assert weight <= 1.0
        assert weight >= 0.0

        # Calculate dampening factor for number of steps *between* Edges
        edge_connection_count = len(self.edges) - 1
        dampening_factor = self.dampening ** edge_connection_count
        weight *= dampening_factor

        # Assert a sensible value
        assert len(self.edges) == 1 and weight < 1.0 or weight <= 1.0
        assert weight >= 0.0

        # Get minimal outgoing ttl for Edges
        ttl = self.get_ttl()

        # Write to cache
        self.graph.store.cache.set(cache_key, weight, ttl)

        return weight


class Ensemble(object):
    """
    Collection of Paths between two Nodes with compound weight as sum of path
    weights.
    """

    def __init__(self, paths=set()):
        # Set graph from first path
        for path in paths:
            self.graph = path.graph
            self.from_node = path.from_node
            self.to_node = path.to_node

            break

        # This is equivalent to the assert statement, see:
        # http://docs.python.org/2/reference/simple_stmts.html#the-assert-statement
        if __debug__:
            for path in paths:
                if not isinstance(path, Path):
                    raise AssertionError('{0} is not a Path.'.format(path))

                if not self.graph is path.graph:
                    raise AssertionError('Path is on a different Graph.')

                if not self.from_node is path.from_node:
                    raise AssertionError(
                        'From node should be the same for all Paths.'
                        'Ensemble: {0} Path: {1}'.format(
                            self.from_node, path.from_node
                        )
                    )

                if not self.to_node is path.to_node:
                    raise AssertionError(
                        'To node should be the same for all Paths.'
                        'Ensemble: {0} Path: {1}'.format(
                            self.to_node, path.to_node
                        )
                    )

        self.paths = set(paths)



    def key(self):
        """ Key used for hashing and comparisons. """
        keys = [path.key() for path in self.paths]

        return tuple(keys)

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        return '<Ensemble {0}>'.format(self.paths)

    def get_ttl(self):
        """
        Returns the Edge ttl, which is the minimum of all Path's ttl's.
        """

        min_ttl = sys.maxint

        for path in self.paths:
            ttl = path.get_ttl()

            if ttl < min_ttl:
                min_ttl = ttl

        assert min_ttl != sys.maxint

        return min_ttl

    def get_weight(self):
        """
        Returns the weight for this Ensemble.

        The weight for an Ensemble is defined as the sum of the weights of
        the Paths it consists of. As such, it is not normalized.
        """

        # Nice hashable tuple of self and identifier
        cache_key = (self, 'weight')

        # Hit cache
        cached = self.graph.store.cache.get(cache_key)
        if cached is not None:
            return cached

        weight = 0.0
        for path in self.paths:
            weight += path.get_weight()

        # Assert a sensible value
        assert weight >= 0.0

        # Get minimal outgoing ttl for Paths
        ttl = self.get_ttl()

        # Write to cache
        self.graph.store.cache.set(cache_key, weight, ttl)

        return weight
