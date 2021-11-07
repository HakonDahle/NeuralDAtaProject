import load_data as load


spike_list_fasit = load.get_data()  # Loads reference data

# Used for testing to speed up the phenotype generation
def best_fit_test(sim_output):
    # 0-59 seconds = 7408
    #0 - 2 seconds = 198
    #0 - 10 seconds 1187
    diff = abs(len(spike_list_fasit[:7408]) - len(sim_output))
    #print("len data[0-198]: ",len(spike_list_fasit),"len phenotype: ",len(sim_output))
    return diff


# Evaluation criteria. Looks at the difference between number of spikes in reference data adn in generated data
# The lower the score, the better the performance
def best_fit(sim_output):
    diff = abs(len(spike_list_fasit) - len(sim_output))
    return diff


# Fitness function selecting the best individual based on the evaluation criteria.
def pick_best_rule_set(set_of_rules):
    score = 10000000000
    differanse = 0
    beste_regel = 0

    for i in range(len(set_of_rules)):
        
        index = i
        differanse = best_fit(set_of_rules[i])
        if differanse < score:
            score = differanse
            beste_regel = index

    return beste_regel, score
