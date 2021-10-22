import random as r
#from numpy import num
import simulate as sim

def create_rule_table(length):

    rule_table = []
    for i in range(length):
        if r.random() < 0.5:
            rule_table.append(0)
        else:
            rule_table.append(1)
    return rule_table

def create_list_of_n_rules(n,rule_length):
    rule_list = []
    for i in range(n):
        rule_list.append(create_rule_table(rule_length))
    return rule_list


def create_mutated_list_of_rules(rule_table_to_mutate,number_of_rule_tables):
    mutated_list_of_rules = []
    for i in range(number_of_rule_tables):
        mutated_rule = rule_table_to_mutate[:]
        for j in range(len(mutated_rule)):
            if r.random() <= 0.5:
                if mutated_rule[j] == 0:
                    mutated_rule[j] = 1
                else:
                    mutated_rule[j] = 0
        mutated_list_of_rules.append(mutated_rule)
    return mutated_list_of_rules

    
    



if __name__ == '__main__':
    '''    hovedliste = [0,0,0,0,0,0,0,0,0,0]
        mutertliste = create_mutated_list_of_rules(hovedliste,15)



        print("--------")
        for i in range(len(mutertliste)):
            print(mutertliste[i])       
            '''
    list_of_rule_sets = create_list_of_n_rules(4,265)
    sim_output = sim.simulate(list_of_rule_sets)

    for i in range(len(sim_output)):
        print(sim_output[i])
        print("---------------------")

