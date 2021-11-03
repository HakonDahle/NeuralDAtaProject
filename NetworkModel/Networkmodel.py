import random as r
import copy
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from networkx.classes.function import freeze
from numpy import errstate
import file_write
import load_data as load
import multiprocessor
import time as t
import fitness_old as fit
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

def init_connection(populationsize):
    population_size = populationsize
    
    edge_list = [[]]*int(population_size)
    for i in range(len(edge_list)):
        weight_factor = r.uniform(weight_min,weight_max)
        edge_list[i] = [(0,1,weight_factor),(0,7,weight_factor),(1,2,weight_factor),(1,8,weight_factor),(2,3,weight_factor),(2,9,weight_factor),(3,4,weight_factor),(3,10,weight_factor),(4,5,weight_factor),(4,11,weight_factor),(5,12,weight_factor),
                (6,7,weight_factor),(6,14,weight_factor),(7,8,weight_factor),(7,15,weight_factor),(8,9,weight_factor),(8,16,weight_factor),(9,10,weight_factor),(9,17,weight_factor),(10,11,weight_factor),(10,18,weight_factor),(11,12,weight_factor),(11,19,weight_factor),(12,13,weight_factor),(12,20,weight_factor),(13,21,weight_factor),
                (14,15,weight_factor),(14,22,weight_factor),(15,16,weight_factor),(15,23,weight_factor),(16,17,weight_factor),(16,24,weight_factor),(17,18,weight_factor),(17,25,weight_factor),(18,19,weight_factor),(18,26,weight_factor),(19,20,weight_factor),(19,27,weight_factor),(20,21,weight_factor),(20,28,weight_factor),(21,29,weight_factor),
                (22,23,weight_factor),(22,30,weight_factor),(23,24,weight_factor),(23,31,weight_factor),(24,25,weight_factor),(24,32,weight_factor),(25,26,weight_factor),(25,33,weight_factor),(26,27,weight_factor),(26,34,weight_factor),(27,28,weight_factor),(27,35,weight_factor),(28,29,weight_factor),(28,36,weight_factor),(29,37,weight_factor),
                (30,31,weight_factor),(30,38,weight_factor),(31,32,weight_factor),(31,39,weight_factor),(32,33,weight_factor),(32,40,weight_factor),(33,34,weight_factor),(33,41,weight_factor),(34,35,weight_factor),(34,42,weight_factor),(35,36,weight_factor),(35,43,weight_factor),(36,37,weight_factor),(36,44,weight_factor),(37,45,weight_factor),
                (38,39,weight_factor),(38,46,weight_factor),(39,40,weight_factor),(39,47,weight_factor),(40,41,weight_factor),(40,48,weight_factor),(41,42,weight_factor),(41,49,weight_factor),(42,43,weight_factor),(42,50,weight_factor),(43,44,weight_factor),(43,51,weight_factor),(44,45,weight_factor),(44,52,weight_factor),(45,53,weight_factor),
                (46,47,weight_factor),(47,48,weight_factor),(47,54,weight_factor),(48,49,weight_factor),(48,55,weight_factor),(49,50,weight_factor),(49,56,weight_factor),(50,51,weight_factor),(50,57,weight_factor),(51,52,weight_factor),(51,58,weight_factor),(52,53,weight_factor),(52,59,weight_factor),
                (54,55,weight_factor),(55,56,weight_factor),(56,57,weight_factor),(57,58,weight_factor),(58,59,weight_factor)]
    '''print("Edgelist[0]: ",edge_list[0])
    print("Edgelist[1]: ",edge_list[1])
    print("Edgelist[2]: ",edge_list[2])'''
    return edge_list      


