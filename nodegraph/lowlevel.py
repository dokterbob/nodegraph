class Graph(object):
    """
    Named container for graph objects.
    """

    def __init__(self, name):
        self.name = name


class Node(object):
    """
    Named node in a graph.
    """

    def __init__(self, graph, name):
        assert isinstance(graph, Graph)
        self.graph = graph

        self.name = name


class Edge(object):
    """
    Weighed connection between two Nodes.
    """

    def __init__(self, from_node, to_node, weight=None):
        assert isinstance(from_node, Node)
        assert isinstance(to_node, Node)
        self.from_node = from_node
        self.to_node = to_node

        if weight:
            assert isinstance(weight, float)
            assert weight >= 0.0
            assert weight <= 1.0
            self.weight = weight
        else:
            weight = 0.0


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
