from .exceptions import NodeNotFound, EdgeNotFound

from .highlevel import Path, Ensemble
from .lowlevel import Node, Edge


class NodeManager(object):
    """ Manager for Nodes in a Graph. """

    def __init__(self, graph):
        self.graph = graph

        # Shorthand for storage
        self._nodes = graph.store.nodes

    def create(self, name):
        """ Create a Node and add it to the graph. Returns Node. """

        node = Node(graph=self.graph, name=name)

        self._nodes.add(node)

        return node

    def all(self):
        """ Return all nodes in the current graph. """
        return self._nodes

    def remove(self, node):
        """ Remove a Npde from the Graph. """
        # isinstance(node, Node)

        self._nodes.remove(node)

    def get(self, name):
        """ Get a single node by name. """
        for node in self._nodes:
            if node.name == name:
                return node

        # Not found, raise exception
        raise NodeNotFound(name=name)

    def linked_to(self, node):
        """ Return all nodes linked to node. """
        edges = self.graph.edges.to_node(node)
        nodes = [edge.node_from for edge in edges]

        return nodes

    def linked_from(self, node):
        """ Return all nodes linked from node. """
        edges = self.graph.edges.from_node(node)
        nodes = [edge.node_to for edge in edges]

        return nodes


class EdgeManager(object):
    """ Manager for Edges in a Graph. """

    def __init__(self, graph):
        self.graph = graph

        # Shorthand for storage
        self._edges = graph.store.edges

    def all(self):
        """ Return edges in the current graph. """
        return self._edges

    def create(self, from_node, to_node):
        """ Create an Edge and add it to the Graph. Returns Edge. """

        edge = Edge(graph=self.graph, from_node=from_node, to_node=to_node)

        # Add oneself to graph
        self._edges.add(edge)

        return edge

    def remove(self, edge):
        """ Remove an Edge from the Graph. """
        # assert isinstance(edge, Edge)

        self._edges.remove(edge)

    def to_node(self, node):
        """ Return set of edges ending at node. """
        edges = set()

        for edge in self._edges:
            if edge.to_node == node:
                edges.add(edge)

        return edges

    def from_node(self, node):
        """ Return set of edges starting at node. """
        edges = set()

        for edge in self._edges:
            if edge.from_node == node:
                edges.add(edge)

        return edges

    def get(self, from_node, to_node):
        """ Return the edge linking two nodes. """

        from_nodes = self.from_node(from_node)
        to_nodes = self.to_node(to_node)

        edges = from_nodes.intersection(to_nodes)

        if not edges:
            raise EdgeNotFound(from_node=from_node, to_node=to_node)

        # There can only ever be one edge connecting two nodes
        assert len(edges) == 1

        return edges.pop()


class PathManager(object):
    """ Manager for Paths in a Graph. """

    def __init__(self, graph):
        self.graph = graph


class EnsembleManager(object):
    """ Manager for Ensembles in a Graph. """

    def __init__(self, graph):
        self.graph = graph

    def get(self, from_node, to_node, prepend_path=None):
        """ Return the Ensemble of paths from from_node tot to_node. """

        paths = set()

        for edge in self.graph.edges.from_node(from_node):
            if prepend_path:
                new_path = Path(prepend_path.edges + [edge])
            else:
                new_path = Path([edge])

            # Only process when the initial Edge has weight
            if new_path.get_weight() > self.graph.ensemble_weight_cutoff:

                if new_path.to_node is to_node:
                    # This is a direct connection, create and add Path
                    paths.add(new_path)

                # Recurse further
                if len(new_path.edges) <= self.graph.ensemble_max_recursion:
                    ensemble = self.get(new_path.to_node, to_node, new_path)

                    # Create non-trivial paths
                    for path in ensemble.paths:
                        paths.add(path)

        return Ensemble(paths)
