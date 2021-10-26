import random as r
import copy
import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.function import freeze
import load_data
import multiprocessor
import time
import fitness as fit
from networkx.classes.reportviews import EdgeDataView

"""
I N I T I A L I S E 
"""
def init_generation(nodeamount,populationsize):
    node_amount = nodeamount
    population_size = populationsize
    node_list = [[]]*population_size
    node_generator = []

    for i in range(population_size):
        for j in range(node_amount):
            node_generator.append((j,{"decay constant": r.uniform(decay_min,decay_max), "threshold": r.uniform(threshold_min,threshold_max), "prob selffire": r.uniform(prob_selffire_min,prob_selffire_max), "obstruction period": r.uniform(obstruction_period_min,obstruction_period_max)  # Configurable variables
            ,"spike": 0, "prev spike": 0, "exhausted": 0, "potential": 0}))  # Functional variables
            #print("i: ",i,"j: ",j,node_generator)
        node_list[i] = copy.deepcopy(node_generator)
        node_generator.clear()
    '''[(0,1,1),(0,7,1),(1,2,1),(1,8,1),(2,3,1),(2,9,1),(3,4,1),(3,10,1),(4,5,1)]''' # Test string
    #print("node_list[0]: ",node_list[0])
    return node_list

"""
S I M U L A T I O N
"""
def phenotype_generator(G_,gen,population_size):
    phenotype_temp = []
    phenotype_ = [[]]*population_size
    fs = 50000
    for i in range(population_size):
        time = 0
        G_.add_nodes_from(gen[i])
        #print("i: ",i,"nodes data: ",G_.nodes.data())
        '''G_.nodes[1]["spike"] = 1
        G_.nodes[2]["spike"] = 1
        G_.nodes[0]["potential"] = 0.5
        G_.edges[0,1]["weight"] = 1
        G_.edges[0,2]["weight"] = 1'''
        while time < 0.01:
            for nodenr in range(len(gen[i])):
                #print("1",G_.nodes[nodenr])
                self_prob = r.random()
                
                if G_.nodes[nodenr]["potential"] > 0:   # Checks if the node has a voltage potential to decrease it with the decay constant
                    #print("1: potential >0:", G_.nodes[nodenr]["potential"])
                    G_.nodes[nodenr]["potential"] -= G_.nodes[nodenr]["decay constant"]
                    #print("2: potential >0:", G_.nodes[nodenr]["potential"])
                elif G_.nodes[nodenr]["potential"] < 0:
                    G_.nodes[nodenr]["potential"] = 0
                    #print("potential <0:", G_.nodes[nodenr]["potential"])
                
                if G_.nodes[nodenr]["exhausted"] > 0:   # Exhausted nodes are inactive for a period of time
                    G_.nodes[nodenr]["exhausted"] -= 1/fs
                    #print("exhausted: ",G_.nodes[nodenr]["exhausted"])
                
                elif G_.nodes[nodenr]["exhausted"] == 0:
                    if G_.nodes[nodenr]["prev spike"] == 1:
                        G_.nodes[nodenr]["prev spike"] = 0

                    for k, nbrs in G_.adj.items():  # Checks the neighbours for spikes and multiplies it with the weighted edge
                        if k == i:
                            for nbr, eattr in nbrs.items():
                                G_.nodes[nodenr]["potential"] += G_.nodes[nbr]["prev spike"]*eattr["weight"]
                                #print("nodenr: ",nodenr,"potential: ",G_.nodes[nodenr]["potential"],"nbr: ",nbr,"nbr_prev_spike: ", G_.nodes[nbr]["prev spike"])
                    if (G_.nodes[nodenr]["potential"] >  G_.nodes[nodenr]["threshold"]) or ((self_prob <= G_.nodes[nodenr]["prob selffire"])):  # Node spikes if threshold is exceeded
                        G_.nodes[nodenr]["spike"] = 1
                        #print("time: ",time, "potential: ", G_.nodes[nodenr]["potential"],"threshold: ",G_.nodes[nodenr]["threshold"], "self_prob: ",self_prob,"selffire: ",G_.nodes[nodenr]["prob selffire"])
                        phenotype_temp.append([float(time),nodenr])
                        #print("i: ",i,"phenotype_temp: ",phenotype_temp)
                        

                elif G_.nodes[nodenr]["exhausted"] < 0:
                    G_.nodes[nodenr]["exhausted"] = 0
                
                #print("node: ",nodenr,"potential: ",G_.nodes[nodenr]["potential"],"nbr_spike: ", G_.nodes[nbr]["spike"])
                #print("2",G_.nodes[nodenr])
                if G_.nodes[nodenr]["spike"] == 1:  # Resets spikes if there has been a spike in last iteration and deactivates the node
                    G_.nodes[nodenr]["prev spike"] = 1
                    G_.nodes[nodenr]["spike"] = 0
                    G_.nodes[nodenr]["exhausted"] = G_.nodes[nodenr]["obstruction period"]
                    G_.nodes[nodenr]["potential"] = 0
                    G_.nodes[nodenr]["exhausted"] = G_.nodes[nodenr]["obstruction period"]

            time += 1/fs
                
            '''
            """
            Drawing
            """
            pos = nx.spring_layout(G_, iterations=300, seed=3977)
            color_map = []
            if G_.nodes[nodenr]['prev spike'] == 1:
                color_map.append('green')
            elif G_.nodes[nodenr]['exhausted'] > 0:
                color_map.append('red')
            else:
                color_map.append('gray')
            nx.draw(
                G_,
                pos,
                node_color=color_map,
                edgecolors="tab:gray",  # Node surface color
                edge_color="tab:gray",  # Color of graph edges
                node_size=100,
                with_labels=True,
                width=3,
            )
            plt.show()'''

        phenotype_[i] = copy.deepcopy(phenotype_temp)
        #print("phenotype_: ",phenotype_)
        #print("i: ",i,"phenotype_temp: ",phenotype_temp)
        phenotype_temp.clear()
        '''print("phenotype0_: ",phenotype_[0])
        print("phenotype0 len: ",len(phenotype_[0]))
        print("phenotype1_: ",phenotype_[1])
        print("phenotype1 len: ",len(phenotype_[1]))'''

    return phenotype_          

