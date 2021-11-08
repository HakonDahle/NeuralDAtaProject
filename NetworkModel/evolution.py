import random as r
import copy
import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.function import freeze
import file_write
import simulation as sim
import time as t
import fitness as fit

"""
I N I T I A L I S E 
"""

# Establishing a list of nodes with its attributes
def init_generation(nodeamount,populationsize):

    node_amount = int(nodeamount)   # Nodes in the network
    population_size = int(populationsize)
    node_generator = []
    graph_list = []

    # Generates desired number of individuals
    for _ in range(population_size):

        # Generates desired number of nodes with the attributes
        for j in range(node_amount):
            node_generator.append((j,{"decay constant": r.uniform(decay_min,decay_max), "threshold": r.uniform(threshold_min,threshold_max), "prob selffire": r.uniform(prob_selffire_min,prob_selffire_max), "obstruction period": r.uniform(obstruction_period_min,obstruction_period_max)  # Adjustable attributes
            ,"spike": 0, "prev spike": 0, "exhausted": 0, "potential": 0}))  # Functional attributes
            #print("i: ",i,"j: ",j,node_generator) 
        
        G_ = nx.Graph() # Creating the undirected graph
        G_.add_nodes_from(node_generator)   # Adds the nodes with their attributes to the graph
        edge_list = init_connection()   # Creates a list of weighted edges
        G_.add_weighted_edges_from(edge_list)   # Adds the weighted edges to the graph
        graph_list.append(G_)   # Creates a list of graphs, which are the individuals that comprise the generation
        node_generator.clear()
    
    return graph_list


# Establishing a list of edges with weights
def init_connection():

    edge_list = []
    weight_factor = r.uniform(weight_min,weight_max)    # Creates a random weight within the desired range

    edge_list = [(0,1,weight_factor),(0,7,weight_factor),(1,2,weight_factor),(1,8,weight_factor),(2,3,weight_factor),(2,9,weight_factor),(3,4,weight_factor),(3,10,weight_factor),(4,5,weight_factor),(4,11,weight_factor),(5,12,weight_factor),
                (6,7,weight_factor),(6,14,weight_factor),(7,8,weight_factor),(7,15,weight_factor),(8,9,weight_factor),(8,16,weight_factor),(9,10,weight_factor),(9,17,weight_factor),(10,11,weight_factor),(10,18,weight_factor),(11,12,weight_factor),(11,19,weight_factor),(12,13,weight_factor),(12,20,weight_factor),(13,21,weight_factor),
                (14,15,weight_factor),(14,22,weight_factor),(15,16,weight_factor),(15,23,weight_factor),(16,17,weight_factor),(16,24,weight_factor),(17,18,weight_factor),(17,25,weight_factor),(18,19,weight_factor),(18,26,weight_factor),(19,20,weight_factor),(19,27,weight_factor),(20,21,weight_factor),(20,28,weight_factor),(21,29,weight_factor),
                (22,23,weight_factor),(22,30,weight_factor),(23,24,weight_factor),(23,31,weight_factor),(24,25,weight_factor),(24,32,weight_factor),(25,26,weight_factor),(25,33,weight_factor),(26,27,weight_factor),(26,34,weight_factor),(27,28,weight_factor),(27,35,weight_factor),(28,29,weight_factor),(28,36,weight_factor),(29,37,weight_factor),
                (30,31,weight_factor),(30,38,weight_factor),(31,32,weight_factor),(31,39,weight_factor),(32,33,weight_factor),(32,40,weight_factor),(33,34,weight_factor),(33,41,weight_factor),(34,35,weight_factor),(34,42,weight_factor),(35,36,weight_factor),(35,43,weight_factor),(36,37,weight_factor),(36,44,weight_factor),(37,45,weight_factor),
                (38,39,weight_factor),(38,46,weight_factor),(39,40,weight_factor),(39,47,weight_factor),(40,41,weight_factor),(40,48,weight_factor),(41,42,weight_factor),(41,49,weight_factor),(42,43,weight_factor),(42,50,weight_factor),(43,44,weight_factor),(43,51,weight_factor),(44,45,weight_factor),(44,52,weight_factor),(45,53,weight_factor),
                (46,47,weight_factor),(47,48,weight_factor),(47,54,weight_factor),(48,49,weight_factor),(48,55,weight_factor),(49,50,weight_factor),(49,56,weight_factor),(50,51,weight_factor),(50,57,weight_factor),(51,52,weight_factor),(51,58,weight_factor),(52,53,weight_factor),(52,59,weight_factor),
                (54,55,weight_factor),(55,56,weight_factor),(56,57,weight_factor),(57,58,weight_factor),(58,59,weight_factor)]  # The edge list is following a regular structure, and is therefore fixed in accordance with the grid layout 
    
    return edge_list      


