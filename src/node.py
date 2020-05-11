from pvector import *
class Node:
    def __init__(self, x, y, node_id):
        self.position = Pvector(x,y)
        self.node_id = node_id
        self.connected_nodes = list()

    def remove_connections_to_me(self):
        for obj in self.connected_nodes:
            for o in obj.connected_nodes:
                if(o.node_id == self.node_id):
                    obj.connected_nodes.remove(o)
                    break

    def add_connections_to_me(self):
        for obj in self.connected_nodes:
            foundFlag = False
            for o in obj.connected_nodes:
                if(o.node_id == self.node_id):
                    foundFlag = True
                    break                   #found id in list
            if(not foundFlag):
                obj.connected_nodes.append(self)


    def update_connections(self, new_node):
        for obj in self.connected_nodes:
            for o in obj.connected_nodes:
                if(o.node_id == self.node_id):
                    obj.connected_nodes.remove(o)
                    obj.connected_nodes.append(new_node)
                    break
        del self.connected_nodes[:]

    def remove_connected_node_with_id(self, index_to_delete):
        for obj in self.connected_nodes:
            if(obj.node_id == index_to_delete):
                self.connected_nodes.remove(obj)
                break

    def get_connections_ids(self):
        conn = list()
        for node in self.connected_nodes:
            conn.append(node.node_id)
        return conn

    def print_connections(self):
        conn = list()
        for node in self.connected_nodes:
            conn.append(node.node_id)
        print('#{}, connected to # {}'.format(self.node_id, conn))
