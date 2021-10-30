import random as r
import simulate as sim
import fitness as fit
import time
import copy
from datetime import datetime
import os
import shutil

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
    for i in range(100):
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")

        full_path = 'C:/Users/elias/OneDrive/OsloMet/Master/ACIT4610 AI/Prosjekt/NeuralDAtaProject-main/CA_Write_to_file/Test_Results'
        path = ("\CA_Final\Test_Results")

        print(f"{path}\\{dt_string}")
        os.makedirs(f'{full_path}/{dt_string}')
        generation = 0
        list_of_rule_sets = create_list_of_n_rules(number_of_rules,256) #Creating rules

        sim.initialize() #Method for setting up the grid of electrodes
        fitness_score = 1000000000 # Setting the fitness score high, so it won't interfere in the beginning.
        
        t1 = time.perf_counter()
        sim_output = sim.simulate_MP(list_of_rule_sets) #Generate spikes based on the given rules of this generation
        t2 = time.perf_counter()
        #print(sim_output)
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
        fitness_list = []
        fitness_list.append(fitness_score)
        dir = 'C:/Users/elias/OneDrive/OsloMet/Master/ACIT4610 AI/Prosjekt/NeuralDAtaProject-main/CA_Write_to_file/Spike_Lists'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        '''
        Method that runs until preferred fitness score is reached
        '''
        for i in range(25):
        #while fitness_score > preferred_fitness_score: 
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
            fitness_list.append(fitness_score)
            '''if fitness_score < preferred_fitness_score:
                break # if the fitness score is reached, the while-loop ends, and the result is saved in a file'''

            rule_name = sim_output[best_rule].replace("C:/Users/elias/OneDrive/OsloMet/Master/ACIT4610 AI/Prosjekt/NeuralDAtaProject-main/CA_Write_to_file/Spike_Lists/","")
            src = f'CA_Write_to_file/Spike_Lists/{rule_name}'
            #dst = f'CA_Write_to_file/Test_Results/{dt_string}/{rule_name}'
            new_name = f'CA_Write_to_file/Test_Results/{dt_string}/Generation_{generation}_FitScore_{fitness_score}.txt'
            #shutil.copyfile(src,dst)
            os.rename(src,new_name)


            '''f = open(f"{full_path}/{dt_string}/Generation_{generation}_FitScore_{fitness_score}.txt", "w")
            for element in sim_output[best_rule]:
                f.write(str(element[0]) + " " + str(element[1]) + '\n')
            f.close()'''
            mutated_set_of_rules = create_mutated_list_of_rules(mutated_set_of_rules[best_rule],number_of_rules)
            sim_output.clear()
            dir = 'C:/Users/elias/OneDrive/OsloMet/Master/ACIT4610 AI/Prosjekt/NeuralDAtaProject-main/CA_Write_to_file/Spike_Lists'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))


        f = open(f"{full_path}/{dt_string}/Fitness_score.txt", "w")
        for element in fitness_list:
            f.write(str(element) + '\n')
        f.close()