"""
V I S U A L I S A T I O N
"""

# Can be used for visualisation if PyCx simulator is imported with Initialise, Observe and Update functions
def net_visualisation(G_,node_amount,ti_me,color_map):
    pos = nx.spring_layout(G_, iterations=300, seed=3977)
    nx.draw(
    G_,
    pos,
    node_color=color_map,
    edgecolors="tab:gray",  # Node surface color
    edge_color="tab:gray",  # Color of graph edges
    node_size=500,
    with_labels=True,
    width=3,
    )
    plt.show()
    

"""
M U T A T I O N
"""

# Function used for mutating the best individual and producing a new generation
def mutation(graph_list,best_match,population_size):
    
    mutated_graph_list = []
    best_individual = copy.deepcopy(graph_list[best_match]) # Gets the elite individual
    
    # Runs through all individuals
    for _ in range(population_size):

        G_= best_individual

        # Runs through all nodes in the individual
        for nodenr in range(len(G_)):

            # Runs through all the genes of the nodes genotype
            for k in range(len(G_.nodes[nodenr])):

                # Mutates a gene with 1% probability
                if r.random() <= 0.01:
                    
                    # The genotype comprise of the following genes: voltage leaking constant, Voltage Threshold, Probability of selfspiking, refraction period and the edges' weights
                    # If a gene mutates, then it will change with a +- range from its current value, and within the min/max boundaries
                    if k == 0:
                        G_.nodes[nodenr]["decay constant"] += r.uniform(-decay_range,decay_range)
                        if G_.nodes[nodenr]["decay constant"] < decay_min:
                            G_.nodes[nodenr]["decay constant"] = decay_min
                        elif G_.nodes[nodenr]["decay constant"] > decay_max:
                            G_.nodes[nodenr]["decay constant"] = decay_max
                    elif k == 1:
                        G_.nodes[nodenr]["threshold"] +=  r.uniform(-threshold_range,threshold_range)
                        if G_.nodes[nodenr]["threshold"] < threshold_min:
                            G_.nodes[nodenr]["threshold"] = threshold_min
                        elif G_.nodes[nodenr]["threshold"] > threshold_max:
                            G_.nodes[nodenr]["threshold"] = threshold_max
                    elif k == 2:
                        G_.nodes[nodenr]["prob selffire"] += r.uniform(-prob_selffire_range,prob_selffire_range)
                        if G_.nodes[nodenr]["prob selffire"] < prob_selffire_min:
                            G_.nodes[nodenr]["prob selffire"] = prob_selffire_min
                        elif G_.nodes[nodenr]["prob selffire"] > prob_selffire_max:
                            G_.nodes[nodenr]["prob selffire"] = prob_selffire_max
                    elif k == 3:
                        G_.nodes[nodenr]["obstruction period"] += r.uniform(-obstruction_period_range,obstruction_period_range)
                        if G_.nodes[nodenr]["obstruction period"] < obstruction_period_min:
                            G_.nodes[nodenr]["obstruction period"] = obstruction_period_min
                        elif G_.nodes[nodenr]["obstruction period"] > obstruction_period_max:
                            G_.nodes[nodenr]["obstruction period"] = obstruction_period_max
                    elif k == 4:
                        adjusted_weight = r.uniform(-weight_range,weight_range)

                        # Runs through the nodes' neihbours
                        for edges in (G_.adj[nodenr]):

                            # Every edge from the node is given the same updated weight within the boundaries
                            G_.edges[nodenr,edges]["weight"] += float(adjusted_weight)
                            if G_.edges[nodenr,edges]["weight"] < weight_min:
                                G_.edges[nodenr,edges]["weight"] = float(weight_min)
                            elif G_.edges[nodenr,edges]["weight"] > weight_max:
                                 G_.edges[nodenr,edges]["weight"] = float(weight_max)
        
        mutated_graph_list.append(G_)   # The new generation
        
    return mutated_graph_list


