from .exceptions import NodeNotFound, EdgeNotFound


class NodeManager(object):
    """ wrapper for managing nodes in a graph. """

    def __init__(self, graph):
        self.graph = graph

        # Create empty set for storage of nodes
        self._nodes = set()

    def all(self):
        """ Return all nodes in the current graph. """
        return self._nodes

    def add(self, node):
        """ Add a Node to the Graph. """
        # isinstance(node, Node)

        self._nodes.add(node)

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
    """ Wrapper for managing edges in a graph. """

    def __init__(self, graph):
        self.graph = graph

        # Create emtpy set for storage of edges
        self._edges = set()

    def all(self):
        """ Return edges in the current graph. """
        return self._edges

    def add(self, edge):
        """ Add an Edge to the Graph. """
        # assert isinstance(edge, Edge)

        self._edges.add(edge)

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

        edges = from_nodes.union(to_nodes)

        if not edges:
            raise EdgeNotFound(from_node=from_node, to_node=to_node)

        assert len(edges) == 1

        return edges.pop()
