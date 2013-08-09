from .lowlevel import Edge


class Path(object):
    """
    Ordered collection of Edges with compound weight as product of Edge weight.
    """

    def __init__(self, edges=[]):
        # This is equivalent to the assert statement, see:
        # http://docs.python.org/2/reference/simple_stmts.html#the-assert-statement
        if __debug__:
            for edge in edges:
                # They should all be edges
                if not isinstance(edge, Edge):
                    raise AssertionError

                # All should have same graph
                if not edge.graph == edges[0].graph:
                    raise AssertionError

        # Store Edges on object
        self.edges = edges

        # Set graph
        self.graph = edges[0].graph

        self.graph.paths.add(self)

    def key(self):
        """ Key used for hashing and comparisons. """
        keys = [edge.key() for edge in self.edges]

        return tuple(keys)

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())


class Ensemble(object):
    """
    Collection of Paths between two Nodes with compound weight as sum of path
    weights.
    """

    def __init__(self, paths=set()):
        # This is equivalent to the assert statement, see:
        # http://docs.python.org/2/reference/simple_stmts.html#the-assert-statement
        if __debug__:
            for path in paths:
                if not isinstance(path, Path):
                    raise AssertionError

        self.paths = paths

    def key(self):
        """ Key used for hashing and comparisons. """
        keys = [path.key() for path in path.edges]

        return tuple(keys)

    def __eq__(x, y):
        return x.key() == y.key()

    def __hash__(self):
        return hash(self.key())
