import networkx as nx
import copy
import file_write
import random as r
from multiprocessing import Pool
import multiprocessing as multi
import time as t
import os
import Networkmodel as nm

def multiprocessor(args):
    population_size = args[0][2]
    G_ = args[0][1]
    arguments = [[]]*population_size
    gen_temp = []
    edge_temp = []
    for i in range(len(args)):
        population_size = args[i][2]
        G_ = args[i][1]
        gen_temp.append(args[i][0])
        edge_temp.append(args[i][3])
        gen = copy.deepcopy(gen_temp)
        edge = copy.deepcopy(edge_temp)
        arguments[i] = gen,G_,population_size, edge
        gen_temp.clear()
        edge_temp.clear()
        #print("arguments: ",arguments)
    
    with Pool(os.cpu_count()-1) as p:
        results = p.map(multi_phenotype_generator,arguments)
        p.close()
    return results

def multi_variables(G_,gen,population_size,edge_list):
    args = []
    for i in range(population_size):
        args.append([gen[i],G_,population_size,edge_list[i]])
    return args



def multi_phenotype_generator(params):
    if __name__ == 'multiprocessor':
        
        current_process = multi.current_process()
        
        print("Process initialising: ",current_process.name)
        print("currentprocess: ",multi.current_process())
        phenofilepath = file_write.generate_pheno_file(nm.trial_nr,nm.generation_nr,nm.trialname,current_process)

        population_size = params[2] # this can be removed
        G_ = params[1]
        gen = params[0]
        edges = params[3]
        '''print("nodes: ",gen,"\n")
        print("gen[0]",gen[0],"\n\n")
        print("edges: ",edges,"\n")
        print("edges[0]: ",edges[0])'''
        phenotype_ = []
        fs = 114
        time = 0
        G_.add_nodes_from(gen[0])
        G_.add_weighted_edges_from(edges[0])
        selffire_count = 0
        potential_count = 0 
        time_limit = 60
        sec = 0
        time_control = 0
        
        while time < time_limit:
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
                    
                    for k, nbrs in G_.adj.items():  # Checks the neighbours for spikes and multiplies it with the weighted edge
                        if k == nodenr:
                            
                            for nbr, eattr in nbrs.items():
                                #print("1: G_.nodes",[nodenr],"[potential]", G_.nodes[nodenr]["potential"])
                                G_.nodes[nodenr]["potential"] += G_.nodes[nbr]["prev spike"]*eattr["weight"]
                                #print("1: G_.nodes",[nodenr],"[potential]", G_.nodes[nodenr]["potential"])
                            if G_.nodes[nodenr]["potential"] >  G_.nodes[nodenr]["threshold"]:
                                G_.nodes[nodenr]["spike"] = 1
                                phenotype_.append([float(time),nodenr])
                                potential_count += 1  
                                for k, nbrs in G_.adj.items():  # Checks the neighbours for spikes and multiplies it with the weighted edge
                                    if k == nodenr:
                                        #print("G_.adj[nodenr]: ",G_.adj[nodenr])
                                        #t.sleep(1)
                                        for nbr, eattr in nbrs.items():
                                            if (G_.nodes[nbr]["prev spike"] == 1) and (G_.nodes[nodenr]["spike"] == 1) and (G_.edges[nodenr,nbr]["weight"] < 1):
                                                #print("nodenr: ",nodenr,"nbr: ",nbr,"G_.edges[nodenr,nbr][ weight]: ",G_.edges[nodenr,nbr]["weight"])
                                                G_.edges[nodenr,nbr]["weight"] += 0.05 #G_.edges[nodenr,nbr]["weight"]  SETS EQUAL TO ITSELF TO HAVE STATIC WEIGHTS!!!!
                                                #print("G_.edges[nodenr,nbr][ weight]: ",G_.edges[nodenr,nbr]["weight"])
                                    #print("SINGLE: i: ",i,"node: ",nodenr,"nbrs: ",nbrs,"nbr: ",nbr,"fire_wire: ", fire_wire)             
                                #print("nodenr: ",nodenr,"potential: ",G_.nodes[nodenr]["potential"],"nbr: ",nbr,"nbr_prev_spike: ", G_.nodes[nbr]["prev spike"])
                        if (self_prob <= G_.nodes[nodenr]["prob selffire"]) and (G_.nodes[nodenr]["spike"] == 0):
                            G_.nodes[nodenr]["spike"] = 1
                            phenotype_.append([float(time),nodenr])
                            selffire_count += 1       
                    #print("time: ",time, "potential: ", G_.nodes[nodenr]["potential"],"threshold: ",G_.nodes[nodenr]["threshold"], "self_prob: ",self_prob,"selffire: ",G_.nodes[nodenr]["prob selffire"])
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
            
            if (time - time_control) > 120.01:
                sec += 120
                time_control = time

                print(sec," seconds has passed.")
                
                file_write.write_pheno_file(phenofilepath,phenotype_)
                phenotype_.clear()
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
    #print("selffire_count: ",selffire_count, "potential_count: ",potential_count)
    #print("G_.edges.data()",G_.edges.data('weight'))
    #print("Process terminating")
    print("Amount of selfspikes: ",selffire_count, "Amount of potential spikes: ", potential_count)
    return phenotype_

    '''elif G_.nodes[nodenr]["exhausted"] == 0:
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
                        #print("i: ",i,"phenotype_temp: ",phenotype_temp)'''