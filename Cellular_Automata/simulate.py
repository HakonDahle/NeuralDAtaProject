import pycxsimulator
from pylab import *
import random as r
import evolution as ev
import copy


width = 5
height = 5
initProb = 0.2 #sannsynlighet for å starte med spike
t = 0

#list_of_rule_sets = ev.create_list_of_n_rules(2,265)
list_of_spikes_rule_n = []
spikes_info = []
spikes_list = []


def initialize():
    global time, config, nextConfig

    time = 0
    
    config = zeros([height, width])
    for x in range(width):
        for y in range(height):
            if random() < initProb:
                state = 1
            else:
                state = 0
            config[y, x] = state

    print("Initialize")

    nextConfig = zeros([height, width])

def update(rule_set):
    global time, config, nextConfig, spikes_info

    time += 1
    #rule_set = rule_set[:]
    electrode_number = 0
    spikes_info = []

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            numberOfAlive = []

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    numberOfAlive.append(config[(y+dy)%height, (x+dx)%width])
            del numberOfAlive[5]

            num = 0
            for b in numberOfAlive:
                num = 2 * num + b
            num = int(num)
            #print(num) # 6
            #print(numberOfAlive) 

            state = int(rule_set[num])
            if state == 1:  
                #spike = [time, electrode_number]
                spike = electrode_number
                spikes_info.append(spike)

            numberOfAlive.clear()
            electrode_number += 1
            nextConfig[y, x] = state
            
    #rule_set = rule.mutate_rule_table(rule_set)
    config, nextConfig = nextConfig, config
    #return spikes_info

'''initialize()


for i in range(len(list_of_rule_sets)):
    while time < 10:
        update(list_of_rule_sets[i])
        copy_spikes = copy.deepcopy(spikes_info)
        
        for j in range(len(copy_spikes)):
            spikes_list.append([time,copy_spikes[j]])
        spikes_info.clear()
        
    spikes_list_copy = copy.deepcopy(spikes_list)
  
    list_of_spikes_rule_n.append(spikes_list_copy)
   
    spikes_list.clear()
    time = 0
'''


def simulate(list_of_rule_sets):
    global time, config, nextConfig, spikes_info
    
    initialize()

    for i in range(len(list_of_rule_sets)):
        while time < 10:
            update(list_of_rule_sets[i])
            copy_spikes = copy.deepcopy(spikes_info)
            
            for j in range(len(copy_spikes)):
                spikes_list.append([time,copy_spikes[j]])
            spikes_info.clear()
        
        spikes_list_copy = copy.deepcopy(spikes_list)
  
        list_of_spikes_rule_n.append(spikes_list_copy)
   
        spikes_list.clear()
        time = 0

    return list_of_spikes_rule_n


