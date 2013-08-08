from .managers import EdgeManager, NodeManager


class Graph(object):
    """
    Named container for graph objects.

    The information in this backend is lost as soon as the process dies.
    """

    def __init__(self, name):
        self.name = name
        self.edges = EdgeManager(graph=self)
        self.nodes = NodeManager(graph=self)


class Node(object):
    """
    Named node in a graph.
    """

    def __init__(self, graph, name):
        assert isinstance(graph, Graph)
        self.graph = graph

        self.name = name

    def get_total_score(self):
        """ Total score of all edges starting at this node. """

        edges = self.graph.edges.from_node(self)

        total_score = 0
        for edge in edges:
            total_score += edge.score

        return total_score


class Edge(object):
    """
    Weighed connection between two Nodes with implicit weight derived from
    score which can only be increased or decreased.
    """

    def __init__(self, from_node, to_node):
        assert isinstance(from_node, Node)
        assert isinstance(to_node, Node)
        self.from_node = from_node
        self.to_node = to_node

        # Initialize score
        self._score = 0

    def increase_score(self, amount=100):
        """ Increase the score with the given amount. """
        self._score += amount

    def decrease_score(self, amount=100):
        """ Decrease the score with the given amount. """
        self._score -= amount

    @property
    def score(self):
        """ Return the current score. """
        return self._score

    @property
    def weight(self):
        """ Return the current weight. """
        total_score = self.from_node.get_total_score()

        assert self._score
        assert total_score

        weight = self.score / total_score

        return weight


class Path(object):
    """
    Ordered collection of Edges with compound weight as product of Edge weight.
    """

    def __init__(self, edges=[]):
        # TODO: Put this iteration into the assert statement, somehow
        for edge in edges:
            assert isinstance(edge, Edge)
        self.edges = edges


class Ensemble(object):
    """
    Collection of Paths between two Nodes with compound weight as sum of path
    weights.
    """
    def __init__(self, paths=set()):
        # TODO: Put this iteration into the assert statement, somehow
        for path in paths:
            assert isinstance(path, Path)
        self.paths = paths
