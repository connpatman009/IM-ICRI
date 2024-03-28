import random
import heapq
from Edge import Edge
from Graph import Graph
from Node import Node

class Test:
    # Helper method to get the seed set, returns a list of nodes selected to be in the seed set already activated
    #   graph = Graph object that represents the social network
    #   algo  = Seed selection paradigm
    #   k     = How many nodes to select for the seed set
    def get_seed_set(self, graph, algo, k):
        match algo:
            case "random":
                seed_set = random.sample(graph.nodes, k)
                for seed in seed_set:
                    seed.active = True
            case "greedy":      # This greedy is defined to select the k nodes with the most edges
                seed_set = heapq.nlargest(k, graph.nodes)
                for seed in seed_set:
                    seed.active = True
            case _:
                print("Seed selection paradigm not found:", algo)
                exit(0)

        return seed_set

    # Time-Aware Independent Cascade
    #   network = Graph object that represents the social network
    #   time_limit = number of steps that you are able to spread influence
    #   k = maximum number of nodes in the seed set
    #   algo = [seed selection paradigm, time step selection paradigm] Both are strings
    #   rng = random number generator
    def independent_cascade(self, network, time_limit, k, algo, rng):
        activated = []                                  # List of which nodes are activated at each time step
        seed_selection = algo[0]
        time_selection = algo[1]
        seed_selected = False   # Determines whether the seed set has been chosen yet

        # A_0 = {initially activated nodes}
        if time_selection == "t=0":
            print("seed set selected at 0")
            seed_set = self.get_seed_set(network, seed_selection, k)
            seed_selected = True
            print(seed_set)
            activated.append(seed_set)
        else:
            activated.append([])
        
        for t in range(1, time_limit):
            print("t =", t)
            if not seed_selected:
                match time_selection:
                    case "midpoint":
                        if t == int(time_limit / 2):
                            seed_set = self.get_seed_set(network, seed_selection, k)
                            seed_selected = True
                            print("seed set selected at", t)
                            print(seed_set)
                            activated.append(seed_set)
                            continue
                    case _:
                        print("Time selection paradigm not found:", time_selection)
                        exit(0)

            t_activated = []                            # A_t = {}
            for v in activated[t-1]:                    # for v in A_(t-1)
                for w_edge in v.edges:                  # for w in neighbor(v)
                    w = w_edge.destination
                    if not w.active and rng.random() < w_edge.ip:    # Randomly influence the neighbor accoring to the likelihood of influence
                        t_activated.append(w)           # A_t = A_t U {w}
                        w.active = True

            if (seed_selected and len(t_activated) == 0):
                print("No more activated at", t)
                break
            print(t_activated)
            activated.append(t_activated)               # Add A_t to A            

        # After IC is done, return the list of activated nodes (Flattened)
        return [node for timestep in activated for node in timestep]    # Return a flattened list of activated nodes
        # return activated                                              # Return activated nodes in lists of timestep activated

if __name__ == "__main__":
    test = Test()
    rng = random.Random()

    print("RANDOM, T=0")
    for node in test.independent_cascade(network=Graph(10, 0.5), time_limit=5, k=2, algo=["random", "t=0"], rng=rng):
        print(node)

    print("\n\n\nRANDOM, MIDPOINT")
    for node in test.independent_cascade(Graph(10, 0.5), time_limit=5, k=2, algo=["random", "midpoint"], rng=rng):
        print(node)

    print("\n\n\nGREEDY, T=0")
    g = Graph(10, 0.5)
    print(g.nodes)
    for node in test.independent_cascade(g, time_limit=5, k=2, algo=["greedy", "t=0"], rng=rng):
        print(node)

    print("\n\n\nGREEDY, MIDPOINT")
    g = Graph(10, 0.5)
    print(g.nodes)
    for node in test.independent_cascade(network=g, time_limit=5, k=2, algo=["greedy", "midpoint"], rng=rng):
        print(node)

    print("\n\n\nGREEDY, MIDPOINT ON BIG GRAPH")
    g = Graph(100, 0.1)
    print(g.nodes)
    for node in test.independent_cascade(network=g, time_limit=30, k=2, algo=["greedy", "midpoint"], rng=rng):
        print(node)