"""
M U T A T I O N
"""
def mutation(gen,best_match,node_amount,population_size):
    mutated_population = [[]]*population_size
    for i in range(population_size):
        best_individual = copy.deepcopy(gen[best_match])
        for j in range(node_amount):
            for k in range(len(best_individual[j][1])):
                if r.random() <= 0.9:
                    if k == 0:
                        best_individual[j][1]["decay constant"] = r.uniform(decay_min,decay_max)
                    elif k == 1:
                        best_individual[j][1]["threshold"] = r.uniform(threshold_min,threshold_max)
                    elif k == 2:
                        best_individual[j][1]["prob selffire"] = r.uniform(prob_selffire_min,prob_selffire_max)
                    elif k == 3:
                        best_individual[j][1]["obstruction period"] = r.uniform(obstruction_period_min,obstruction_period_max)
        mutated_population[i] = best_individual
        #print("mutated_population[0]: ",mutated_population[0])
    return mutated_population


'''
#print(G.nodes[1])
#print(G.edges([1]))
#print(G.degree[1])
G.nodes[1]['spike'] = 1
G.nodes[2]['rest'] = 0.3
print(G.nodes.data())
'''


def network_initialise():
    print("name: ",__name__)
    print("Network initalising:")
    print("Electrode array consists of 60 electrodes")
    node_amount = input("How many nodes should be generated in the network?:")
    population_size = input("How many individuals should comprise the population?:")
    CA = input("Should the network be connected as CA?:")
    
    if CA == "yes":
        edge_list = [(0,1,1),(0,7,1),(1,2,1),(1,8,1),(2,3,1),(2,9,1),(3,4,1),(3,10,1),(4,5,1),(4,11,1),(5,12,1),
            (6,7,1),(6,14,1),(7,8,1),(7,15,1),(8,9,1),(8,16,1),(9,10,1),(9,17,1),(10,11,1),(10,18,1),(11,12,1),(11,19,1),(12,13,1),(12,20,1),(13,21,1),
            (14,15,1),(14,22,1),(15,16,1),(15,23,1),(16,17,1),(16,24,1),(17,18,1),(17,25,1),(18,19,1),(18,26,1),(19,20,1),(19,27,1),(20,21,1),(20,28,1),(21,29,1),
            (22,23,1),(22,30,1),(23,24,1),(23,31,1),(24,25,1),(24,32,1),(25,26,1),(25,33,1),(26,27,1),(26,34,1),(27,28,1),(27,35,1),(28,29,1),(28,36,1),(29,37,1),
            (30,31,1),(30,38,1),(31,32,1),(31,39,1),(32,33,1),(32,40,1),(33,34,1),(33,41,1),(34,35,1),(34,42,1),(35,36,1),(35,43,1),(36,37,1),(36,44,1),(37,45,1),
            (38,39,1),(38,46,1),(39,40,1),(39,47,1),(40,41,1),(40,48,1),(41,42,1),(41,49,1),(42,43,1),(42,50,1),(43,44,1),(43,51,1),(44,45,1),(44,52,1),(45,53,1),
            (46,47,1),(47,48,1),(47,54,1),(48,49,1),(48,55,1),(49,50,1),(49,56,1),(50,51,1),(50,57,1),(51,52,1),(51,58,1),(52,53,1),(52,59,1),
            (54,55,1),(55,56,1),(56,57,1),(57,58,1),(58,59,1)]
    G_ = nx.Graph()
    G_.add_weighted_edges_from(edge_list)
    return int(node_amount), int(population_size), G_, edge_list

