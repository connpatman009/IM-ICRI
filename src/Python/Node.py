from Edge import Edge

class Node:
    # Static count of how many nodes there are
    nodeCount = 0
    
    # id: int = identification number for the node
    # edges: list = List of edges originating from this node
    # active: bool = Indicates whether the node has been activated yet
    def __init__(self):
        self.id = Node.nodeCount
        Node.nodeCount += 1
        self.edges = []
        self.active = False
    
    def __str__(self):
        sb = []
        sb.append("Node " + str(self.id))
        if self.active:
            sb.append(" (ACTIVE)")
        '''sb.append("\nEdges: [" + str(len(self.edges)) + "]\n")
        for e in self.edges:
            sb.append(str(e.destination.id))
            sb.append(" (")
            sb.append(str(e.ip))
            sb.append(")")
            sb.append(", ")
        sb.pop()    # Remove the extra comma at the end'''

        return "".join(sb)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id

    # Add a new edge starting from this node leading to another node "destination"
    def add_edge(self, destination, weight):
        proposed_edge = Edge(self, destination, weight)
        if proposed_edge not in self.edges:
            self.edges.append(proposed_edge)
            return True
        else:
            print("Edge already in graph")
            return False
