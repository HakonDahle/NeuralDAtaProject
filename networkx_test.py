import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.reportviews import EdgeDataView


nodelist = range(60)
edgelist = [(0,1),(0,7),(1,2),(1,8),(2,3),(2,9),(3,4),(3,10),(4,5),(4,11),(5,12),
            (6,7),(6,14),(7,8),(7,15),(8,9),(8,16),(9,10),(9,17),(10,11),(10,18),(11,12),(11,19),(12,13),(12,20),(13,21),
            (14,15),(14,22),(15,16),(15,23),(16,17),(16,24),(17,18),(17,25),(18,19),(18,26),(19,20),(19,27),(20,21),(20,28),(21,29),
            (22,23),(22,30),(23,24),(23,31),(24,25),(24,32),(25,26),(25,33),(26,27),(26,34),(27,28),(27,35),(28,29),(28,36),(29,37),
            (30,31),(30,38),(31,32),(31,39),(32,33),(32,40),(33,34),(33,41),(34,35),(34,42),(35,36),(35,43),(36,37),(36,44),(37,45),
            (38,39),(38,46),(39,40),(39,47),(40,41),(40,48),(41,42),(41,49),(42,43),(42,50),(43,44),(43,51),(44,45),(44,52),(45,53),
            (46,47),(47,48),(47,54),(48,49),(48,55),(49,50),(49,56),(50,51),(50,57),(51,52),(51,58),(52,53),(52,59),
            (54,55),(55,56),(56,57),(57,58),(58,59)]

G = nx.Graph()
G.add_nodes_from(nodelist, decay = 0.5, threshold = 1, prob_selffire = 0.2,spike = 0, rest = 0)
G.add_edges_from(edgelist)

print(G.nodes[1])
print(G.edges([1]))
print(G.degree[1])
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