def network_initialise():
    print("name: ",__name__)
    print("Network initalising:")
    print("Electrode array consists of 60 electrodes")
    t.sleep(2)
    node_amount = input("How many nodes should be generated in the network?:")
    population_size = input("How many individuals should comprise the population?:")
    CA = input("Should the network be connected as CA?:")
    
    trial_name = input("Please enter the name of the file: ")

    if CA == "yes":
        edge_list = init_connection(population_size)
    '''if CA == "yes":
        edge_list = [(0,1,0.1),(0,7,0.1),(1,2,0.1),(1,8,0.1),(2,3,0.1),(2,9,0.1),(3,4,0.1),(3,10,0.1),(4,5,0.1),(4,11,0.1),(5,12,0.1),
            (6,7,0.1),(6,14,0.1),(7,8,0.1),(7,15,0.1),(8,9,0.1),(8,16,0.1),(9,10,0.1),(9,17,0.1),(10,11,0.1),(10,18,0.1),(11,12,0.1),(11,19,0.1),(12,13,0.1),(12,20,0.1),(13,21,0.1),
            (14,15,0.1),(14,22,0.1),(15,16,0.1),(15,23,0.1),(16,17,0.1),(16,24,0.1),(17,18,0.1),(17,25,0.1),(18,19,0.1),(18,26,0.1),(19,20,0.1),(19,27,0.1),(20,21,0.1),(20,28,0.1),(21,29,0.1),
            (22,23,0.1),(22,30,0.1),(23,24,0.1),(23,31,0.1),(24,25,0.1),(24,32,0.1),(25,26,0.1),(25,33,0.1),(26,27,0.1),(26,34,0.1),(27,28,0.1),(27,35,0.1),(28,29,0.1),(28,36,0.1),(29,37,0.1),
            (30,31,0.1),(30,38,0.1),(31,32,0.1),(31,39,0.1),(32,33,0.1),(32,40,0.1),(33,34,0.1),(33,41,0.1),(34,35,0.1),(34,42,0.1),(35,36,0.1),(35,43,0.1),(36,37,0.1),(36,44,0.1),(37,45,0.1),
            (38,39,0.1),(38,46,0.1),(39,40,0.1),(39,47,0.1),(40,41,0.1),(40,48,0.1),(41,42,0.1),(41,49,0.1),(42,43,0.1),(42,50,0.1),(43,44,0.1),(43,51,0.1),(44,45,0.1),(44,52,0.1),(45,53,0.1),
            (46,47,0.1),(47,48,0.1),(47,54,0.1),(48,49,0.1),(48,55,0.1),(49,50,0.1),(49,56,0.1),(50,51,0.1),(50,57,0.1),(51,52,0.1),(51,58,0.1),(52,53,0.1),(52,59,0.1),
            (54,55,0.1),(55,56,0.1),(56,57,0.1),(57,58,0.1),(58,59,0.1)]'''
    G_ = nx.Graph()
    #G_.add_weighted_edges_from(edge_list)
    return int(node_amount), int(population_size), G_, edge_list, trial_name


"""
M U T A T I O N
"""
def mutation(gen,best_match,node_amount,population_size,G_,edge_list):
    mutated_population = [[]]*population_size
    G_.add_weighted_edges_from(edge_list[best_match])
    #print("gen[best_match]: ",gen[best_match])
    for i in range(population_size):
        best_individual = copy.deepcopy(gen[best_match])
        best_weight = copy.deepcopy(edge_list[best_match])
        #print("best individual:                                    ",best_individual)
        for j in range(node_amount):
            for k in range(len(best_individual[j][1])):
                if r.random() <= 0.01:
                    if k == 0:
                        #print("1: best_individual[j][1][decay constant]",best_individual[j][1]["decay constant"])
                        best_individual[j][1]["decay constant"] += r.uniform(-decay_range,decay_range)
                        if best_individual[j][1]["decay constant"] < decay_min:
                            best_individual[j][1]["decay constant"] = decay_min
                        elif best_individual[j][1]["decay constant"] > decay_max:
                            best_individual[j][1]["decay constant"] = decay_max
                        #print("2: best_individual[j][1][decay constant]",best_individual[j][1]["decay constant"])
                    elif k == 1:
                        #print("1: best_individual[j][1][threshold]",best_individual[j][1]["threshold"])
                        best_individual[j][1]["threshold"] +=  r.uniform(-threshold_range,threshold_range)
                        if best_individual[j][1]["threshold"] < threshold_min:
                            best_individual[j][1]["threshold"] = threshold_min
                        elif best_individual[j][1]["threshold"] > threshold_max:
                            best_individual[j][1]["threshold"] = threshold_max
                        #print("2: best_individual[j][1][threshold]",best_individual[j][1]["threshold"])
                    elif k == 2:
                        #print("1: best_individual[j][1][prob selffire]",best_individual[j][1]["prob selffire"])
                        best_individual[j][1]["prob selffire"] += r.uniform(-prob_selffire_range,prob_selffire_range)
                        if best_individual[j][1]["prob selffire"] < prob_selffire_min:
                            best_individual[j][1]["prob selffire"] = prob_selffire_min
                        elif best_individual[j][1]["prob selffire"] > prob_selffire_max:
                            best_individual[j][1]["prob selffire"] = prob_selffire_max
                        #print("2: best_individual[j][1][prob selffire]",best_individual[j][1]["prob selffire"])
                    elif k == 3:
                        #print("1: best_individual[j][1][obstruction period]",best_individual[j][1]["obstruction period"])
                        best_individual[j][1]["obstruction period"] += r.uniform(-obstruction_period_range,obstruction_period_range)
                        if best_individual[j][1]["obstruction period"] < obstruction_period_min:
                            best_individual[j][1]["obstruction period"] = obstruction_period_min
                        elif best_individual[j][1]["obstruction period"] > obstruction_period_max:
                            best_individual[j][1]["obstruction period"] = obstruction_period_max
                        #print("2: best_individual[j][1][obstruction period]",best_individual[j][1]["obstruction period"])
                    elif k == 4:
                        adjusted_weight = r.uniform(-weight_range,weight_range)
                        for edges in (G_.adj[j]):
                            for s in range(node_amount):
                                if (best_weight[s][0] == j) and (best_weight[s][1] == edges):
                                    #print("BEFORE node: ",j,"edges: ",edges,"best_weight[s][2]: ",best_weight[s][2])
                                    best_weight[s] = list(best_weight[s])
                                    best_weight[s][2] = float(adjusted_weight)
                                    if best_weight[s][2] < weight_min:
                                        best_weight[s][2] = float(weight_min)
                                    elif best_weight[s][2] > weight_max:
                                        best_weight[s][2] = float(weight_max)
                                    #print("AFTER node: ",j,"edges: ",edges,"best_weight[s][2]: ",best_weight[s][2])
                            #print("best_weight[1]: ",best_weight[1])
            '''for k in (G_.adj[j]):
                if r.random() <= 0.01:
                    print("node: ",j,"adj items: ",G_.adj[j],"k: ",k)
                t.sleep(3)'''
        mutated_population[i] = best_individual
        edge_list[best_match] = best_weight
        #print("best_weight: ",best_weight)
        
        #print("Mutated population[0]                          : ",mutated_population[0])
        #print("Mutated population[1]                          : ",mutated_population[1])
        #print("Mutated population[2]                          : ",mutated_population[2])
        #t.sleep(20)
    return mutated_population, edge_list


