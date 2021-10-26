import networkx as nx
import copy
import random as r
from multiprocessing import Pool
import os

def multiprocessor(args):
    population_size = args[0][2]
    G_ = args[0][1]
    arguments = [[]]*population_size
    gen_temp = []
    for i in range(len(args)):
        population_size = args[i][2]
        G_ = args[i][1]
        gen_temp.append(args[i][0])
        gen = copy.deepcopy(gen_temp)
        arguments[i] = gen,G_,population_size
        gen_temp.clear()
        #print("arguments: ",arguments)
    
    with Pool(os.cpu_count()-1) as p:
        results = p.map(multi_phenotype_generator,arguments)
        p.close()
    return results

def multi_variables(G_,gen,population_size):
    args = []
    for i in range(population_size):
        args.append([gen[i],G_,population_size])
    return args



def multi_phenotype_generator(params):
    if __name__ == 'multiprocessor':
        population_size = params[2] # this can be removed
        G_ = params[1]
        gen = params[0]
        phenotype_ = []
        fs = 50000
        time = 0
        G_.add_nodes_from(gen[0])
        while time < 0.01:
            for nodenr in range(len(gen[0])):
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

                    for k,nbrs in G_.adj.items():  # Checks the neighbours for spikes and multiplies it with the weighted edge
                        for nbr, eattr in nbrs.items():
                            G_.nodes[nodenr]["potential"] += G_.nodes[nbr]["prev spike"]*eattr["weight"]
                            #print("nodenr: ",nodenr,"potential: ",G_.nodes[nodenr]["potential"],"nbr: ",nbr,"nbr_prev_spike: ", G_.nodes[nbr]["prev spike"])
                    if (G_.nodes[nodenr]["potential"] >  G_.nodes[nodenr]["threshold"]) or ((self_prob <= G_.nodes[nodenr]["prob selffire"])):  # Node spikes if threshold is exceeded
                        G_.nodes[nodenr]["spike"] = 1
                        #print("time: ",time, "potential: ", G_.nodes[nodenr]["potential"],"threshold: ",G_.nodes[nodenr]["threshold"], "self_prob: ",self_prob,"selffire: ",G_.nodes[nodenr]["prob selffire"])
                        phenotype_.append([float(time),nodenr])
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
    return phenotype_