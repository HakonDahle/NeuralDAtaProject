import load_data as load
import copy
from multiprocessing import Pool
import os


# Calculates fire rate for the whole electrode array (spikes/t)

spike_list_fasit = load.get_data()
spike_list_time = load.get_time()

#print(spike_list_time)

#print(len(spike_list_fasit))

def best_fit(sim_output):
    diff = abs(len(spike_list_fasit) - len(sim_output))
    diff += use_electrodes(sim_output)

    return diff

def pick_best_rule_set(set_of_rules):
    score = 10000000000
    #differanse = 0
    beste_regel = 0

    with Pool(os.cpu_count()-1) as p: #Pool(2) as p:
        results = p.map(best_fit,set_of_rules)
        p.close()
    '''print("xxxxxxxxxxxxxxxxxxxxxxx")
    print(f"pool-results: {results}")'''
    for i in range(len(results)): #result in results:
        
        index = i
        #print(f"antall spikes på regel {i} er {len(set_of_rules[i])}")
        #differanse = best_fit(set_of_rules[i])
        #print(f"differansen på regel {i} er {differanse}")
        if results[i] < score:
            score = results[i]
            beste_regel = index
            #print(f"score er foreløbig {score}")

    '''print(f"beste regel: {beste_regel}, score: {score}")
    print("xxxxxxxxxxxxxxxxxxxxxxx")'''

    return beste_regel, score

def part_list_to_time_only(list):
    time = []
    time_each_rule = []
    #print(f"liste er {len(liste)} lang") 
    for i in range(len(list)):
        for j in range(len(list[i])):
            #print(f"halåå{liste[i][j][0]}")
            time.append(list[i][j][0])
        tider = copy.deepcopy(time)
        time_each_rule.append(tider)
        time.clear()
    return time_each_rule

def part_list_to_sorted_electrodes_only(list):
    electrodes_temp = []
    electrodes_each_rule = []
    #print(f"liste er {len(liste)} lang") 
    for i in range(len(list)):
        for j in range(len(list[i])):
            #print(f"halåå{liste[i][j][0]}")
            electrodes_temp.append(list[i][j][1])
        electrodes_temp.sort()
        electrodes = copy.deepcopy(electrodes_temp)
        electrodes_each_rule.append(electrodes)
        electrodes.clear()
    return electrodes_each_rule

def use_electrodes(list_of_electrodes):
    score = 0
    temp_list = copy.deepcopy(list_of_electrodes)
    for i in range(64):
        try:
            index = temp_list.index(i)
            del temp_list[:index]
            #print(index)
        except ValueError:
            score += 5000
            #print(f"inneholder ikke tallet {i}")
    return score

def arrayWideSpikeDetectionRate(time,interval):
    t0 = 0 
    t1 = time[:]
    f = []
    #interval = 0.1
    #print("det går denne gangen")
    #print(time)
    spikes = 0   # number of spikes
    for element in range(len(time)):
        if t1[element] - t0 <= interval:
            spikes += 1
            #print("IF: element: ",element,"spikes: ",spikes)
        elif t1[element] - t0 > interval:
            f.append(spikes/(t1[element]-t0))
            t0 = t1[element]
            spikes = 0
    return f

def get_fitness(list_of_times,interval):
    freq = []
    fasit_freq = arrayWideSpikeDetectionRate(spike_list_time,interval)
    #print("fasit ingen problem")
    for i in range(len(list_of_times)):
        #print(f"gang nr {i} starter")
        freq.append(arrayWideSpikeDetectionRate(list_of_times[i],interval))
        #print(f"gang nr {i} slutter")
    return(freq, fasit_freq)


def freq_fit(list_of_times,interval):
    fitness_score = 0
    best_score = 10000000000
    index_best_rule = 0
    spike_rule_time, real_spike_time = get_fitness(list_of_times,interval)
    for rule in spike_rule_time:
        for f in range(len(real_spike_time)):
            fitness_score += abs(real_spike_time[f]-spike_rule_time[rule][f])
        if fitness_score < best_score:
            best_score = fitness_score
            index_best_rule = rule
        else:
            fitness_score = 0
    return index_best_rule,best_score
        






