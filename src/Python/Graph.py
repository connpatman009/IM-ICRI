import random
from Edge import Edge
from Node import Node

class Graph:
    # numN: int = number of nodes in the graph
    # density: double = Ratio of how many edges you'd like there to be
    def __init__(self, numN, density):
        self.nodes = []
        self.num_nodes = numN
        
        # Create a random graph with the number of nodes specified
        for i in range(self.num_nodes):
            new_node = Node()
            self.nodes.append(new_node)
        
        # Randomly generate edges
        rng = random.Random()
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i == j:
                    continue
        
                if rng.random() < density:
                    src = self.nodes[i]
                    dest = self.nodes[j]
                    influence = rng.random() / 2.0
                    if src is not None and dest is not None:
                        src.add_edge(dest, influence)
    
    def get_node(self, id):
        for curr in self.nodes:
            if curr.id == id:
                return curr
        return None

    # Used in our IM-ICRI model. Increases the influence as the time limit approaches, up to a maximum of 0.95
    def ramp_influence(self):
        for node in self.nodes:
            for edge in node.edges:
                edge.ip = min(edge.ip + 0.1, 0.95)
