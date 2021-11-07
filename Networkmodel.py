import random as r
import copy
import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.reportviews import EdgeDataView

# initialise
#genotype = {"decay": 0.5, "threshold": 1, "prob selffire": 0.2, "obstruction period": 0.3}

nodeamount = 60
populationsize = 2
range_selffire = 0.01,0.02  # can be added into the genotype

edgelist = [(0,1,1),(0,7,1),(1,2,1),(1,8,1),(2,3,1),(2,9,1),(3,4,1),(3,10,1),(4,5,1),(4,11,1),(5,12,1),
            (6,7,1),(6,14,1),(7,8,1),(7,15,1),(8,9,1),(8,16,1),(9,10,1),(9,17,1),(10,11,1),(10,18,1),(11,12,1),(11,19,1),(12,13,1),(12,20,1),(13,21,1),
            (14,15,1),(14,22,1),(15,16,1),(15,23,1),(16,17,1),(16,24,1),(17,18,1),(17,25,1),(18,19,1),(18,26,1),(19,20,1),(19,27,1),(20,21,1),(20,28,1),(21,29,1),
            (22,23,1),(22,30,1),(23,24,1),(23,31,1),(24,25,1),(24,32,1),(25,26,1),(25,33,1),(26,27,1),(26,34,1),(27,28,1),(27,35,1),(28,29,1),(28,36,1),(29,37,1),
            (30,31,1),(30,38,1),(31,32,1),(31,39,1),(32,33,1),(32,40,1),(33,34,1),(33,41,1),(34,35,1),(34,42,1),(35,36,1),(35,43,1),(36,37,1),(36,44,1),(37,45,1),
            (38,39,1),(38,46,1),(39,40,1),(39,47,1),(40,41,1),(40,48,1),(41,42,1),(41,49,1),(42,43,1),(42,50,1),(43,44,1),(43,51,1),(44,45,1),(44,52,1),(45,53,1),
            (46,47,1),(47,48,1),(47,54,1),(48,49,1),(48,55,1),(49,50,1),(49,56,1),(50,51,1),(50,57,1),(51,52,1),(51,58,1),(52,53,1),(52,59,1),
            (54,55,1),(55,56,1),(56,57,1),(57,58,1),(58,59,1)]
'''[(0,1,1),(0,7,1),(1,2,1),(1,8,1),(2,3,1),(2,9,1),(3,4,1),(3,10,1),(4,5,1)]''' # Test string


nodelist = [[0]*nodeamount]*populationsize
G = nx.Graph()

for i in range(populationsize):
    for j in range(nodeamount):
        nodelist[i][j] = (j,{"decay constant": r.uniform(0.0001,0.01), "threshold": r.uniform(2,3), "prob selffire": r.uniform(0.01,0.1), "obstruction period": r.uniform(0.05,0.3)  # Configurable variables
        ,"spike": 0, "prev spike": 0, "exhausted": 0, "potential": 0})   # Functional variables
# legges til nodelist.append og geotype etterpå: "spike": 0, "exhausted": 0, "potential": 0


G.add_weighted_edges_from(edgelist)

#print(G.nodes.data())

def phenotype_generator(G_,node_list,population_size):
    phenotype_temp = []
    phenotype_ = []
    fs = 50000
    time = 0
    for i in range(population_size):
        G_.add_nodes_from(node_list[i])
        '''G_.nodes[1]["spike"] = 1
        G_.nodes[2]["spike"] = 1
        G_.nodes[0]["potential"] = 0.5
        G_.edges[0,1]["weight"] = 1
        G_.edges[0,2]["weight"] = 1'''
        while time < 0.01:
            #print(time)
            for nodenr in range(len(node_list[i])):
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
                        phenotype_.append([float(time),nodenr])
                        #print("phenotype_: ",phenotype_)

                elif G_.nodes[nodenr]["exhausted"] < 0:
                    G_.nodes[nodenr]["exhausted"] = 0

                '''if (G_.nodes[nodenr]["potential"] >  G_.nodes[nodenr]["threshold"]) or ((r.uniform(0.01,0.2) <= G_.nodes[nodenr]["prob selffire"])):  # Node spikes if threshold is exceeded
                    G_.nodes[nodenr]["spike"] = 1
                    print("time: ",time)
                    phenotype_.append([float(time),nodenr])
                    G_.nodes[nodenr]["potential"] = 0
                    G_.nodes[nodenr]["exhausted"] = G_.nodes[nodenr]["obstruction period"]'''

                '''elif (r.uniform(0.01,0.2) <= G_.nodes[nodenr]["prob selffire"]) and (G_.nodes[nodenr]["exhausted"] == 0):
                    G_.nodes[nodenr]["spike"] = 1
                    G_.nodes[nodenr]["potential"] = 0
                    G_.nodes[nodenr]["exhausted"] = G_.nodes[nodenr]["obstruction period"]
                    phenotype_.append([float(time),nodenr])'''
                
                #print("node: ",nodenr,"potential: ",G_.nodes[nodenr]["potential"],"nbr_spike: ", G_.nodes[nbr]["spike"])
                #print("2",G_.nodes[nodenr])
                if G_.nodes[nodenr]["spike"] == 1:  # Resets spikes if there has been a spike in last iteration and deactivates the node
                    G_.nodes[nodenr]["prev spike"] = 1
                    G_.nodes[nodenr]["spike"] = 0
                    G_.nodes[nodenr]["exhausted"] = G_.nodes[nodenr]["obstruction period"]
                    G_.nodes[nodenr]["potential"] = 0
                    G_.nodes[nodenr]["exhausted"] = G_.nodes[nodenr]["obstruction period"]

            # add a function that checks if spike was 1 last iteration and sets it to 0
            # add a function that checks if threshold is reached if neighbours have fired and not exhausted
            # add a function that decrease the potential (decay)
            # add a function that nodes can selffire

            time += 1/fs
            
            '''# Drawing
            pos = nx.spring_layout(G_, iterations=300, seed=3977)
            color_map = []
            if G_.nodes[nodenr]['spike'] == 1:
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
        phenotype_.append(phenotype_temp)
    return phenotype_          

test = phenotype_generator(G,nodelist,populationsize)
print(test)
'''
# mutation
def mutation(graph,node_nr):
    for i in range(node_nr):
        for j in range(len(graph.nodes[i])):
            #print("length: ",len(graph.nodes[i]))
            if r.random() <= 0.5:
                if j == 0:
                    graph.nodes[i]["decay constant"] = r.uniform(0.01,0.5)
                elif j == 1:
                    graph.nodes[i]["threshold"] = r.uniform(0.5,1)
                elif j == 2:
                    graph.nodes[i]["prob_selffire"] = r.uniform(0.01,0.2)
                elif j == 3:
                    graph.nodes[i]["obstruction period"] = r.uniform(0.05,0.3)
    return graph
new_generation = mutation(G,nodeamount)
'''

'''
#print(G.nodes[1])
#print(G.edges([1]))
#print(G.degree[1])
G.nodes[1]['spike'] = 1
G.nodes[2]['rest'] = 0.3

print(G.nodes.data())

pos = nx.spring_layout(G, iterations=300, seed=3977)

color_map = []
for node in G:
    if G.nodes[node]['spike'] == 1:
        color_map.append('green')
    elif G.nodes[node]['rest'] > 0:
        color_map.append('red')
    else:
        color_map.append('gray')
nx.draw(
    G,
    pos,
    node_color=color_map,
    edgecolors="tab:gray",  # Node surface color
    edge_color="tab:gray",  # Color of graph edges
    node_size=100,
    with_labels=True,
    width=3,
)

plt.show()
'''