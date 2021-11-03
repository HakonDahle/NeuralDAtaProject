import load_data as load
import copy
from multiprocessing import Pool
import os
import time as t


'''
This is the fitness-function methods that are used to evaluate the spikes created
'''

list_of_imported_spikes = load.get_data()  #imports spikes and times from Dense2-3-10 in two separate lists
imported_list_spike_time = load.get_time()

unused_electrodes_penalty = 5000           #Sets the value for the penalty given for each unused electrode

'''
Method that gets the simulated input and returns the
index of the best rule, and the fitness score of this rule
'''

def pick_best_rule_set(list_of_spikes):
    score = 10000000000
    best_rule = 0

    with Pool(os.cpu_count()-1 ) as p: #os.cpu_count()-1       #Making the best_fit method run at the same time, on different cpu's
        results = p.map(best_fit,list_of_spikes)
        p.close()

    for i in range(len(results)): 
        
        index = i

        if results[i] < score:
            score = results[i]
            best_rule = index

    return best_rule, score


def best_fit(sim_output):
    diff = abs(len(list_of_imported_spikes) - len(sim_output))
    diff += use_electrodes(sim_output)           #penalizes unused electrodes

    return diff

def best_fit_test(sim_output):
    # 0-59 seconds = 7408
    #0 - 2 seconds = 198
    #0 - 10 seconds 1187
    diff = abs(len(list_of_imported_spikes[:7408]) - len(sim_output))
    print("Length data: ",len(list_of_imported_spikes), "Length spikes: ",len(sim_output))
    diff += use_electrodes(sim_output)           #penalizes unused electrodes
    #print("len data[0-198]: ",len(spike_list_fasit),"len phenotype: ",len(sim_output))
    return diff

'''
Method that worsen the fitness score if many electrodes are unused
'''

def use_electrodes(list_of_electrodes):
    score = 0
    temp_list = copy.deepcopy(list_of_electrodes)
    print("temp_list: ",temp_list)
    t.sleep(20)
    for i in range(60):
        try:
            index = temp_list.index(i)
            print("Active: ",i)
            del temp_list[:index]
        except ValueError:
            print("Inactive: ",i)
            score += unused_electrodes_penalty

    print("Electrode score: ",score)
    return score












'''
THE METHODS UNDERNEATH ARE NOT BEING USED, BUT ARE A WAY OF GETTING THE FREQUENZY OF SPIKES IN A GIVEN INTERVAL
'''


def part_list_to_time_only(list):
    time = []
    time_each_rule = []
    for i in range(len(list)):
        for j in range(len(list[i])):
            time.append(list[i][j][0])
        tider = copy.deepcopy(time)
        time_each_rule.append(tider)
        time.clear()
    return time_each_rule

def part_list_to_sorted_electrodes_only(list):
    electrodes_temp = []
    electrodes_each_rule = []
    for i in range(len(list)):
        for j in range(len(list[i])):
            electrodes_temp.append(list[i][j][1])
        electrodes_temp.sort()
        electrodes = copy.deepcopy(electrodes_temp)
        electrodes_each_rule.append(electrodes)
        electrodes.clear()
    return electrodes_each_rule

def arrayWideSpikeDetectionRate(time,interval):
    t0 = 0 
    t1 = time[:]
    f = []
    spikes = 0   # number of spikes
    for element in range(len(time)):
        if t1[element] - t0 <= interval:
            spikes += 1
        elif t1[element] - t0 > interval:
            f.append(spikes/(t1[element]-t0))
            t0 = t1[element]
            spikes = 0
    return f

def get_fitness(list_of_times,interval):
    freq = []
    fasit_freq = arrayWideSpikeDetectionRate(imported_list_spike_time,interval)
    for i in range(len(list_of_times)):
        freq.append(arrayWideSpikeDetectionRate(list_of_times[i],interval))
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
        






