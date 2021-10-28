import random as r
import simulate as sim
import fitness as fit
import time
import copy

'''
Select number of rules to make for each generation.
Set wished fitness score.
'''

number_of_rules = 7
preferred_fitness_score = 15000

'''
Methods creating rule table and lists of rule tables
'''

def create_rule_table(length):
    rule_table = []
    for i in range(length):
        if r.random() < 0.8: #probability of a 0 in the rule table
            rule_table.append(0)
        else:
            rule_table.append(1)
    return rule_table

def create_list_of_n_rules(n,rule_length):  #how many rules, and how long rules(2^8 --> 256 defult)
    rule_list = []
    for _ in range(n):
        rule_list.append(create_rule_table(rule_length))
    return rule_list

'''
Method mutating given list to preferred number of new lists
'''
def create_mutated_list_of_rules(rule_table_to_mutate,number_of_rule_tables):
    mutated_list_of_rules = []
    for i in range(number_of_rule_tables):
        mutated_rule_temp = rule_table_to_mutate[:]
        for j in range(len(mutated_rule_temp)):
            if r.random() <= 0.1:            #probabillity of mutating each bit
                if mutated_rule_temp[j] == 0:
                    mutated_rule_temp[j] = 1
                else:
                    mutated_rule_temp[j] = 0
        mutated_rule = copy.deepcopy(mutated_rule_temp)
        mutated_list_of_rules.append(mutated_rule)
        mutated_rule_temp.clear()


    return mutated_list_of_rules

    
    
'''
Main method - setting up the grid before entering while-loop which runs
until preferred fitness score is reached.
Set up running the simulate_MP method that uses multiprocessing.
Can be run without multiprocessing, then you must change simulate_MP to simulate two places underneath.
'''


if __name__ == '__main__':

    generation = 0
    list_of_rule_sets = create_list_of_n_rules(number_of_rules,256) #Creating rules

    sim.initialize() #Method for setting up the grid of electrodes
    fitness_score = 1000000000 # Setting the fitness score high, so it won't interfere in the beginning.
    
    t1 = time.perf_counter()
    sim_output = sim.simulate_MP(list_of_rule_sets) #Generate spikes based on the given rules of this generation
    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
    
    t11 = time.perf_counter()
    best_rule, fitness_score = fit.pick_best_rule_set(sim_output) #Running the results from the spike-sim through our fitness function
    t22 = time.perf_counter()
    print(f'Mutation finished in {t22-t11} seconds')
    print(f"The best rule is rule number: {best_rule}")
    print(f"The fitness score is {fitness_score}")
    print(f"This is generation number {generation}")
    print("----------")
  
    sim_output.clear()                      
    mutated_set_of_rules = create_mutated_list_of_rules(list_of_rule_sets[best_rule],number_of_rules)

    '''
    Method that runs until preferred fitness score is reached
    '''

    while fitness_score > preferred_fitness_score: 
        t1 = time.perf_counter() 
        sim_output = []
        sim_output = sim.simulate_MP(mutated_set_of_rules) ##Generate spikes based on the given rules of this generation
        t2 = time.perf_counter()
        print(f'Finished in {t2-t1} seconds')
    
        t10 = time.perf_counter()
        best_rule, fitness_score = fit.pick_best_rule_set(sim_output) #Running the results from the spike-sim through our fitness function
        t11 = time.perf_counter()
        
        generation += 1
        
        print(f'Mutation finished in {t11-t10} seconds')
        print(f"The best rule set is number: {best_rule}")
        print(f"The fitness score is {fitness_score}")
        print(f"This is generation number {generation}")
        print("------------------- ")

        if fitness_score < preferred_fitness_score:
            break # if the fitness score is reached, the while-loop ends, and the result is saved in a file
        mutated_set_of_rules = create_mutated_list_of_rules(mutated_set_of_rules[best_rule],number_of_rules)
        sim_output.clear()


    f = open("Bestspikes.txt", "w")
    for element in sim_output[best_rule]:
        f.write(str(element[0]) + " " + str(element[1]) + '\n')
    f.close()
