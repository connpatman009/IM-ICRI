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
    
    def getID(self):
        return self.id
    
    # Add a new edge starting from this node leading to another node "destination"
    def addEdge(self, destination, weight):
        proposedEdge = Edge(self, destination, weight)
        if proposedEdge not in self.edges:
            self.edges.append(proposedEdge)
            return True
        else:
            print("Edge already in graph")
            return False
    
    def __str__(self):
        sb = []
        sb.append("Node " + str(self.id))
        if self.active:
            sb.append(" (ACTIVE)\n")
        else:
            sb.append("\n")
        sb.append("Edges: " + "\n")
        for e in self.edges:
            sb.append(str(e.getDestination().getID()))
            sb.append(" (")
            sb.append(str(e.getIP()))
            sb.append(")")
            sb.append(", ")

        sb.pop()    # Remove the extra comma at the end
        sb.append("\n")
        return "".join(sb)
