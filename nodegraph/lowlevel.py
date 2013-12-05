import sys


class Node(object):
    """
    Named node in a graph.
    """

    def __init__(self, graph, name):
        # Set name
        assert isinstance(name, basestring)
        self.name = name

        # Associate with graph
        self.graph = graph

    def key(self):
        """ Key used for hashing and comparisons. """
        return (self.graph.key(), self.name)

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        return '<Node {0}>'.format(self.name)

    @property
    def ttl(self):
        """
        Node ttl storage wrapper, returns explicitly set ttl or graph default.
        """
        return self.graph.store.node_ttl.get(self, self.graph.ttl)

    @ttl.setter
    def ttl(self, value):
        assert isinstance(value, int)

        self.graph.store.node_ttl[self] = value

    @ttl.deleter
    def ttl(self):
        del self.graph.store.node_ttl[self]

    def get_min_ttl_out(self):
        """
        Get the minimal ttl of all Edges pointing outward from this Node or
        the Node's ttl if no Edges are available.
        """

        # Nice hashable tuple of self and 'score' identifier
        cache_key = (self, 'min_ttl_out')

        # Hit cache
        cached = self.graph.store.cache.get(cache_key)
        if cached is not None:
            return cached

        # No cache available -> calculate!
        edges = self.graph.edges.from_node(self)

        if edges:
            # Calculate minimal Edge ttl and total Edge score
            min_ttl = sys.maxint
            for edge in edges:
                if edge.ttl < min_ttl:
                    min_ttl = edge.ttl

            assert min_ttl != sys.maxint

            # Write to cache, using self.ttl as cache time
            self.graph.store.cache.set(cache_key, min_ttl, self.ttl)

        else:
            # No Edges available to calculate score; use Node's ttl in which
            # case caching is useless.
            min_ttl = self.ttl

        return min_ttl

    def get_score_out(self):
        """ Total score of all Edges pointing outward form this Node. """

        # Nice hashable tuple of self and 'score' identifier
        cache_key = (self, 'score_out')

        # Hit cache
        cached = self.graph.store.cache.get(cache_key)
        if cached:
            return cached

        # No cache available -> calculate!
        edges = self.graph.edges.from_node(self)

        total_score = 0

        # Total Edge score
        for edge in edges:
            total_score += edge.score

        # Get minimal ttl of outgoing Edges
        ttl = self.get_min_ttl_out()

        # Write to cache
        self.graph.store.cache.set(cache_key, total_score, ttl)

        return total_score


class Edge(object):
    """
    Weighed connection between two Nodes with implicit weight derived from
    score which can only be increased or decreased.
    """

    def __init__(self, graph, from_node, to_node):
        # Initialize properties
        assert isinstance(from_node, Node)
        assert isinstance(to_node, Node)
        assert from_node is not to_node, 'From node to node are the same.'
        assert from_node.graph == graph
        assert to_node.graph == graph

        self.graph = graph
        self.from_node = from_node
        self.to_node = to_node

    def increase_score(self, amount=100):
        """ Increase the score with the given amount. """
        self.score += amount

    def decrease_score(self, amount=100):
        """ Decrease the score with the given amount - but never less than 0. """

        if amount > self.score:
            self.score = 0
        else:
            self.score -= amount

    def key(self):
        """ Key used for hashing and comparisons. """
        return (self.from_node.key(), self.to_node.key())

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        return "<Edge {0}, {1}>".format(
            self.from_node.name, self.to_node.name
        )

    @property
    def ttl(self):
        """
        Edge ttl property wrapper. Returns minimum ttl of nodes as default.
        """
        return self.graph.store.edge_ttl.get(self,
            min(self.from_node.ttl, self.to_node.ttl)
        )

    @ttl.setter
    def ttl(self, value):
        assert isinstance(value, int)

        self.graph.store.edge_ttl[self] = value

    @property
    def score(self):
        """ Score storage wrapper. """
        return self.graph.store.edge_score.get(self, 0)

    @score.setter
    def score(self, value):
        assert isinstance(value, int)

        self.graph.store.edge_score[self] = value

    @score.deleter
    def score(self):
        del self.graph.store.edge_score[self]

    def get_weight(self):
        """ Return the current weight. """

        # Nice hashable tuple of self and identifier
        cache_key = (self, 'weight')

        # Hit cache
        cached = self.graph.store.cache.get(cache_key)
        if cached is not None:
            return cached

        # No score, no weight: simple optimizations, prevents division by zero
        if self.score:
            total_score = self.from_node.get_score_out()
            assert total_score

            weight = self.score / float(total_score)
        else:
            weight = 0.0

        # Get minimal outgoing ttl for Edges
        ttl = self.from_node.get_min_ttl_out()

        # Write to cache
        self.graph.store.cache.set(cache_key, weight, ttl)

        return weight
