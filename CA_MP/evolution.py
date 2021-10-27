import random as r
#from numpy import num
import simulate as sim
import fitness as fit
import time
#import tester as t

#her under kan du endre sannsynligheten for hvordan reglene skal se ut,
#har satt det som 20% sannsynlig å få en 1'er. Dette kan justeres

def create_rule_table(length):

    rule_table = []
    for i in range(length):
        if r.random() < 0.8:
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
    mutated_rule = rule_table_to_mutate[:]
    for i in range(number_of_rule_tables):
        #mutated_rule = rule_table_to_mutate[:]
        for j in range(len(mutated_rule)):
            if r.random() <= 0.1:
                if mutated_rule[j] == 0:
                    mutated_rule[j] = 1
                else:
                    mutated_rule[j] = 0
        mutated_list_of_rules.append(mutated_rule)
    return mutated_list_of_rules

    
    



if __name__ == '__main__':
    #Her velger du hvor mange regelsett du vil lage, den står på 4 nå
    antall_regler = 7
    ønsket_fitness_score = 15000 #Her må du nesten bare se ann litt, Dette er differansen
                            #Mellom antall spikes vi lager, og antall spikes i dense2310
    generasjon = 0
    list_of_rule_sets = create_list_of_n_rules(antall_regler,256)

    

    sim.initialize()
    fitness_score = 1000000000 # Setter den høyt sånn at den ikke har noe å si i starten, vil ha den så lav som mulig.
    
    t1 = time.perf_counter()

    sim_output = sim.simulate_MP(list_of_rule_sets) #Her sender vi inn reglene, og får tilbake spikes
    #print(sim_output)
    '''for i in range(len(sim_output)):
        print(sim_output)'''
    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
    print(f"sim_output er: {len(sim_output)} lang")

    #time.sleep(20)

    beste_regel, fitness_score = fit.pick_best_rule_set(sim_output) #Tester spikes opp mot original, returnerer regelnummer og score
    print(f"beste regel er denne: {beste_regel}")  #disse printene kan du endre på hvis du ikke vil se de underveis
    print(f"fitness score er {fitness_score}")
    print(f"Dette er generasjon nummer {generasjon}")
    #print(f"sim output er en {type(sim_output)}")
    
    ''' beste_regel, fitness_score = fit.freq_fit(fit.part_list_to_time_only(sim_output),1)
    print(f"BESTE REGEL ER DENNE: {beste_regel}")
    print(f"FITNESS score er {fitness_score}")'''

    #freq, fasit_freq = fit.get_fitness(fit.part_list_to_time_only(sim_output),1)
    #print(f"fasit er: {fasit_freq}")
    print("----------")
    '''for freqz in freq:
        print(freqz)'''
  
    sim_output.clear()

    



    while fitness_score > ønsket_fitness_score: 
        t1 = time.perf_counter()                        
        mutert_regelliste = create_mutated_list_of_rules(list_of_rule_sets[beste_regel],antall_regler)
        #print(f"mutert_regelliste er {len(mutert_regelliste)} lang")
        sim_output = []
        sim_output = sim.simulate_MP(mutert_regelliste)
        #print(f"nå er den {len(sim_output)} lang")

        beste_regel, fitness_score = fit.pick_best_rule_set(sim_output)
        generasjon += 1
        print(f"beste regel er denne: {beste_regel}")
        print(f"fitness score er {fitness_score}")
        print(f"Dette er generasjon nummer {generasjon}")
        if fitness_score < ønsket_fitness_score:
            break # må hindre den i å slette sim_output siste gangen sånn at vi får lagra den til fil.
        sim_output.clear()
        t2 = time.perf_counter()
        print(f'Finished in {t2-t1} seconds')
        #print(f"sim_output er: {len(sim_output)} lang")
        #time.sleep(20)


    f = open("Bestspikes.txt", "w")
    for element in sim_output[beste_regel]:
        f.write(str(element[0]) + " " + str(element[1]) + '\n')
    f.close()
