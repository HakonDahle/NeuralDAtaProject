
from pylab import *
import random as r
import evolution as ev
import copy
import concurrent.futures
import numpy as np


#Her kan du endre tiden i update() time+= xx, den står nå på 0.01, skal vel stå på 0.00002
#i simulate() må du endre while time < 100 til det den skal stå på.

width = 5
height = 5
initProb = 0.2 #sannsynlighet for å starte med spike
sec_to_run = 10
update_freq = 1
t = 0


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

def update_MP(rule_set,time,config,nextConfig):
    time += update_freq
    electrode_number = 0
    spikes_info = []
    #print(f"dette er config: {config}")
    #print(f"den er: {np.ndim(config)} dimensjoner")

    for x in range(width):
        for y in range(height):
            #print(f"posisjon x: {x} posisjon y: {y}")
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
    return spikes_info,time,config,nextConfig

def simulate_MP(list_of_rule_sets):
    global time, config, nextConfig

    initialize()
    print(f"list of rule sets er {len(list_of_rule_sets)} lang")
    #print(config)
    #print(f"den er: {np.ndim(config)} dimensjoner")
    '''with concurrent.futures.ProcessPoolExecutor() as executor:
        list_of_spikes_rule_n = (executor.map(simulate,list_of_rule_sets))
        print(f"list_o_s_r_n er av type {type(list_of_spikes_rule_n)}")
        return_list = list(list_of_spikes_rule_n)
        print(f"return list er {type(return_list)}")'''
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for rules in range(len(list_of_rule_sets)):
            future = executor.submit(sim_MP(list_of_rule_sets[rules],config,nextConfig))
            kopi = copy.deepcopy(future)
            print(f"future er {type(kopi)}")
            list_of_spikes_rule_n.append(kopi.result())
        #list_of_spikes_rule_n = executor.map(sim_MP,list_of_rule_sets,config,nextConfig)
        liste = list_of_spikes_rule_n
        #print(f"lista er av typen {type(liste)} og er {len(liste)} lang")
        return_list = liste
    return return_list   #concurrent.futures.Future.result

def sim_MP(rule_set,config,nextConfig):
    time = 0
    #print(config)
    #print(f"Nå er config : {np.ndim(config)} dimensjoner")
    while time < sec_to_run:
        spikes_info, time, config, nextConfig = update_MP(rule_set, time,config,nextConfig)
        copy_spikes = copy.deepcopy(spikes_info)
        #print(f"config er {config}")

        for j in range(len(copy_spikes)):
            spikes_list.append([time,copy_spikes[j]])
        spikes_info.clear()

    #spikes_list_copy = copy.deepcopy(spikes_list)
    #spikes_list.clear()
    return spikes_list
    



def simulate(list_of_rule_sets):
    global time, config, nextConfig, spikes_info
    
    initialize()

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


