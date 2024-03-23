import random
from Edge import Edge
from Node import Node

class Graph:
    # numN: int = number of nodes in the graph
    # density: double = Ratio of how many edges you'd like there to be
    def __init__(self, numN, density):
        self.nodes = []
        self.numNodes = numN
        
        # Create a random graph with the number of nodes specified
        for i in range(numN):
            newNode = Node()
            self.nodes.append(newNode)
        
        # Randomly generate edges
        rng = random.Random()
        for i in range(numN):
            for j in range(numN):
                if i == j:
                    continue
        
                if rng.random() < density:
                    src = self.getNode(i)
                    dest = self.getNode(j)
                    influence = rng.random()
                    if src is not None and dest is not None:
                        src.addEdge(dest, influence)
    
    def getNode(self, id):
        for curr in self.nodes:
            if curr.getID() == id:
                return curr
        return None
