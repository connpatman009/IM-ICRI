import random
import copy
from Edge import Edge
from Node import Node

class Graph:
    # numN: int = number of nodes in the graph
    # density: double = Ratio of how many edges you'd like there to be
    def __init__(self, nodes=[]):
        self.num_nodes = len(nodes)
        self.nodes = nodes
        
    
    @classmethod
    def gen_random(self, numN, density):
        nodes = []
        num_nodes = numN
        
        # Create a random graph with the number of nodes specified
        for i in range(num_nodes):
            new_node = Node(i)
            nodes.append(new_node)
        
        # Randomly generate edges
        rng = random.Random()
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i == j:
                    continue
        
                if rng.random() < density:
                    src = nodes[i]
                    dest = nodes[j].id
                    influence = rng.random() / 2
                    delta_influence = rng.random() / 2
                    if src is not None and dest is not None:
                        src.add_edge(dest, influence, delta_influence)
        
        return Graph(nodes)
        
    def __repr__(self) -> str:
        sb = [f"Node count: {len(self.nodes)}\n"]
        sb.append("{")
        for node in self.nodes:
            sb.append(node.__repr__())
            sb.append(",")
            sb.append("\n")
        sb.pop()
        sb.pop()
        sb.append("\n}")
        return "".join(sb)
        
    def __deepcopy__(self, memo=[]):
        node_list = []
        for node in self.nodes:
            node_list.append(copy.deepcopy(node))
        return Graph(node_list)
        
            
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def get_node(self, id):
        for curr in self.nodes:
            if curr.id == id:
                return curr
        return None

    # Used in our IM-ICRI model. Increases the influence as the time limit approaches, up to a maximum of 0.95
    def ramp_influence(self):
        for i, node in enumerate(self.nodes):
            for j, edge in enumerate(node.edges):
                self.nodes[i].edges[j].ip = min(edge.ip + 0.1, 0.95)
            
    
    def dampen_graph(self, t, time_limit):
        graph = copy.deepcopy(self)
        for i, node in enumerate(graph.nodes):
            for j, edge in enumerate(node.edges):
                graph.nodes[i].edges[j].ip = (1-(t/time_limit)) * edge.ip
        return graph