import networkx as nx
import copy
import random as r
from multiprocessing import Pool
import multiprocessing as multi
import os


# Launching parallell processes for spike data generation
def multiprocessor(args):
    
    with Pool(os.cpu_count()-1) as p:
        results = p.map(multi_phenotype_generator,args)
        p.close()
    return results


# Setting up an environment where the network model can function and produce spikes
def multi_phenotype_generator(G_):
    
    if __name__ == 'simulation':

        current_process = multi.current_process()   # Acquires the name of the process
        
        print("Process initialising: ",current_process.name)

        phenotype_ = []
        fs = 1000   # Sampling frequency
        time = 0

        selffire_count = 0  # Used for analysing network behaviour
        potential_count = 0 # Used for analysing network behaviour
        time_limit = 1800   # Max run time in seconds
        sec = 0
        time_control = 0
        
        # Simulation is running until the time limit is reached
        while time < time_limit:

            color_map = []

            # Iterating through every node in the network to check and update their values
            for nodenr in range(len(G_)):

                self_prob = r.random()  # Used to simulate if a node is self spiking
                
                # Checks if the node has a voltage potential to decrease it with the decay constant
                if G_.nodes[nodenr]["potential"] > 0:   
                    G_.nodes[nodenr]["potential"] -= G_.nodes[nodenr]["decay constant"]
                elif G_.nodes[nodenr]["potential"] < 0:
                    G_.nodes[nodenr]["potential"] = 0
                
                # Exhausted nodes are inactive for a period of time
                if G_.nodes[nodenr]["exhausted"] > 0:   
                    G_.nodes[nodenr]["exhausted"] -= 1/fs
                    color_map.append('red') # For visualisation purposes
                
                # If the node is active the voltage potential will increase if neighbours are spiking, and the node will spike if the voltage threshold is reached.
                # Then the node will enter a refraction period and become inactive
                elif G_.nodes[nodenr]["exhausted"] == 0:
                    
                    # Checks the neighbours for spikes and multiplies it with the weighted edge
                    for k, nbrs in G_.adj.items():  
                        if k == nodenr:

                            # The potential is increased by the sum of neighbouring spikes times the weight of the edge
                            for nbr, eattr in nbrs.items():
                                G_.nodes[nodenr]["potential"] += G_.nodes[nbr]["prev spike"]*eattr["weight"]
                            
                            # The node spikes if the threshold is reached
                            if G_.nodes[nodenr]["potential"] >  G_.nodes[nodenr]["threshold"]:
                                G_.nodes[nodenr]["spike"] = 1
                                phenotype_.append([float(time),nodenr]) # Timestamp and node nr is added to the data list
                                potential_count += 1    # Counter used for network model performance analysis 
                                
                                # This loop is used to update the weights according to "cells that fire together wire together"
                                # This means that if a neighbour influence the node into spiking then the bonds are strengthened and the weight increase
                                for k, nbrs in G_.adj.items():
                                    if k == nodenr:
                                        for nbr, eattr in nbrs.items():
                                            if (G_.nodes[nbr]["prev spike"] == 1) and (G_.nodes[nodenr]["spike"] == 1) and (G_.edges[nodenr,nbr]["weight"] < 1):
                                                G_.edges[nodenr,nbr]["weight"] = G_.edges[nodenr,nbr]["weight"]   # SETS EQUAL TO ITSELF TO HAVE STATIC WEIGHTS!!!! OLD: G_.edges[nodenr,nbr]["weight"] += 0.05

                        # There is a small chance that the node will self spike
                        if (self_prob <= G_.nodes[nodenr]["prob selffire"]) and (G_.nodes[nodenr]["spike"] == 0):
                            G_.nodes[nodenr]["spike"] = 1
                            phenotype_.append([float(time),nodenr]) # Timestamp and node nr is added to the data list
                            selffire_count += 1     # Counter used for network model performance analysis     

                # Makes sure the node returns to its active state
                elif G_.nodes[nodenr]["exhausted"] < 0:
                    G_.nodes[nodenr]["exhausted"] = 0
                
                # If the node spiked: Resets spikes, returning voltage potential to 0, put node into refraction, 
                if G_.nodes[nodenr]["spike"] == 1:  
                    G_.nodes[nodenr]["prev spike"] = 1
                    color_map.append('yellow')  # For visualisation purposes
                    G_.nodes[nodenr]["spike"] = 0
                    G_.nodes[nodenr]["exhausted"] = G_.nodes[nodenr]["obstruction period"]
                    G_.nodes[nodenr]["potential"] = 0
                
                # Resets spikes from previous iteration
                elif G_.nodes[nodenr]["prev spike"] == 1:
                    G_.nodes[nodenr]["prev spike"] = 0
                
                # this is only for visualisation, to indicate a node in rest ready to spike
                if (G_.nodes[nodenr]["prev spike"] == 0) and (G_.nodes[nodenr]["spike"] == 0) and (G_.nodes[nodenr]["exhausted"] == 0):
                    color_map.append('gray')    # For visualisation purposes
            
            time += 1/fs    # incrementing time according to the sampling frequency
            
            # This is to occationaly give vital signs that the simulation has not crashed
            if (time - time_control) > 120.01:
                sec += 120
                time_control = time

                print(sec," seconds has passed.")
                
            #nm.net_visualisation(G_,len(G_),time,color_map)    # Can be used for visualising the spikes in the network    
    
    print("Amount of selfspikes: ",selffire_count, "Amount of potential spikes: ", potential_count)
    
    return phenotype_