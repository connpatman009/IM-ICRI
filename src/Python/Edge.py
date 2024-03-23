class Edge:
    # src: Node = Source
    # dest: Node = Destination
    # ip: int = influence probability
    def __init__(self, src, dest, ip):
        self.source = src
        self.destination = dest
        self.influenceProbability = ip
    
    def getSource(self):
        return self.source
    
    def getDestination(self):
        return self.destination
    
    def getIP(self):
        return self.influenceProbability
    
    def equals(self, e):
        if self.getSource() == e.getSource() and self.getDestination() == e.getDestination():
            return True
        else:
            return False
    
    def __str__(self):
        return str(self.source.getID()) + " " + str(self.destination.getID()) + " (" + str(self.influenceProbability) + ")"
