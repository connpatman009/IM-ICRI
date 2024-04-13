import random
import heapq
import copy
from Edge import Edge
from Graph import Graph
from Node import Node

MONTE_CARLO_TRIALS = 10

class Test:
    # Helper method to simulate independent_cascade for use with Monte Carlo Approximation
    #   Similar to independent_cascade below, but originates with the seed set already chosen and starting from time step t
    #   TODO: Update with the ramping influence model
    def sim_IC(self, sim_graph, seed_set, time, time_limit, ramping):
        time_left = time_limit - time
        activated = []                                  # List of which nodes are activated at each time step
        graph = copy.deepcopy(sim_graph)
        
        for t in range(time+1, time_limit):
            t_activated = []                            # A_t = {}
            for v in activated[t-1]:                    # for v in A_(t-1)
                for w_edge in v.edges:                  # for w in neighbor(v)
                    w = graph.nodes[w_edge.destination]
                    if not w.active and rng.random() < w_edge.ip:    # Randomly influence the neighbor accoring to the likelihood of influence
                        t_activated.append(w)           # A_t = A_t U {w}
                        w.active = True

            if (len(t_activated) == 0):
                break
            activated.append(t_activated)               # Add A_t to A
            if ramping:
                graph.ramp_influence()

        # After IC is done, return the list of activated nodes (Flattened)
        return [node for timestep in activated for node in timestep]    # Return a flattened list of activated nodes


    # Helper method to get the seed set, returns a list of nodes selected to be in the seed set already activated
    #   graph = Graph object that represents the social network
    #   algo  = Seed selection paradigm
    #   k     = How many nodes to select for the seed set
    def get_seed_set(self, graph, algo, k, t, time_limit, ramping):
        match algo:
            case "random":
                seed_set = random.sample(graph.nodes, k)
                for seed in seed_set:
                    seed.active = True
            case "greedy":      # Monte Carlo Greedy Approximation
                seed_set = []
                for i in range(k):
                    #print(f"Choosing node {i}")
                    sim_activated = []      #List of how many nodes (on average) were activated when adding w to the seed set
                    sim_w = []              # Parallel list of w

                    for w in graph.nodes:
                        if w not in seed_set:
                            # Try seed_set U {w} for each node not already in the seed set
                            seed_set_with_w = seed_set.copy()
                            seed_set_with_w.append(w)
                            w.active = True
                            # get the expected number of nodes activated!
                            avg_activated = 0
                            for sim in range(MONTE_CARLO_TRIALS):
                                avg_activated += len(self.sim_IC(graph, seed_set_with_w, t, time_limit, ramping)) / MONTE_CARLO_TRIALS
                            #sim_activated.append(self.sim_IC(graph, seed_set_with_w, t, time_limit, ramping))
                            sim_activated.append(avg_activated)
                            sim_w.append(w)

                            # Reset which nodes have been activated
                            for node in graph.nodes:
                                node.active = False
                            for node in seed_set:
                                node.active = True

                    # Check which addition of w lead to the most activated nodes
                    max_activated = sim_activated[0] #len(sim_activated[0])
                    max_index = 0
                    for i in range(1, len(sim_activated)):
                        if sim_activated[i] > max_activated:
                            max_activated = sim_activated[i]
                            max_index = i
                    
                    #print(sim_activated)

                    # Add the node with the most simulated influence spread to the seed set
                    sim_w[max_index].active = True
                    seed_set.append(sim_w[max_index])
            case "damped_greedy":      # Monte Carlo Greedy Approximation
                    seed_set = []
                    for i in range(k):
                        #print(f"Choosing node {i}")
                        sim_activated = []      #List of how many nodes (on average) were activated when adding w to the seed set
                        sim_w = []              # Parallel list of w

                        for w in graph.nodes:
                            if w not in seed_set:
                                # Try seed_set U {w} for each node not already in the seed set
                                seed_set_with_w = seed_set.copy()
                                seed_set_with_w.append(w)
                                w.active = True
                                # get the expected number of nodes activated!
                                avg_activated = 0
                                for sim in range(MONTE_CARLO_TRIALS):
                                    avg_activated += len(self.sim_IC(graph.dampen_graph(t, time_limit), seed_set_with_w, t, time_limit, ramping)) / MONTE_CARLO_TRIALS
                                #sim_activated.append(self.sim_IC(graph, seed_set_with_w, t, time_limit, ramping))
                                sim_activated.append(avg_activated)
                                sim_w.append(w)

                                # Reset which nodes have been activated
                                for node in graph.nodes:
                                    node.active = False
                                for node in seed_set:
                                    node.active = True

                        # Check which addition of w lead to the most activated nodes
                        max_activated = sim_activated[0] #len(sim_activated[0])
                        max_index = 0
                        for i in range(1, len(sim_activated)):
                            if sim_activated[i] > max_activated:
                                max_activated = sim_activated[i]
                                max_index = i
                        
                        #print(sim_activated)

                        # Add the node with the most simulated influence spread to the seed set
                        sim_w[max_index].active = True
                        seed_set.append(sim_w[max_index])

                    return seed_set
            case _:
                print("Seed selection paradigm not found:", algo)
                exit(0)

        return seed_set

    # Time-Aware Independent Cascade
    #   graph = Graph object that represents the social network
    #   time_limit = number of steps that you are able to spread influence
    #   k = maximum number of nodes in the seed set
    #   algo = [seed selection paradigm, time step selection paradigm] Both are strings
    #   ramping = True if ramping influence, False for static edge weights
    #   rng = random number generator
    def independent_cascade(self, sim_graph, time_limit, k, algo, ramping, rng):
        activated = []                                  # List of which nodes are activated at each time step
        seed_selection = algo[0]
        time_selection = algo[1]
        seed_selected = False   # Determines whether the seed set has been chosen yet
        #print(f"Graph at time = {0}: {graph}")
        graph = copy.deepcopy(sim_graph)
        if time_selection == "random":
            random_seed_time = rng.randrange(0, time_limit)
        if time_selection == "greedy":
            greedy_seed_time = 0
            best_avg_activated = 0
            test_graph = copy.deepcopy(graph)
            for t in range(time_limit):
                seed_set_t = self.get_seed_set(test_graph, seed_selection, k, t, time_limit, ramping)
                avg_activated = 0
                for sim in range(MONTE_CARLO_TRIALS):
                    avg_activated += len(self.sim_IC(test_graph, seed_set_t, t, time_limit, ramping)) / MONTE_CARLO_TRIALS
                #print(avg_activated)
                if avg_activated > best_avg_activated:
                    #print(f"Woohoo better at time {t}")
                    best_avg_activated = avg_activated
                    greedy_seed_time = t
                test_graph.ramp_influence()
        if time_selection == "damped_greedy":
            greedy_seed_time = 0
            best_avg_activated = 0
            test_graph = copy.deepcopy(graph)
            for t in range(time_limit):
                seed_set_t = self.get_seed_set(test_graph, seed_selection, k, t, time_limit, ramping)
                avg_activated = 0
                for sim in range(MONTE_CARLO_TRIALS):
                    avg_activated += len(self.sim_IC(test_graph.dampen_graph(t, time_limit), seed_set_t, t, time_limit, ramping)) / MONTE_CARLO_TRIALS
                #print(avg_activated)
                if avg_activated > best_avg_activated:
                    best_avg_activated = avg_activated
                    greedy_seed_time = t
                test_graph.ramp_influence()

        # A_0 = {initially activated nodes}
        if time_selection == "t=0" or (time_selection == "random" and random_seed_time == 0) or (time_selection == "greedy" and greedy_seed_time == 0) or (time_selection == "damped_greedy" and greedy_seed_time == 0):
            seed_set = self.get_seed_set(graph, seed_selection, k, 0, time_limit, ramping)
            seed_selected = True
            #print("Seed set selected at 0")
            #print(seed_set)
            activated.append(seed_set)
        else:
            activated.append([])
        for t in range(1, time_limit):
            #print("t =", t)
            # Determine whether to select your seed set at time step t
            if not seed_selected:
                match time_selection:
                    case "midpoint":
                        if t == int(time_limit / 2):
                            seed_set = self.get_seed_set(graph, seed_selection, k, t, time_limit, ramping)
                            seed_selected = True
                            #print("Seed set selected at", t)
                            #print(seed_set)
                            activated.append(seed_set)
                            continue
                    case "random":
                        if t == random_seed_time:
                            seed_set = self.get_seed_set(graph, seed_selection, k, t, time_limit, ramping)
                            seed_selected = True
                            #print("Seed set selected at", t)
                            #print(seed_set)
                            activated.append(seed_set)
                            continue
                    case "greedy" | "damped_greedy":
                        if t == greedy_seed_time:
                            seed_set = self.get_seed_set(graph, seed_selection, k, t, time_limit, ramping)
                            seed_selected = True
                            #print("Seed set selected at", t)
                            #print(seed_set)
                            activated.append(seed_set)
                            continue
                    case _:
                        print("Time selection paradigm not found:", time_selection)
                        exit(0)

            t_activated = []                            # A_t = {}
            for v in activated[t-1]:                    # for v in A_(t-1)
                for w_edge in v.edges:                  # for w in neighbor(v)
                    w = graph.nodes[w_edge.destination]
                    roll = rng.random()
                    active = "ACTIVE" if w.active else "NOT ACTIVE"
                    #print(f"Trying to activate Node {w.id} ({active}), with roll={roll} and roll needing to be lower than {w_edge.ip}")
                    if not w.active and roll < w_edge.ip:    # Randomly influence the neighbor accoring to the likelihood of influence
                        #print(f"Activating Node {w.id} at time {t}")
                        t_activated.append(w)           # A_t = A_t U {w}
                        w.active = True
                        #if graph.nodes[w.id].active:
                        #    print(f"Node {w.id} actually active!")

            if (seed_selected and (len(t_activated) == 0)):
                #print("No more activated at", t)
                break
            # print(t_activated)
            activated.append(t_activated)               # Add A_t to A
            if ramping:
                #print(f"Graph at time = {t}: {graph}")
                graph.ramp_influence()
                

        # After IC is done, return the list of activated nodes (Flattened)
        return [node for timestep in activated for node in timestep]    # Return a flattened list of activated nodes
        # return activated                                              # Return activated nodes in lists by timestep activated

