import mixins
import webkit_server

class Node(webkit_server.Node, mixins.SelectionMixin, mixins.AttributeMixin) :
    pass

class NodeFactory(webkit_server.NodeFactory) :
    def create(self, node_id):
        return Node(self.client, node_id)


class Driver(webkit_server.Client, mixins.WaitMixin, mixins.HtmlParsingMixin) :
    def __init__(self, **kw):
        kw.setdefault('node_factory_class', NodeFactory)
        super(Driver, self).__init__(**kw)
