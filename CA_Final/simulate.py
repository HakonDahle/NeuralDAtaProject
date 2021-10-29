from multiprocessing import Pool
import os
from pylab import *
import copy
from functools import partial
import numpy as np

'''
This is the program containing the simulation of spikes
It has two versions, one with multiprocessing, and one without. 
It is the multiprocessing one that is the most suitable for this process.
'''

#Setting initial conditions. Height and Width of the grid, 
# how long to run the simulation, and the update frequenzy
width = 8
height = 8
initProb = 0.2 #probability for electrode in grid to start active
sec_to_run = 180
update_freq = 1
t = 0


list_of_spikes_rule_n = []
spikes_info = []
spikes_list = []

'''
Method that creates the grid with initial conditions set above.
'''

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



'''
Multiprocessing verson of simulate() and update()
'''

'''
Running the method sim_MP on several cpu's 
The method encapsulates the global variables config and nextConfig so that the different processes won't interfere with each other
Returning a list containing the spikes for each rule set'''
def simulate_MP(list_of_rule_sets):
    global time, config, nextConfig

    part_sim_MP = partial(sim_MP,config=config,nextConfig=nextConfig)

    with Pool(4) as p: #os.cpu_count()-1
        results = p.map(part_sim_MP,list_of_rule_sets)
        p.close()
    return results

'''
Running the update function for the given preferred time period
Returning a list with time and electrode number for each spike on the given rule set'''
def sim_MP(rule_set,config,nextConfig): 
    time = 0
    
    while time < sec_to_run:
        spikes_info, time, config, nextConfig = update_MP(rule_set, time,config,nextConfig)
        copy_spikes = copy.deepcopy(spikes_info)
       

        for j in range(len(copy_spikes)):
            spikes_list.append([time,copy_spikes[j]])
        spikes_info.clear()

    return spikes_list

def update_MP(rule_set,time,config,nextConfig):
    time += update_freq
    electrode_number = 0
    spikes_info = []


    for x in range(width):
        for y in range(height):
            state = config[y, x]
            numberOfAlive = []
            #registers the states of the surrounding electrodes
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    numberOfAlive.append(config[(y+dy)%height, (x+dx)%width])
            del numberOfAlive[5] # deletes itself

            #converting the list of sorrunding states to int via binary
            num = 0
            for b in numberOfAlive:
                num = 2 * num + b
            num = int(num)
        
            #Sets the state of given electrode to state given by rule set
            state = int(rule_set[num])
            if state == 1:  
                spike = electrode_number
                spikes_info.append(spike)

            numberOfAlive.clear()
            electrode_number += 1
            nextConfig[y, x] = state
            
    config, nextConfig = nextConfig, config
    return spikes_info,time,config,nextConfig



'''
Simulate and update method for single processing
'''

def simulate(list_of_rule_sets):
    global time, config, nextConfig, spikes_info
    

    for i in range(len(list_of_rule_sets)):
        while time < sec_to_run:
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

def update(rule_set):
    global time, config, nextConfig, spikes_info

    time += update_freq
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

            state = int(rule_set[num])
            if state == 1:  
                spike = electrode_number
                spikes_info.append(spike)

            numberOfAlive.clear()
            electrode_number += 1
            nextConfig[y, x] = state
            
    config, nextConfig = nextConfig, config





'''
Method Not used in final code
'''
    
def encapsulate_args(rules,config,nextConfig):
    encapsulated_args = []
    config_list = []
    nextConfig_list = []
    encapsulated_args.append(rules)
    for i in range(len(rules)):
        config_list.append(config)
    encapsulated_args.append(config_list)
    for i in range(len(rules)):
        nextConfig_list.append(nextConfig)
    encapsulated_args.append(nextConfig_list)
    numpy_array = np.array(encapsulated_args)
    transposed = numpy_array.T

    return transposed