"""
P R O G R A M
"""

if __name__ == '__main__':
    # Initialise
    t0 = time.perf_counter()

    ###
    decay_min = 0.001
    decay_max = 0.1
    threshold_min = 2
    threshold_max = 3
    prob_selffire_min = 0.001
    prob_selffire_max = 0.01
    obstruction_period_min = 0.005
    obstruction_period_max = 0.05
    # could be declared in initialise() and returned
    ###
    
    nodeamount, populationsize, G, edgelist = network_initialise()
    generation = init_generation(nodeamount,populationsize)
    
    # Update

    generation_nr = 0
    fitnesscore = 900000

    while fitnesscore > 10000:
        t1 = time.perf_counter()
    
    
        #phenotype = phenotype_generator(G,generation,populationsize)
        args = multiprocessor.multi_variables(G,generation,populationsize)
        phenotype = multiprocessor.multiprocessor(args)
        #print("generation_nr: ",generation_nr,"name: ",__name__)
        
        t2 = time.perf_counter()
        bestmatch, fitnesscore = fit.pick_best_rule_set(phenotype)
    
        if generation_nr == 0:
            print("Initial generation")
        else:
            print("Generation: ",generation_nr)
        print("Population size: ",populationsize)
        print("Phenotype generation finished in "+str(round(t2-t1,2))+" seconds")
        print("best individual: ",bestmatch, "Fitnesscore: ",fitnesscore)
    
        generation = mutation(generation,bestmatch,nodeamount,populationsize)
        #generation = multiprocessor.multi_mutation(generation,bestmatch,nodeamount,populationsize)

        generation_nr += 1
        #time.sleep(1)

    t3 = time.perf_counter()
    print("total elapsed time: ",round(t3-t2,2))
    f = open("Data\Best_spikes.txt", "w")
    for element in phenotype[bestmatch]:
        f.write(str(element[0]) + " " + str(element[1]) + '\n')
    f.close()
 
    """

    - Apply number of active electrodes in fitness function?
    - Fix weights

    """