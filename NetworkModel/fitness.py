import load_data as load


# Calculates fire rate for the whole electrode array (spikes/t) 

spike_list_fasit = load.get_data()

#print(len(spike_list_fasit))

def best_fit(sim_output):
    diff = abs(len(spike_list_fasit) - len(sim_output))
    return diff

def best_fit_test(sim_output):
    # 0-59 seconds = 7408
    #0 - 2 seconds = 198
    diff = abs(len(spike_list_fasit[:198]) - len(sim_output))
    print("len data[0-198]: ",len(spike_list_fasit),)
    print("len phenotype: ",len(sim_output))
    return diff

def pick_best_rule_set(set_of_rules):
    score = 10000000000
    differanse = 0
    beste_regel = 0
    for i in range(len(set_of_rules)):
        
        index = i
        #print(f"antall spikes på regel {i} er {len(set_of_rules[i])}")
        differanse = best_fit_test(set_of_rules[i]) #           CHANGE THIS BACK
        #print(f"differansen på regel {i} er {differanse}")
        if differanse < score:
            score = differanse
            beste_regel = index
            #print(f"score er foreløbig {score}")
    return beste_regel, score