if __name__ == "__main__":
    test = Test()
    rng = random.Random()
    tl=10
    size = 100
    graph = Graph.gen_random(size, 10/(size*tl))
    seed_size=3
    # Random seed set selection
    print("SeedSet: RANDOM, Time: T=0")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["random", "t=0"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: RANDOM, Time: MIDPOINT")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["random", "midpoint"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: RANDOM, Time: RANDOM")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["random", "random"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)
    
    print("\n\n\nSeedSet: RANDOM, Time: GREEDY")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["random", "greedy"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)
        
    print("\n\n\nSeedSet: RANDOM, Time: DAMPED GREEDY")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["random", "damped_greedy"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)


    # Greedy seed set selection
    print("\n\n\nSeedSet: GREEDY, Time: T=0")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["greedy", "t=0"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: GREEDY, Time: MIDPOINT")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["greedy", "midpoint"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: GREEDY, Time: RANDOM")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["greedy", "random"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)
        
    print("\n\n\nSeedSet: GREEDY, Time: GREEDY")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["greedy", "greedy"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: GREEDY, Time: DAMPED GREEDY")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["greedy", "damped_greedy"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)
    
    # Greedy seed set selection
    print("\n\n\nSeedSet: DAMPED GREEDY, Time: T=0")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["damped_greedy", "t=0"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: DAMPED GREEDY, Time: MIDPOINT")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["damped_greedy", "midpoint"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: DAMPED GREEDY, Time: RANDOM")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["damped_greedy", "random"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)
        
    print("\n\n\nSeedSet: DAMPED GREEDY, Time: GREEDY")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["damped_greedy", "greedy"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)

    print("\n\n\nSeedSet: DAMPED GREEDY, Time: DAMPED GREEDY")
    result = test.independent_cascade(sim_graph=copy.deepcopy(graph), time_limit=tl, k=seed_size, algo=["damped_greedy", "damped_greedy"], ramping=True, rng=rng)
    print(len(result), "nodes activated:")
    for node in result:
        print(node)