"""
P R O G R A M
"""

if __name__ == '__main__':
    for _ in range(100):
        # Initialise
        t0 = t.perf_counter()
        
        
        ###
        decay_min = 0.0001
        decay_max = 5
        decay_percent_of_max = 0.1
        decay_range = (decay_max)*decay_percent_of_max
        threshold_min = 0.5
        threshold_max = 5
        threshold_percent_of_max = 0.1
        threshold_range = (threshold_max)*threshold_percent_of_max
        prob_selffire_min = 0.000001
        prob_selffire_max = 0.01
        prob_selffire_percent_of_max = 0.1
        prob_selffire_range = (prob_selffire_max)*prob_selffire_percent_of_max
        obstruction_period_min = 0.003 
        obstruction_period_max = 5
        obstruction_period_percent_of_max = 0.1
        obstruction_period_range = (obstruction_period_max)*obstruction_period_percent_of_max
        weight_min = 0.01
        weight_max = 1
        weight_percent_of_max = 0.1
        weight_range = (weight_max)*weight_percent_of_max
        # could be declared in initialise() and returned
    
    

        nodeamount, populationsize, G, edgelist, trialname = network_initialise()
        generation = init_generation(nodeamount,populationsize)
    

        

        # Update
        nr_of_generations = 25
        generation_nr = 0
        trial_nr = 0
        fitnesscore = 900000

        print("Trial version: ",trial_nr)
        for _ in range(nr_of_generations):
            t1 = t.perf_counter()
    
            if generation_nr == 0:
                print("Initial generation")
                '''parameter_progress_file = open("data\parameter_progress.txt","w")
                parameter_progress_file.write("Initial generation:\n")
                parameter_progress_file.close()'''
            else:
                print("Generation: ",generation_nr)
                '''parameter_progress_file = open("data\parameter_progress.txt","a")
                parameter_progress_file.write("\n --------------------\n Generation number: "+str(generation_nr)+"\n ---------------------\n")
                parameter_progress_file.close()'''


            #phenotype = phenotype_generator(G,generation,edgelist,populationsize)
            args = multiprocessor.multi_variables(G,generation,populationsize,edgelist)
            phenotype = multiprocessor.multiprocessor(args)
            #print("generation_nr: ",generation_nr,"name: ",__name__)
            

            t2 = t.perf_counter()
            bestmatch, fitnesscore = fit.pick_best_rule_set(phenotype)
            
            print("Best match: ",bestmatch, "fitnesscore: ",fitnesscore)
            file_write.phenotype_file(fitnesscore,generation_nr,trialname,trial_nr,bestmatch,phenotype)
            file_write.fitness_file(fitnesscore,generation_nr,trialname,trial_nr)

            if fitnesscore < 10:
                print("Fitnesscore is below 10. Starting new trial.")
                break
               
            generation, edgelist = mutation(generation,bestmatch,nodeamount,populationsize,G,edgelist)

            generation_nr += 1
            if generation_nr > 25:
                generation_nr = 0

        t3 = t.perf_counter()
        trial_nr +=1
        print("total elapsed time: ",round(t3-t0,2))
        '''f = open("Data\Best_spikes.txt", "w")
        for element in phenotype[bestmatch]:
            f.write(str(element[0]) + " " + str(element[1]) + '\n')
        f.close()'''
 
        """

        - Apply number of active electrodes in fitness function?
        - Fix weights

        """