"""
M A I N  P R O G R A M
"""

# Main program
if __name__ == '__main__':

    # Runs the EA for X number of trials
    for _ in range(100):
        
        '''
        Initialise
        '''
        
        t0 = t.perf_counter()   # Initial timestamp
        
        # Min/Max parameters are used for initial node configuration, and range during mutation
        decay_min = 0.0001
        decay_max = 2
        decay_percent_of_max = 0.1
        decay_range = (decay_max)*decay_percent_of_max
        threshold_min = 0.5
        threshold_max = 1
        threshold_percent_of_max = 0.1
        threshold_range = (threshold_max)*threshold_percent_of_max
        prob_selffire_min = 0.000001
        prob_selffire_max = 0.001
        prob_selffire_percent_of_max = 0.1
        prob_selffire_range = (prob_selffire_max)*prob_selffire_percent_of_max
        obstruction_period_min = 0.003 
        obstruction_period_max = 0.5
        obstruction_period_percent_of_max = 0.1
        obstruction_period_range = (obstruction_period_max)*obstruction_period_percent_of_max
        weight_min = 0.5
        weight_max = 1
        weight_percent_of_max = 0.1
        weight_range = (weight_max)*weight_percent_of_max

        # Initialising the network
        nodeamount = 60  # Must be 60 because of the regular structure and fixed edges
        populationsize = int(input("How many individuals should comprise the population?:"))
        population = init_generation(nodeamount,populationsize) # Generating the first generation
        trialname = input("Please enter the name of the file: ")    # Used for permanent storage
        
        '''
        Update
        '''

        # Declaring variables used in Update
        nr_of_generations = 25  # Max number of generations
        generation_nr = 0   # Counts generations
        trial_nr = 0    # Counts trials
        fitnesscore = 900000    # imaginary high fitness score

        print("Trial version: ",trial_nr)

        # Phenotype. Fitness function. Mutation - new generation. Repeat:
        # Each generation is generating the phenotype, which is evaluated by the fitness function. 
        # Then the elite individual is passed through a clone and mutation function 
        # Finally the mutated individuals comprise the new generation.
        for _ in range(nr_of_generations):
            
            if generation_nr == 0:
                print("Initial generation")
            else:
                print("Generation: ",generation_nr)

            t1 = t.perf_counter()   # Start time for the new generation

            phenotype = sim.multiprocessor(population)   # Testing the artificial neuronal network in an environment.

            t2 = t.perf_counter()   # Stop time for phenotype production
            
            print("time: ",t2-t1)

            bestindividual, fitnesscore = fit.pick_best_rule_set(phenotype) # The generated spike data is passed through the fitness function to get the best individual
            
            print("Best individual: ",bestindividual, "fitnesscore: ",fitnesscore)

            file_write.phenotype_file(fitnesscore,generation_nr,trialname,trial_nr,bestindividual,phenotype)    # Writes spikes and coherent timestamp to file for permanent storage in the same format as reference data
            file_write.fitness_file(fitnesscore,generation_nr,trialname,trial_nr)    # Writes fitness score  in chronological order to file for permanent storage.

            # Starts a new trial if the fitness score is satisfactory
            if fitnesscore < 10:
                print("Fitnesscore is below 10. Starting new trial.")
                break

            population = mutation(population,bestindividual,populationsize) # Cloning the best individual of the population and mutates their genotype to form a new generation
            
            generation_nr += 1  # Generation counter
            
            # Resets if fitness score is not satisfactory within 25 generations
            if generation_nr > 25:
                generation_nr = 0

        t3 = t.perf_counter()   # Stop time for the new generation
        trial_nr +=1    # Trial counter

        print("total elapsed time: ",round(t3-t0,2))