import load_data as load
import copy


# Calculates fire rate for the whole electrode array (spikes/t)

spike_list_fasit = load.get_data()
spike_list_time = load.get_time()

#print(spike_list_time)

#print(len(spike_list_fasit))

def best_fit(sim_output):
    diff = abs(len(spike_list_fasit) - len(sim_output))
    return diff

def pick_best_rule_set(set_of_rules):
    score = 10000000000
    differanse = 0
    beste_regel = 0
    for i in range(len(set_of_rules)):
        
        index = i
        #print(f"antall spikes på regel {i} er {len(set_of_rules[i])}")
        differanse = best_fit(set_of_rules[i])
        #print(f"differansen på regel {i} er {differanse}")
        if differanse < score:
            score = differanse
            beste_regel = index
            #print(f"score er foreløbig {score}")
    return beste_regel, score

def part_list_to_time_only(list):
    time = []
    time_each_rule = []
    #print(f"liste er {len(liste)} lang") 
    for i in range(len(list)):
        for j in range(len(list[i])):
            #print(f"halåå{liste[i][j][0]}")
            time.append([list[i][j][0]])
        tider = copy.deepcopy(time)
        time_each_rule.append(tider)
        time.clear()
    return time_each_rule

def arrayWideSpikeDetectionRate(time,interval):
    t0 = 0 
    t1 = time[:]
    f = []
    #interval = 0.1
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
    for i in range(len(list_of_times)):
        freq.append(arrayWideSpikeDetectionRate(list_of_times[i],interval))
    
    return(freq, fasit_freq)






