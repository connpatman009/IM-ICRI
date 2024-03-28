class Edge:
    # src: Node = Source
    # dest: Node = Destination
    # ip: int = probability of src influencing dest
    def __init__(self, src, dest, influence_probability):
        self.source = src
        self.destination = dest
        self.ip = influence_probability
    
    def equals(self, e):
        if self.source == e.source and self.destination == e.destination:
            return True
        else:
            return False
    
    def __str__(self):
        return str(self.source.id) + " " + str(self.destination.id) + " (" + str(self.ip) + ")"

    def __repr__(self):
        return self.__str__()
