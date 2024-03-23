import random
from Edge import Edge
from Graph import Graph
from Node import Node

class Test:
    def independent_cascade(network, time_limit, rng):
        # Time-Aware Independent Cascade
        activated = []                                  # List of which nodes are activated at each time step
        activated.append([network.get_node(0)])         # A_0 = {initially activated nodes} TODO: Decide the which nodes are selected initially
        
        for t in range(time_limit):
            t_activated = []                            # A_t = {}
            for v in activated[t-1]:                    # for v in A_(t-1)
                for w_edge in v.edges:                  # for w in neighbor(v)
                    w = w_edge.destination
                    # If w not in the activation set
                    all_activated = [j for sub in activated for j in sub]
                    if w not in all_activated:
                        if rng.random() < w_edge.ip:    # Randomly influence the neighbor accoring to the likelihood of influence
                            t_activated.append(w)       # A_t = A_t U {w}

            activated.append(t_activated)               # Add A_t to A
            if (len(t_activated) == 0):
                break

        # After IC is done, return the list of activated nodes
        return activated

    if __name__ == "__main__":
        rng = random.Random()
        g = Graph(10, 0.5)
        print(independent_cascade(g, 10, rng))

