class ObjectNotFound(Exception):
    """ Base exception for queries returning no result. """

    object_type = 'Object'

    def __init__(self, **args):
        self.args = args

    def __unicode__(self):
        attribute_list = [u'%s=%s' % (arg.key, arg.value) for arg in self.args]
        attributes = u', '.join(attribute_list)

        return u'%s not found with query attributes %s' % (
            self.object_type, attributes
        )


class NodeNotFound(ObjectNotFound):
    """ Exception raised when a queried node could not be found. """
    object_type = 'Node'


class EdgeNotFound(ObjectNotFound):
    """ Exception raised when a queried edge could not be found. """
    object_type = 'Edge'
